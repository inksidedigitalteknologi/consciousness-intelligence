# core/dividend_brain.py
# DIVIDEND BRAIN — Integrasi Dividend dengan Cognitive Brain
# Menggabungkan dividend analysis dengan brain decision engine
#
# Features:
# - Analyze dividend opportunity with brain
# - Dividend capture strategy (buy before ex-date)
# - Trap detection with brain confirmation
# - Timing recommendation (BUY BEFORE / WAIT / SKIP)

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict

from core.dividend_history import DividendHistory, DividendHistorySummary
from core.dividend_trap import DividendTrapDetector, TrapAnalysis

logger = logging.getLogger(__name__)


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class DividendOpportunity:
    """Peluang dividen lengkap dengan brain analysis."""
    symbol: str
    name: str = ""
    sector: str = ""

    # Timing
    ex_date: str = ""
    pay_date: str = ""
    record_date: str = ""
    announcement_date: str = ""
    days_to_ex: int = 0
    days_to_pay: int = 0
    timing_status: str = "UNKNOWN"  # UPCOMING / TODAY / PAST / NO_DATA

    # Dividend
    dividend_amount: float = 0.0
    annual_dividend: float = 0.0
    current_yield: float = 0.0
    frequency: str = ""

    # Trap analysis
    trap_score: int = 0
    trap_category: str = "UNKNOWN"
    trap_recommendation: str = "HOLD"

    # History
    streak_years: int = 0
    cut_count: int = 0
    cagr_5y: float = 0.0
    cagr_10y: float = 0.0
    is_king: bool = False
    is_aristocrat: bool = False
    is_champion: bool = False

    # Fundamentals
    current_price: float = 0.0
    payout_ratio: float = 0.0
    free_cash_flow: float = 0.0
    debt_to_equity: float = 0.0

    # Brain analysis
    brain_confidence: float = 0.0
    brain_sentiment: str = "NEUTRAL"
    brain_decision: str = "HOLD"
    brain_reasoning: List[str] = field(default_factory=list)

    # Strategy
    strategy: str = "WAIT"  # BUY_BEFORE_EX / BUY_NOW / WAIT / SKIP
    strategy_reason: str = ""

    # Capture calculation
    expected_drop: float = 0.0
    net_dividend: float = 0.0
    net_profit_pct: float = 0.0
    capture_verdict: str = "UNKNOWN"  # WORTH_IT / NOT_WORTH

    # Red/Green flags
    red_flags: List[Dict[str, Any]] = field(default_factory=list)
    green_flags: List[Dict[str, Any]] = field(default_factory=list)

    error: str = ""


# ============================================================
# DIVIDEND BRAIN
# ============================================================

class DividendBrain:
    """Integrasi dividend dengan cognitive brain."""

    def __init__(self, brain_instance=None):
        self.brain = brain_instance

    # ============================================================
    # MAIN: ANALYZE OPPORTUNITY
    # ============================================================

    def analyze_opportunity(self, symbol: str) -> DividendOpportunity:
        """Analisis peluang dividen lengkap dengan brain."""
        symbol = symbol.upper().strip()

        try:
            # 1. Fetch dividend data dari module yang ada
            from core.dividend import dividend as div_module
            if div_module.df.empty:
                div_module.fetch()

            # Cari di DataFrame
            row = None
            if not div_module.df.empty:
                matches = div_module.df[div_module.df['symbol'] == symbol]
                if not matches.empty:
                    row = matches.iloc[0].to_dict()

            # 2. Fetch trap analysis
            trap = DividendTrapDetector(symbol).analyze()

            # 3. Build opportunity
            opp = DividendOpportunity(
                symbol=symbol,
                name=trap.name or (row.get('name') if row else ''),
                sector=trap.sector or (row.get('sector') if row else ''),
                current_price=trap.current_price,
                current_yield=trap.current_yield,
                trap_score=trap.trap_score,
                trap_category=trap.category,
                trap_recommendation=trap.recommendation,
                streak_years=trap.streak_years,
                cut_count=trap.cut_count,
                cagr_5y=trap.cagr_5y,
                cagr_10y=trap.cagr_10y,
                is_king=trap.is_king,
                is_aristocrat=trap.is_aristocrat,
                is_champion=trap.is_champion,
                payout_ratio=trap.payout_ratio,
                free_cash_flow=trap.free_cash_flow,
                debt_to_equity=trap.debt_to_equity,
                red_flags=trap.red_flags,
                green_flags=trap.green_flags,
            )

            # 4. Isi data dari row (Nasdaq)
            if row:
                opp.ex_date = row.get('ex_date', '') or ''
                opp.pay_date = row.get('pay_date', '') or ''
                opp.record_date = row.get('record_date', '') or ''
                opp.announcement_date = row.get('announcement_date', '') or ''
                opp.dividend_amount = float(row.get('dividend', 0) or 0)
                opp.annual_dividend = float(row.get('annual_dividend', 0) or 0)
                opp.frequency = row.get('frequency', '') or ''

            # 5. Hitung timing
            self._calculate_timing(opp)

            # 6. Brain analysis
            self._analyze_with_brain(opp)

            # 7. Capture strategy
            self._calculate_capture(opp)

            # 8. Strategy recommendation
            self._recommend_strategy(opp)

            return opp

        except Exception as e:
            logger.error(f"DividendBrain error for {symbol}: {e}")
            return DividendOpportunity(symbol=symbol, error=str(e))

    # ============================================================
    # TIMING
    # ============================================================

    def _calculate_timing(self, opp: DividendOpportunity):
        """Hitung timing ex-date dan pay-date."""
        now = datetime.now()

        # Kalau ex_date kosong, enrich dari history
        if not opp.ex_date:
            self._enrich_timing_from_history(opp)

        if opp.ex_date:
            try:
                ex_dt = datetime.strptime(opp.ex_date, '%Y-%m-%d')
                delta = (ex_dt - now).days
                opp.days_to_ex = delta
                if delta > 0:
                    opp.timing_status = 'UPCOMING'
                elif delta == 0:
                    opp.timing_status = 'TODAY'
                else:
                    opp.timing_status = 'PAST'
            except Exception:
                opp.timing_status = 'UNKNOWN'

        if opp.pay_date:
            try:
                pay_dt = datetime.strptime(opp.pay_date, '%Y-%m-%d')
                opp.days_to_pay = (pay_dt - now).days
            except Exception:
                pass

    def _enrich_timing_from_history(self, opp: DividendOpportunity):
        """Kalau ex-date tidak ada di Nasdaq, ambil dari history yfinance."""
        try:
            import yfinance as yf
            from datetime import timezone
            ticker = yf.Ticker(opp.symbol)
            divs = ticker.dividends

            if divs is None or len(divs) == 0:
                return

            recent = divs.tail(8)
            last_date = recent.index[-1]
            last_amount = float(recent.iloc[-1])

            # Convert ke naive datetime (strip timezone)
            last_dt = last_date.to_pydatetime() if hasattr(last_date, 'to_pydatetime') else last_date
            if last_dt.tzinfo is not None:
                last_dt = last_dt.replace(tzinfo=None)

            if len(recent) >= 2:
                dates = []
                for d in recent.index:
                    dt = d.to_pydatetime() if hasattr(d, 'to_pydatetime') else d
                    if dt.tzinfo is not None:
                        dt = dt.replace(tzinfo=None)
                    dates.append(dt)

                deltas = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
                avg_delta = sum(deltas) / len(deltas) if deltas else 90

                predicted = last_dt + timedelta(days=avg_delta)
                now = datetime.now()

                if predicted > now:
                    opp.ex_date = predicted.strftime('%Y-%m-%d')
                    opp.dividend_amount = last_amount
                    opp.frequency = 'Quarterly' if 80 <= avg_delta <= 100 else 'Unknown'
                    pay = predicted + timedelta(days=14)
                    opp.pay_date = pay.strftime('%Y-%m-%d')
                else:
                    opp.ex_date = last_dt.strftime('%Y-%m-%d')
                    opp.dividend_amount = last_amount
                    opp.frequency = 'Quarterly' if 80 <= avg_delta <= 100 else 'Unknown'
                    pay = last_dt + timedelta(days=14)
                    opp.pay_date = pay.strftime('%Y-%m-%d')
            else:
                opp.ex_date = last_dt.strftime('%Y-%m-%d')
                opp.dividend_amount = last_amount
                opp.pay_date = (last_dt + timedelta(days=14)).strftime('%Y-%m-%d')

        except Exception as e:
            logger.warning(f"History timing enrich failed for {opp.symbol}: {e}")

    # ============================================================
    # BRAIN ANALYSIS
    # ============================================================

    def _analyze_with_brain(self, opp: DividendOpportunity):
        """Analisis pakai Brain kalau tersedia."""
        if not self.brain:
            # Fallback: reasoning sederhana
            self._simple_reasoning(opp)
            return

        try:
            data = {
                'symbol': opp.symbol,
                'dividend_yield': opp.current_yield,
                'trap_score': opp.trap_score,
                'streak_years': opp.streak_years,
                'cut_count': opp.cut_count,
                'cagr_5y': opp.cagr_5y,
                'payout_ratio': opp.payout_ratio,
                'free_cash_flow': opp.free_cash_flow,
                'debt_to_equity': opp.debt_to_equity,
                'days_to_ex': opp.days_to_ex,
                'type': 'dividend_analysis',
            }

            result = self.brain.observe(data)

            if isinstance(result, dict):
                opp.brain_confidence = float(result.get('confidence', 0)) * 100
                opp.brain_sentiment = result.get('sentiment', 'NEUTRAL')
                opp.brain_decision = result.get('decision', 'HOLD')

                reasoning = result.get('reasoning') or result.get('reasoning_steps') or []
                if isinstance(reasoning, list):
                    opp.brain_reasoning = [str(r) for r in reasoning[:5]]

            if not opp.brain_reasoning:
                self._simple_reasoning(opp)

        except Exception as e:
            logger.warning(f"Brain analysis failed: {e}")
            self._simple_reasoning(opp)

    def _simple_reasoning(self, opp: DividendOpportunity):
        """Fallback reasoning tanpa Brain."""
        reasons = []

        if opp.trap_score < 30:
            reasons.append(f"Trap score {opp.trap_score}/100 — low risk")
        elif opp.trap_score < 50:
            reasons.append(f"Trap score {opp.trap_score}/100 — moderate risk")
        else:
            reasons.append(f"Trap score {opp.trap_score}/100 — high risk")

        if opp.is_king:
            reasons.append(f"Dividend King — {opp.streak_years} years of increases")
        elif opp.is_aristocrat:
            reasons.append(f"Dividend Aristocrat — {opp.streak_years} years of increases")
        elif opp.is_champion:
            reasons.append(f"Dividend Champion — {opp.streak_years} years of increases")

        if opp.cut_count > 0:
            reasons.append(f"Dividend cut {opp.cut_count}x in history")

        if opp.cagr_5y > 5:
            reasons.append(f"Dividend growth {opp.cagr_5y:.1f}% CAGR (5Y)")
        elif opp.cagr_5y < 0:
            reasons.append(f"Negative growth {opp.cagr_5y:.1f}% (5Y)")

        if opp.payout_ratio > 80:
            reasons.append(f"Payout ratio high ({opp.payout_ratio:.0f}%)")
        elif opp.payout_ratio > 0 and opp.payout_ratio < 50:
            reasons.append(f"Payout ratio healthy ({opp.payout_ratio:.0f}%)")

        opp.brain_reasoning = reasons
        opp.brain_confidence = max(0, 100 - opp.trap_score)
        opp.brain_sentiment = 'BULLISH' if opp.trap_score < 30 else 'BEARISH' if opp.trap_score > 60 else 'NEUTRAL'

        # Decision
        if opp.trap_score < 20 and opp.streak_years > 10:
            opp.brain_decision = 'STRONG BUY'
        elif opp.trap_score < 30:
            opp.brain_decision = 'BUY'
        elif opp.trap_score < 50:
            opp.brain_decision = 'HOLD'
        elif opp.trap_score < 70:
            opp.brain_decision = 'MONITOR'
        else:
            opp.brain_decision = 'AVOID'

    # ============================================================
    # CAPTURE STRATEGY
    # ============================================================

    def _calculate_capture(self, opp: DividendOpportunity):
        """Hitung strategi dividend capture."""
        if opp.dividend_amount <= 0:
            return

        # Expected drop = dividend amount (biasanya)
        opp.expected_drop = opp.dividend_amount

        # Net dividend after tax (15% default)
        tax_rate = 0.15
        opp.net_dividend = opp.dividend_amount * (1 - tax_rate)

        # Net profit = net dividend - expected drop
        # (biasanya drop = dividend, jadi net = -tax)
        net = opp.net_dividend - opp.expected_drop

        if opp.current_price > 0:
            opp.net_profit_pct = (net / opp.current_price) * 100

        # Verdict
        if opp.net_profit_pct > 0.1:
            opp.capture_verdict = 'WORTH_IT'
        elif opp.net_profit_pct > -0.5:
            opp.capture_verdict = 'MARGINAL'
        else:
            opp.capture_verdict = 'NOT_WORTH'

    # ============================================================
    # STRATEGY RECOMMENDATION
    # ============================================================

    def _recommend_strategy(self, opp: DividendOpportunity):
        """Rekomendasi strategi final."""
        strategy = 'WAIT'
        reason = ''

        # Trap tinggi → SKIP
        if opp.trap_score >= 70:
            return self._set_strategy(opp, 'SKIP',
                f'Trap score {opp.trap_score}/100 — high risk of dividend cut')
        if opp.trap_score >= 50:
            return self._set_strategy(opp, 'SKIP',
                f'Trap score {opp.trap_score}/100 — risky, monitor only')

        # Timing-based
        if opp.timing_status == 'UPCOMING':
            if 0 < opp.days_to_ex <= 7:
                strategy = 'BUY_BEFORE_EX'
                reason = f'Ex-date in {opp.days_to_ex} days — buy now to capture dividend'
            elif 7 < opp.days_to_ex <= 30:
                strategy = 'WAIT'
                reason = f'Ex-date in {opp.days_to_ex} days — wait closer to ex-date'
            else:
                strategy = 'BUY_NOW'
                reason = f'Ex-date in {opp.days_to_ex} days — good entry for long-term hold'
        elif opp.timing_status == 'TODAY':
            strategy = 'BUY_NOW'
            reason = 'Ex-date today — last chance to capture dividend'
        elif opp.timing_status == 'PAST':
            if opp.days_to_ex > -30:
                strategy = 'WAIT'
                reason = f'Ex-date passed {-opp.days_to_ex} days ago — wait for next cycle'
            else:
                strategy = 'BUY_NOW' if opp.trap_score < 30 else 'WAIT'
                reason = 'Good entry point for long-term dividend investor'
        else:
            strategy = 'BUY_NOW' if opp.trap_score < 30 else 'WAIT'
            reason = 'No ex-date info — evaluate based on fundamentals'

        # King/Aristocrat bonus
        if (opp.is_king or opp.is_aristocrat) and opp.trap_score < 20:
            if strategy == 'WAIT':
                strategy = 'BUY_NOW'
                reason = f'{opp.streak_years} years of increases — strong long-term hold'

        return self._set_strategy(opp, strategy, reason)

    def _set_strategy(self, opp: DividendOpportunity, strategy: str, reason: str):
        """Set strategy dan reason."""
        opp.strategy = strategy
        opp.strategy_reason = reason
        return opp

# ============================================================
# SHORTCUT
# ============================================================

def analyze_dividend_opportunity(symbol: str, brain_instance=None) -> Dict[str, Any]:
    """Shortcut untuk analisis peluang dividen."""
    db = DividendBrain(brain_instance)
    return asdict(db.analyze_opportunity(symbol))


__all__ = ['DividendBrain', 'DividendOpportunity', 'analyze_dividend_opportunity']
