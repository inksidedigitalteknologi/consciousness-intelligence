# core/dividend_history.py
# DIVIDEND HISTORY MODULE
# Fetch & analyze dividend history for trap detection
#
# Features:
# - Fetch 10+ years dividend history (yfinance)
# - Calculate CAGR (1Y, 3Y, 5Y, 10Y, 20Y)
# - Detect dividend cuts
# - Consecutive years of increase (Dividend King/Aristocrat/Champion)
# - Yield on cost
# - Payout ratio trend

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class DividendHistorySummary:
    """Ringkasan history dividen."""
    symbol: str
    total_records: int
    first_date: str
    last_date: str
    first_amount: float
    last_amount: float
    years_of_history: float

    # Growth
    cagr_1y: float = 0.0
    cagr_3y: float = 0.0
    cagr_5y: float = 0.0
    cagr_10y: float = 0.0
    cagr_20y: float = 0.0

    # Cuts & streak
    cut_count: int = 0
    last_cut_date: str = ""
    last_cut_pct: float = 0.0
    consecutive_increase_years: int = 0
    is_dividend_king: bool = False       # 50+ years
    is_dividend_aristocrat: bool = False  # 25+ years
    is_dividend_champion: bool = False    # 10+ years

    # Current
    current_annual: float = 0.0
    current_yield: float = 0.0
    yield_on_cost_5y: float = 0.0
    yield_on_cost_10y: float = 0.0

    # History list
    yearly_history: List[Dict[str, Any]] = field(default_factory=list)

    # Flags
    flags: List[str] = field(default_factory=list)

    error: str = ""


# ============================================================
# DIVIDEND HISTORY
# ============================================================

class DividendHistory:
    """Fetch & analyze dividend history."""

    def __init__(self, symbol: str):
        self.symbol = symbol.upper().strip()
        self._cache: Optional[DividendHistorySummary] = None
        self._cache_time: Optional[datetime] = None
        self._cache_ttl = 3600  # 1 hour

    def fetch(self, years: int = 10) -> DividendHistorySummary:
        """Fetch dividend history pakai yfinance."""
        # Cache
        if self._cache and self._cache_time:
            if (datetime.now() - self._cache_time).total_seconds() < self._cache_ttl:
                return self._cache

        try:
            import yfinance as yf
        except ImportError:
            return DividendHistorySummary(
                symbol=self.symbol,
                total_records=0,
                first_date="", last_date="",
                first_amount=0, last_amount=0,
                years_of_history=0,
                error="yfinance not installed"
            )

        try:
            ticker = yf.Ticker(self.symbol)
            divs = ticker.dividends
        except Exception as e:
            return DividendHistorySummary(
                symbol=self.symbol,
                total_records=0,
                first_date="", last_date="",
                first_amount=0, last_amount=0,
                years_of_history=0,
                error=f"yfinance error: {e}"
            )

        if divs is None or len(divs) == 0:
            return DividendHistorySummary(
                symbol=self.symbol,
                total_records=0,
                first_date="", last_date="",
                first_amount=0, last_amount=0,
                years_of_history=0,
                error="No dividend data"
            )

        # Convert ke DataFrame-like
        records = []
        for date, amount in divs.items():
            records.append({
                'date': date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date),
                'amount': float(amount),
            })

        # Sort by date
        records.sort(key=lambda x: x['date'])

        # Group by year (sum per year)
        yearly = {}
        for r in records:
            year = r['date'][:4]
            yearly.setdefault(year, []).append(r['amount'])

        yearly_history = []
        for year in sorted(yearly.keys()):
            amounts = yearly[year]
            yearly_history.append({
                'year': int(year),
                'total': round(sum(amounts), 4),
                'count': len(amounts),
                'avg': round(sum(amounts) / len(amounts), 4),
            })

        # Basic info
        first = records[0]
        last = records[-1]
        first_dt = datetime.strptime(first['date'], '%Y-%m-%d')
        last_dt = datetime.strptime(last['date'], '%Y-%m-%d')
        years_hist = (last_dt - first_dt).days / 365.25

        # Current annual (sum of last 4 records, or trailing 12 months)
        current_annual = self._get_trailing_annual(records)

        # Growth
        cagr_1y = self._cagr(yearly_history, 1)
        cagr_3y = self._cagr(yearly_history, 3)
        cagr_5y = self._cagr(yearly_history, 5)
        cagr_10y = self._cagr(yearly_history, 10)
        cagr_20y = self._cagr(yearly_history, 20)

        # Cuts & streak
        cuts = self._detect_cuts(yearly_history)
        cut_count = len(cuts)
        last_cut_date = cuts[-1]['year'] if cuts else ""
        last_cut_pct = cuts[-1]['pct'] if cuts else 0.0

        streak = self._consecutive_increase_years(yearly_history)

        # Current yield (butuh harga)
        current_yield = 0.0
        current_price = self._get_current_price()
        if current_price and current_price > 0:
            current_yield = (current_annual / current_price) * 100

        # Yield on cost
        yoc_5y = self._yield_on_cost(yearly_history, 5)
        yoc_10y = self._yield_on_cost(yearly_history, 10)

        # Flags
        flags = []
        if cut_count > 0:
            flags.append(f"DIVIDEND_CUT_{cut_count}X")
        if cagr_5y < 0:
            flags.append("NEGATIVE_GROWTH_5Y")
        if streak >= 50:
            flags.append("DIVIDEND_KING")
        elif streak >= 25:
            flags.append("DIVIDEND_ARISTOCRAT")
        elif streak >= 10:
            flags.append("DIVIDEND_CHAMPION")
        if years_hist < 5:
            flags.append("SHORT_HISTORY")

        summary = DividendHistorySummary(
            symbol=self.symbol,
            total_records=len(records),
            first_date=first['date'],
            last_date=last['date'],
            first_amount=round(first['amount'], 4),
            last_amount=round(last['amount'], 4),
            years_of_history=round(years_hist, 2),
            cagr_1y=round(cagr_1y, 2),
            cagr_3y=round(cagr_3y, 2),
            cagr_5y=round(cagr_5y, 2),
            cagr_10y=round(cagr_10y, 2),
            cagr_20y=round(cagr_20y, 2),
            cut_count=cut_count,
            last_cut_date=str(last_cut_date),
            last_cut_pct=round(last_cut_pct, 2),
            consecutive_increase_years=streak,
            is_dividend_king=streak >= 50,
            is_dividend_aristocrat=streak >= 25,
            is_dividend_champion=streak >= 10,
            current_annual=round(current_annual, 4),
            current_yield=round(current_yield, 2),
            yield_on_cost_5y=round(yoc_5y, 2),
            yield_on_cost_10y=round(yoc_10y, 2),
            yearly_history=yearly_history[-20:],  # last 20 years
            flags=flags,
        )

        self._cache = summary
        self._cache_time = datetime.now()
        return summary

    # ============================================================
    # HELPERS
    # ============================================================

    def _get_trailing_annual(self, records: List[Dict]) -> float:
        """Sum of dividends in trailing 12 months."""
        if not records:
            return 0.0
        last_date = datetime.strptime(records[-1]['date'], '%Y-%m-%d')
        cutoff = last_date - timedelta(days=365)
        total = 0.0
        for r in records:
            try:
                d = datetime.strptime(r['date'], '%Y-%m-%d')
                if d >= cutoff:
                    total += r['amount']
            except Exception:
                continue
        return total

    def _cagr(self, yearly: List[Dict], period: int) -> float:
        """Hitung CAGR dividen berdasarkan annualized (avg per payment * freq)."""
        # Hanya pakai tahun yang lengkap (>= 4 pembayaran untuk quarterly)
        complete = [y for y in yearly if y['count'] >= 4]
        if len(complete) < period + 1:
            # Fallback: pakai semua tahun
            complete = yearly
        if len(complete) < period + 1:
            return 0.0

        # Pakai avg per payment * 4 (annualized quarterly)
        def annualize(y):
            return y['avg'] * 4 if y['count'] > 0 else 0

        end = annualize(complete[-1])
        start = annualize(complete[-(period + 1)])
        if start <= 0:
            return 0.0
        try:
            return ((end / start) ** (1.0 / period) - 1) * 100
        except Exception:
            return 0.0
    def _detect_cuts(self, yearly: List[Dict]) -> List[Dict]:
        """Deteksi pemotongan dividen berdasarkan avg per payment (bukan total tahunan)."""
        # Hanya bandingkan tahun yang lengkap
        complete = [y for y in yearly if y['count'] >= 4]
        if len(complete) < 2:
            complete = yearly

        cuts = []
        for i in range(1, len(complete)):
            prev = complete[i - 1]['avg']  # avg per payment
            curr = complete[i]['avg']
            if prev > 0 and curr < prev * 0.98:  # toleransi 2%
                pct = ((prev - curr) / prev) * 100
                cuts.append({
                    'year': complete[i]['year'],
                    'prev': round(prev, 4),
                    'curr': round(curr, 4),
                    'pct': round(pct, 2),
                })
        return cuts
    def _consecutive_increase_years(self, yearly: List[Dict]) -> int:
        """Hitung berapa tahun berturut-turut dividen naik (per payment)."""
        # Hanya pakai tahun lengkap
        complete = [y for y in yearly if y['count'] >= 4]
        if len(complete) < 2:
            complete = yearly

        streak = 0
        for i in range(len(complete) - 1, 0, -1):
            prev = complete[i - 1]['avg']
            curr = complete[i]['avg']
            if prev > 0 and curr >= prev * 0.99:  # toleransi 1%
                streak += 1
            else:
                break
        return streak
    def _yield_on_cost(self, yearly: List[Dict], years_ago: int) -> float:
        """Yield berdasarkan harga beli N tahun lalu."""
        if len(yearly) < years_ago + 1:
            return 0.0
        # Simplified: assume price was 20x dividend then
        past = yearly[-(years_ago + 1)]['total']
        if past <= 0:
            return 0.0
        current = yearly[-1]['total']
        # Yield on cost = current annual / past price
        # Assume past price ~ 20x past annual dividend
        past_price = past * 20
        if past_price <= 0:
            return 0.0
        return (current / past_price) * 100

    def _get_current_price(self) -> float:
        """Get current price pakai yfinance."""
        try:
            import yfinance as yf
            ticker = yf.Ticker(self.symbol)
            info = ticker.info
            return float(info.get('currentPrice') or info.get('regularMarketPrice') or 0)
        except Exception:
            return 0.0


# ============================================================
# SINGLETON & SHORTCUT
# ============================================================

def get_dividend_history(symbol: str) -> Dict[str, Any]:
    """Shortcut untuk fetch history."""
    h = DividendHistory(symbol)
    return asdict(h.fetch())


__all__ = ['DividendHistory', 'DividendHistorySummary', 'get_dividend_history']
