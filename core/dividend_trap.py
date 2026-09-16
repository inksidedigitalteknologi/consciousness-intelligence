# core/dividend_trap.py
# DIVIDEND TRAP DETECTOR
# Detect dividend traps — high yield but unsustainable dividends
#
# Factors:
# - Payout ratio > 80%
# - Free cash flow negative
# - Debt-to-equity > 2
# - Dividend cut history
# - Yield > 2x sector
# - Earnings declining
# - Price downtrend
# - Interest coverage < 1.5x
# - Dividend King/Aristocrat bonus (-30)

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict

from core.dividend_history import DividendHistory, DividendHistorySummary

logger = logging.getLogger(__name__)


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class TrapAnalysis:
    """Hasil analisis dividend trap."""
    symbol: str
    name: str = ""
    sector: str = ""

    # Scores
    trap_score: int = 0            # 0-100
    category: str = "UNKNOWN"      # SAFE / CAUTION / RISKY / TRAP
    recommendation: str = "HOLD"

    # Raw metrics
    current_price: float = 0.0
    current_yield: float = 0.0
    payout_ratio: float = 0.0
    free_cash_flow: float = 0.0
    debt_to_equity: float = 0.0
    interest_coverage: float = 0.0
    earnings_growth_3y: float = 0.0
    price_change_1y: float = 0.0

    # From history
    history_years: float = 0.0
    streak_years: int = 0
    cut_count: int = 0
    cagr_5y: float = 0.0
    cagr_10y: float = 0.0
    is_king: bool = False
    is_aristocrat: bool = False
    is_champion: bool = False

    # Flags
    red_flags: List[Dict[str, Any]] = field(default_factory=list)
    green_flags: List[Dict[str, Any]] = field(default_factory=list)

    # History
    history: Optional[Dict[str, Any]] = None

    error: str = ""


# ============================================================
# SECTOR YIELD (untuk perbandingan)
# ============================================================

SECTOR_AVG_YIELD = {
    'Technology': 1.5,
    'Financial': 3.0,
    'Healthcare': 2.5,
    'Consumer': 2.5,
    'Energy': 4.0,
    'Industrial': 2.5,
    'Utilities': 3.5,
    'Real Estate': 4.0,
    'Materials': 2.5,
    'Communication': 3.0,
    'ETF': 2.0,
    'Unknown': 2.5,
}


# ============================================================
# DIVIDEND TRAP DETECTOR
# ============================================================

class DividendTrapDetector:
    """Deteksi dividend trap."""

    def __init__(self, symbol: str, name: str = "", sector: str = ""):
        self.symbol = symbol.upper().strip()
        self.name = name
        self.sector = sector or "Unknown"

    def analyze(self) -> TrapAnalysis:
        """Analisis lengkap dividend trap."""
        # Get history
        hist = DividendHistory(self.symbol).fetch()

        # Get fundamentals dari yfinance
        fundamentals = self._fetch_fundamentals()

        # Mulai analisis
        red_flags = []
        green_flags = []
        score = 0

        # ============================================================
        # 1. PAYOUT RATIO (max 20)
        # ============================================================
        payout = fundamentals.get('payout_ratio', 0)
        if payout > 0:
            if payout > 100:
                score += 20
                red_flags.append({
                    'code': 'PAYOUT_RATIO_OVER_100',
                    'severity': 'CRITICAL',
                    'message': f'Payout ratio {payout:.0f}% — membayar lebih dari pendapatan',
                    'weight': 20,
                })
            elif payout > 80:
                score += 15
                red_flags.append({
                    'code': 'PAYOUT_RATIO_HIGH',
                    'severity': 'HIGH',
                    'message': f'Payout ratio {payout:.0f}% — sangat tinggi',
                    'weight': 15,
                })
            elif payout < 40:
                green_flags.append({
                    'code': 'PAYOUT_RATIO_LOW',
                    'message': f'Payout ratio {payout:.0f}% — sehat, ada ruang naik',
                })
            elif payout < 60:
                green_flags.append({
                    'code': 'PAYOUT_RATIO_MODERATE',
                    'message': f'Payout ratio {payout:.0f}% — wajar',
                })

        # ============================================================
        # 2. FREE CASH FLOW (max 25)
        # ============================================================
        fcf = fundamentals.get('free_cash_flow', 0)
        if fcf != 0:
            if fcf < 0:
                score += 25
                red_flags.append({
                    'code': 'FCF_NEGATIVE',
                    'severity': 'CRITICAL',
                    'message': f'Free cash flow negatif (${fcf/1e9:.2f}B)',
                    'weight': 25,
                })
            else:
                green_flags.append({
                    'code': 'FCF_POSITIVE',
                    'message': f'Free cash flow positif (${fcf/1e9:.2f}B)',
                })

        # ============================================================
        # 3. DEBT-TO-EQUITY (max 15)
        # ============================================================
        de = fundamentals.get('debt_to_equity', 0)
        if de > 0:
            if de > 200:
                score += 15
                red_flags.append({
                    'code': 'DEBT_VERY_HIGH',
                    'severity': 'HIGH',
                    'message': f'Debt-to-equity {de:.0f}% — sangat tinggi',
                    'weight': 15,
                })
            elif de > 100:
                score += 8
                red_flags.append({
                    'code': 'DEBT_HIGH',
                    'severity': 'MEDIUM',
                    'message': f'Debt-to-equity {de:.0f}% — tinggi',
                    'weight': 8,
                })
            elif de < 50:
                green_flags.append({
                    'code': 'DEBT_LOW',
                    'message': f'Debt-to-equity {de:.0f}% — rendah, sehat',
                })

        # ============================================================
        # 4. DIVIDEND CUT HISTORY (max 20)
        # ============================================================
        if hist.cut_count > 0:
            # Kalau cut baru (< 5 tahun), lebih berat
            score += 20
            severity = 'HIGH' if hist.cut_count >= 2 else 'MEDIUM'
            red_flags.append({
                'code': 'DIVIDEND_CUT_HISTORY',
                'severity': severity,
                'message': f'Pernah potong dividen {hist.cut_count}x (terakhir {hist.last_cut_date}, -{hist.last_cut_pct:.1f}%)',
                'weight': 20,
            })

        # ============================================================
        # 5. YIELD > 2x SECTOR (max 10)
        # ============================================================
        sector_yield = SECTOR_AVG_YIELD.get(self.sector, 2.5)
        if hist.current_yield > 0 and sector_yield > 0:
            if hist.current_yield > 2 * sector_yield:
                score += 10
                red_flags.append({
                    'code': 'YIELD_TOO_HIGH',
                    'severity': 'MEDIUM',
                    'message': f'Yield {hist.current_yield:.1f}% > 2x rata-rata sektor ({sector_yield:.1f}%)',
                    'weight': 10,
                })

        # ============================================================
        # 6. EARNINGS GROWTH 3Y (max 10)
        # ============================================================
        earnings_growth = fundamentals.get('earnings_growth_3y', 0)
        if earnings_growth < 0:
            score += 10
            red_flags.append({
                'code': 'EARNINGS_DECLINING',
                'severity': 'MEDIUM',
                'message': f'Laba turun {abs(earnings_growth):.1f}% (3Y)',
                'weight': 10,
            })
        elif earnings_growth > 10:
            green_flags.append({
                'code': 'EARNINGS_GROWING',
                'message': f'Laba naik {earnings_growth:.1f}% (3Y)',
            })

        # ============================================================
        # 7. PRICE DOWNTREND (max 15)
        # ============================================================
        price_change = fundamentals.get('price_change_1y', 0)
        if price_change < -30:
            score += 15
            red_flags.append({
                'code': 'PRICE_DOWNTREND_SEVERE',
                'severity': 'HIGH',
                'message': f'Harga turun {abs(price_change):.1f}% (1Y)',
                'weight': 15,
            })
        elif price_change < -15:
            score += 8
            red_flags.append({
                'code': 'PRICE_DOWNTREND',
                'severity': 'MEDIUM',
                'message': f'Harga turun {abs(price_change):.1f}% (1Y)',
                'weight': 8,
            })
        elif price_change > 20:
            green_flags.append({
                'code': 'PRICE_UPTREND',
                'message': f'Harga naik {price_change:.1f}% (1Y)',
            })

        # ============================================================
        # 8. INTEREST COVERAGE (max 10)
        # ============================================================
        ic = fundamentals.get('interest_coverage', 0)
        if ic > 0 and ic < 1.5:
            score += 10
            red_flags.append({
                'code': 'LOW_INTEREST_COVERAGE',
                'severity': 'HIGH',
                'message': f'Interest coverage {ic:.2f}x — rendah, sulit bayar utang',
                'weight': 10,
            })
        elif ic > 5:
            green_flags.append({
                'code': 'STRONG_INTEREST_COVERAGE',
                'message': f'Interest coverage {ic:.2f}x — kuat',
            })

        # ============================================================
        # 9. BONUS: DIVIDEND KING / ARISTOCRAT (-30)
        # ============================================================
        if hist.is_dividend_king:
            score -= 30
            green_flags.append({
                'code': 'DIVIDEND_KING',
                'message': f'🏆 Dividend King — {hist.consecutive_increase_years} tahun naik terus',
            })
        elif hist.is_dividend_aristocrat:
            score -= 20
            green_flags.append({
                'code': 'DIVIDEND_ARISTOCRAT',
                'message': f'👑 Dividend Aristocrat — {hist.consecutive_increase_years} tahun naik terus',
            })
        elif hist.is_dividend_champion:
            score -= 10
            green_flags.append({
                'code': 'DIVIDEND_CHAMPION',
                'message': f'🎖️ Dividend Champion — {hist.consecutive_increase_years} tahun naik terus',
            })

        # ============================================================
        # 10. BONUS: STRONG GROWTH (-15)
        # ============================================================
        if hist.cagr_5y > 10:
            score -= 15
            green_flags.append({
                'code': 'STRONG_DIVIDEND_GROWTH',
                'message': f'Dividen tumbuh {hist.cagr_5y:.1f}% CAGR (5Y)',
            })
        elif hist.cagr_5y > 5:
            score -= 8
            green_flags.append({
                'code': 'GOOD_DIVIDEND_GROWTH',
                'message': f'Dividen tumbuh {hist.cagr_5y:.1f}% CAGR (5Y)',
            })

        # ============================================================
        # FINAL SCORE
        # ============================================================
        score = max(0, min(100, score))

        # Category
        if score >= 70:
            category = 'TRAP'
            recommendation = 'AVOID'
        elif score >= 50:
            category = 'RISKY'
            recommendation = 'MONITOR'
        elif score >= 30:
            category = 'CAUTION'
            recommendation = 'HOLD'
        else:
            category = 'SAFE'
            recommendation = 'BUY' if score < 15 else 'STRONG BUY'

        # Build result
        return TrapAnalysis(
            symbol=self.symbol,
            name=self.name or fundamentals.get('name', ''),
            sector=self.sector,
            trap_score=score,
            category=category,
            recommendation=recommendation,
            current_price=fundamentals.get('current_price', 0),
            current_yield=hist.current_yield,
            payout_ratio=round(payout, 2),
            free_cash_flow=round(fcf / 1e9, 3) if fcf else 0,
            debt_to_equity=round(de, 2),
            interest_coverage=round(ic, 2),
            earnings_growth_3y=round(earnings_growth, 2),
            price_change_1y=round(price_change, 2),
            history_years=hist.years_of_history,
            streak_years=hist.consecutive_increase_years,
            cut_count=hist.cut_count,
            cagr_5y=hist.cagr_5y,
            cagr_10y=hist.cagr_10y,
            is_king=hist.is_dividend_king,
            is_aristocrat=hist.is_dividend_aristocrat,
            is_champion=hist.is_dividend_champion,
            red_flags=red_flags,
            green_flags=green_flags,
            history=asdict(hist) if hist else None,
        )

    def _fetch_fundamentals(self) -> Dict[str, Any]:
        """Fetch fundamental data dari yfinance."""
        try:
            import yfinance as yf
            ticker = yf.Ticker(self.symbol)
            info = ticker.info

            current_price = float(info.get('currentPrice') or info.get('regularMarketPrice') or 0)
            payout_ratio = float(info.get('payoutRatio') or 0) * 100
            free_cash_flow = float(info.get('freeCashflow') or 0)
            debt_to_equity = float(info.get('debtToEquity') or 0)
            earnings_growth = float(info.get('earningsGrowth') or 0) * 100
            name = info.get('longName') or info.get('shortName') or self.name
            sector = info.get('sector') or self.sector

            # Interest coverage = EBIT / Interest Expense
            ebit = float(info.get('ebitda') or 0)
            interest_expense = float(info.get('interestExpense') or 0)
            interest_coverage = abs(ebit / interest_expense) if interest_expense != 0 else 0

            # Price change 1Y
            hist = ticker.history(period='1y')
            price_change = 0
            if len(hist) >= 2:
                first = float(hist['Close'].iloc[0])
                last = float(hist['Close'].iloc[-1])
                if first > 0:
                    price_change = ((last - first) / first) * 100

            return {
                'name': name,
                'sector': sector,
                'current_price': current_price,
                'payout_ratio': payout_ratio,
                'free_cash_flow': free_cash_flow,
                'debt_to_equity': debt_to_equity,
                'earnings_growth_3y': earnings_growth,
                'interest_coverage': interest_coverage,
                'price_change_1y': price_change,
            }
        except Exception as e:
            logger.warning(f"Fundamentals fetch failed for {self.symbol}: {e}")
            return {}


# ============================================================
# SHORTCUT
# ============================================================

def analyze_trap(symbol: str, name: str = "", sector: str = "") -> Dict[str, Any]:
    """Shortcut untuk analisis trap."""
    detector = DividendTrapDetector(symbol, name, sector)
    return asdict(detector.analyze())


__all__ = ['DividendTrapDetector', 'TrapAnalysis', 'analyze_trap']
