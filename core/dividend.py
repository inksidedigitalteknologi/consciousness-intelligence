# core/dividend.py
# DIVIDEND HUNTER MODULE - COMPREHENSIVE VERSION
# Cognitive Mirror Engine - Advanced Dividend Tracking & Analysis
# 
# Fitur Lengkap:
# - Auto-fetch data dividen dari Nasdaq API
# - Dividend Yield Analysis
# - Dividend Growth Rate
# - Payout Ratio Analysis
# - Multi-Criteria Screening
# - Portfolio Simulation
# - Dividend Calendar
# - Sector Analysis
# - Safety Score
# - Export ke Excel/CSV/JSON

import os
import json
import logging
import requests
import pandas as pd
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

# ============================================================
# CONFIGURATION
# ============================================================

NASDAQ_DIVIDEND_API = os.getenv("NASDAQ_DIVIDEND_API", "https://api.nasdaq.com/api/calendar/dividends")
MIN_DIVIDEND = float(os.getenv("MIN_DIVIDEND", "0.10"))
ALERT_DAYS_BEFORE = int(os.getenv("ALERT_DAYS_BEFORE", "3"))
DIVIDEND_CACHE_TTL = int(os.getenv("DIVIDEND_CACHE_TTL", "3600"))

# ============================================================
# ENUMS & CONSTANTS
# ============================================================

class DividendQuality(Enum):
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    FAIR = "FAIR"
    POOR = "POOR"
    UNKNOWN = "UNKNOWN"

class DividendFrequency(Enum):
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    SEMI_ANNUAL = "Semi-Annual"
    ANNUAL = "Annual"
    UNKNOWN = "Unknown"

# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class DividendAnalysis:
    """Analisis lengkap untuk satu saham."""
    symbol: str
    name: str
    dividend: float
    annual_dividend: float
    ex_date: str
    pay_date: str
    sector: str
    frequency: str
    yield_percent: float = 0.0
    growth_rate: float = 0.0
    payout_ratio: float = 0.0
    safety_score: float = 0.0
    quality: str = "UNKNOWN"
    recommendation: str = "HOLD"
    notes: List[str] = field(default_factory=list)

@dataclass
class PortfolioSimulation:
    """Simulasi portofolio dividen."""
    total_investment: float
    annual_income: float
    monthly_income: float
    yield_on_cost: float
    holdings: List[Dict[str, Any]]
    projections: Dict[str, Any]

# ============================================================
# DIVIDEND MODULE - COMPREHENSIVE
# ============================================================

class DividendModule:
    """
    Dividend Hunter Module - Comprehensive Version.
    Advanced dividend tracking, analysis, and screening.
    """

    def __init__(self):
        self.df = pd.DataFrame()
        self.analysis_df = pd.DataFrame()
        self.alerts = []
        self.last_update = None
        self._cache = {}
        self._cache_time = {}
        self._stock_prices = {}  # For yield calculation
        
        logger.info("💰 Dividend Module v2.0 (Comprehensive) initialized")

    # ============================================================
    # MAIN FETCH
    # ============================================================

    def fetch(self, date: str = None, force: bool = False) -> pd.DataFrame:
        """
        Ambil data dividen dari Nasdaq API.

        Args:
            date: Tanggal dalam format YYYY-MM-DD (default: hari ini)
            force: Force refresh meskipun ada cache

        Returns:
            DataFrame dengan data dividen
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        cache_key = f"dividend_{date}"
        if not force and self._is_cache_valid(cache_key):
            logger.info(f"📊 Using cached dividend data for {date}")
            return self._cache[cache_key]

        logger.info(f"📊 Fetching dividends for {date}...")

        try:
            url = f"{NASDAQ_DIVIDEND_API}?date={date}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json"
            }
            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                data = response.json()
                calendar = data.get('data', {}).get('calendar', {})
                rows = calendar.get('rows', [])
                
                if not rows:
                    logger.warning(f"No rows found for {date}, using fallback")
                    return self._fallback_data(date)
                
                records = []
                for item in rows:
                    symbol = item.get('symbol', '')
                    name = item.get('companyName', '')
                    dividend = float(item.get('dividend_Rate', 0))
                    ex_date_raw = item.get('dividend_Ex_Date', '')
                    pay_date_raw = item.get('payment_Date', '')
                    record_date_raw = item.get('record_Date', '')
                    announcement_date_raw = item.get('announcement_Date', '')
                    annual_dividend = float(item.get('indicated_Annual_Dividend', 0))
                    
                    ex_date = self._parse_date(ex_date_raw)
                    pay_date = self._parse_date(pay_date_raw)
                    record_date = self._parse_date(record_date_raw)
                    announcement_date = self._parse_date(announcement_date_raw)
                    sector = self._guess_sector(symbol, name)
                    frequency = self._guess_frequency(dividend, annual_dividend)
                    
                    records.append({
                        'symbol': symbol,
                        'name': name,
                        'dividend': dividend,
                        'annual_dividend': annual_dividend,
                        'ex_date': ex_date,
                        'pay_date': pay_date,
                        'record_date': record_date,
                        'announcement_date': announcement_date,
                        'sector': sector,
                        'frequency': frequency,
                        'type': 'Cash',
                        'source': 'nasdaq'
                    })
                
                self.df = pd.DataFrame(records)
                self.last_update = datetime.now()
                self._set_cache(cache_key, self.df)
                
                # Run analysis
                self._analyze_all()

                logger.info(f"✅ Found {len(records)} dividends for {date}")
                return self.df

            else:
                logger.warning(f"⚠️ API error {response.status_code}, using fallback data")
                return self._fallback_data(date)

        except Exception as e:
            logger.error(f"❌ Fetch error: {e}, using fallback data")
            return self._fallback_data(date)

    # ============================================================
    # COMPREHENSIVE ANALYSIS
    # ============================================================

    def _analyze_all(self) -> None:
        """Analisis semua data dividen."""
        if self.df.empty:
            return
        
        # Enrich with mock prices (for yield calculation)
        self._enrich_with_prices()
        
        # Calculate metrics
        analysis_records = []
        for _, row in self.df.iterrows():
            analysis = self._analyze_single(row)
            analysis_records.append(analysis.__dict__)
        
        self.analysis_df = pd.DataFrame(analysis_records)
        logger.info(f"📊 Analysis complete: {len(self.analysis_df)} stocks analyzed")

    def _analyze_single(self, row: pd.Series) -> DividendAnalysis:
        """Analisis single stock."""
        symbol = row.get('symbol', '')
        name = row.get('name', '')
        dividend = float(row.get('dividend', 0))
        annual_dividend = float(row.get('annual_dividend', 0))
        ex_date = row.get('ex_date', '')
        pay_date = row.get('pay_date', '')
        sector = row.get('sector', 'Unknown')
        frequency = row.get('frequency', 'Unknown')
        
        # Yield (estimate based on price)
        price = self._get_stock_price(symbol)
        yield_percent = (annual_dividend / price * 100) if price > 0 else 0
        
        # Growth rate (estimate)
        growth_rate = self._estimate_growth_rate(symbol, dividend)
        
        # Payout ratio (estimate)
        payout_ratio = self._estimate_payout_ratio(symbol, annual_dividend)
        
        # Safety score
        safety_score = self._calculate_safety_score(
            symbol, dividend, annual_dividend, yield_percent, payout_ratio
        )
        
        # Quality rating
        quality = self._get_quality_rating(safety_score, yield_percent, growth_rate)
        
        # Recommendation
        recommendation = self._get_recommendation(
            quality, yield_percent, growth_rate, safety_score
        )
        
        # Notes
        notes = self._generate_notes(
            symbol, yield_percent, growth_rate, payout_ratio, safety_score
        )
        
        return DividendAnalysis(
            symbol=symbol,
            name=name,
            dividend=dividend,
            annual_dividend=annual_dividend,
            ex_date=ex_date,
            pay_date=pay_date,
            sector=sector,
            frequency=frequency,
            yield_percent=round(yield_percent, 2),
            growth_rate=round(growth_rate, 2),
            payout_ratio=round(payout_ratio, 2),
            safety_score=round(safety_score, 2),
            quality=quality.value,
            recommendation=recommendation,
            notes=notes
        )

    # ============================================================
    # HELPER METHODS
    # ============================================================

    def _parse_date(self, date_str: str) -> str:
        """Konversi tanggal dari MM/DD/YYYY ke YYYY-MM-DD."""
        if not date_str:
            return ''
        try:
            if '/' in date_str:
                dt = datetime.strptime(date_str, "%m/%d/%Y")
                return dt.strftime("%Y-%m-%d")
            return date_str
        except:
            return date_str

    def _guess_sector(self, symbol: str, name: str) -> str:
        """Perkirakan sektor berdasarkan simbol/nama."""
        name_lower = name.lower() if name else ''
        symbol_upper = symbol.upper() if symbol else ''
        
        tech_keywords = ['tech', 'software', 'semi', 'cloud', 'data', 'digital', 'amd', 'intel', 'nvidia', 'apple', 'microsoft', 'oracle', 'cisco', 'ibm']
        finance_keywords = ['bank', 'financial', 'capital', 'invest', 'trust', 'jpm', 'bac', 'wfc', 'citi', 'goldman', 'morgan']
        healthcare_keywords = ['health', 'pharma', 'biotech', 'med', 'care', 'johnson', 'pfizer', 'merck', 'abbvie', 'amgen']
        consumer_keywords = ['consumer', 'retail', 'food', 'beverage', 'coca', 'pepsi', 'walmart', 'amazon', 'target', 'costco']
        energy_keywords = ['energy', 'oil', 'gas', 'petro', 'exxon', 'chevron', 'shell', 'bp']
        industrial_keywords = ['industrial', 'manufacturing', 'machinery', 'caterpillar', 'honeywell', 'ge', 'boeing']
        
        if any(k in name_lower for k in tech_keywords) or symbol_upper in ['AAPL', 'MSFT', 'NVDA', 'AVGO', 'TXN', 'INTC', 'AMD', 'ORCL', 'CSCO', 'IBM']:
            return 'Technology'
        if any(k in name_lower for k in finance_keywords) or symbol_upper in ['JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'BLK', 'V', 'MA', 'AXP']:
            return 'Financial'
        if any(k in name_lower for k in healthcare_keywords) or symbol_upper in ['JNJ', 'PFE', 'MRK', 'ABBV', 'AMGN', 'UNH', 'CVS', 'GILD']:
            return 'Healthcare'
        if any(k in name_lower for k in consumer_keywords) or symbol_upper in ['PG', 'KO', 'PEP', 'WMT', 'AMZN', 'TGT', 'COST', 'MCD', 'NKE']:
            return 'Consumer'
        if any(k in name_lower for k in energy_keywords) or symbol_upper in ['XOM', 'CVX', 'COP', 'EOG', 'SLB']:
            return 'Energy'
        if any(k in name_lower for k in industrial_keywords) or symbol_upper in ['CAT', 'HON', 'GE', 'BA', 'MMM', 'UNP', 'UPS']:
            return 'Industrial'
        return 'Unknown'

    def _guess_frequency(self, dividend: float, annual_dividend: float) -> str:
        """Perkirakan frekuensi dividen."""
        if annual_dividend <= 0 or dividend <= 0:
            return DividendFrequency.UNKNOWN.value
        
        ratio = annual_dividend / dividend
        if 11.5 <= ratio <= 12.5:
            return DividendFrequency.MONTHLY.value
        elif 3.5 <= ratio <= 4.5:
            return DividendFrequency.QUARTERLY.value
        elif 1.5 <= ratio <= 2.5:
            return DividendFrequency.SEMI_ANNUAL.value
        elif 0.8 <= ratio <= 1.2:
            return DividendFrequency.ANNUAL.value
        return DividendFrequency.UNKNOWN.value

    def _enrich_with_prices(self) -> None:
        """Tambahkan harga saham untuk perhitungan yield."""
        # Use mock prices for now (in real implementation, fetch from API)
        default_prices = {
            'DOX': 85.50, 'CGBD': 18.75, 'CCAP': 14.20, 'DRH': 9.80,
            'JOYY': 45.60, 'LECO': 198.50, 'MDLZ': 72.30, 'RMCO': 12.40,
            'STLD': 75.20, 'STRC': 8.50, 'UMBFO': 24.80, 'VOXR': 6.75,
            'WAFDP': 22.40, 'WTW': 268.50, 'XRX': 14.20, 'YORW': 38.60,
        }
        
        for symbol in self.df['symbol'].unique():
            if symbol not in self._stock_prices:
                self._stock_prices[symbol] = default_prices.get(symbol, 50.0)

    def _get_stock_price(self, symbol: str) -> float:
        """Dapatkan harga saham."""
        return self._stock_prices.get(symbol, 50.0)

    def _estimate_growth_rate(self, symbol: str, current_dividend: float) -> float:
        """Estimasi pertumbuhan dividen (0-15%)."""
        # In real implementation, fetch historical dividends
        # For now, use deterministic values based on symbol
        growth_map = {
            'DOX': 8.5, 'JOYY': 12.0, 'LECO': 10.2, 'WTW': 9.5,
            'MDLZ': 7.8, 'STLD': 11.5, 'CCAP': 6.5, 'CGBD': 5.8
        }
        base = growth_map.get(symbol, 6.0)
        # Add randomness based on dividend amount
        adj = (current_dividend / 0.5) * 2
        return min(15, base + adj)

    def _estimate_payout_ratio(self, symbol: str, annual_dividend: float) -> float:
        """Estimasi payout ratio (0-100%)."""
        # In real implementation, fetch earnings
        base_ratio = {
            'DOX': 35, 'JOYY': 25, 'LECO': 40, 'WTW': 30,
            'MDLZ': 55, 'STLD': 20, 'CCAP': 70, 'CGBD': 65
        }
        base = base_ratio.get(symbol, 50)
        # Adjust based on dividend amount
        adj = (annual_dividend / 2) * 5
        return min(90, max(10, base + adj))

    def _calculate_safety_score(self, symbol: str, dividend: float, annual_dividend: float, yield_percent: float, payout_ratio: float) -> float:
        """Hitung skor keamanan dividen (0-100)."""
        score = 60  # Base
        
        # Yield penalty/reward
        if 2 <= yield_percent <= 6:
            score += 15
        elif yield_percent > 8:
            score -= 10
        elif yield_percent < 1:
            score -= 5
        
        # Payout ratio
        if payout_ratio < 40:
            score += 15
        elif payout_ratio < 60:
            score += 10
        elif payout_ratio < 75:
            score += 5
        else:
            score -= 15
        
        # Dividend amount
        if dividend > 1.0:
            score += 10
        elif dividend > 0.5:
            score += 5
        elif dividend < 0.1:
            score -= 10
        
        # Sector bonus
        if self._guess_sector(symbol, '') in ['Technology', 'Healthcare', 'Consumer']:
            score += 5
        
        return max(0, min(100, score))

    def _get_quality_rating(self, safety_score: float, yield_percent: float, growth_rate: float) -> DividendQuality:
        """Dapatkan rating kualitas dividen."""
        if safety_score >= 80 and yield_percent >= 2 and growth_rate >= 5:
            return DividendQuality.EXCELLENT
        elif safety_score >= 65 and yield_percent >= 1.5:
            return DividendQuality.GOOD
        elif safety_score >= 50:
            return DividendQuality.FAIR
        elif safety_score > 0:
            return DividendQuality.POOR
        return DividendQuality.UNKNOWN

    def _get_recommendation(self, quality: DividendQuality, yield_percent: float, growth_rate: float, safety_score: float) -> str:
        """Dapatkan rekomendasi trading."""
        if quality == DividendQuality.EXCELLENT:
            return "STRONG BUY"
        elif quality == DividendQuality.GOOD:
            if yield_percent > 3:
                return "BUY"
            return "BUY" if growth_rate > 8 else "HOLD"
        elif quality == DividendQuality.FAIR:
            return "HOLD" if yield_percent > 2 else "MONITOR"
        else:
            return "AVOID" if safety_score < 40 else "MONITOR"

    def _generate_notes(self, symbol: str, yield_percent: float, growth_rate: float, payout_ratio: float, safety_score: float) -> List[str]:
        """Generate notes for analysis."""
        notes = []
        
        if safety_score >= 80:
            notes.append("✅ High safety score - very stable dividend")
        elif safety_score >= 65:
            notes.append("🟡 Good safety score - stable dividend")
        elif safety_score >= 50:
            notes.append("⚠️ Moderate safety - monitor closely")
        else:
            notes.append("🔴 Low safety - high risk dividend")
        
        if yield_percent >= 4:
            notes.append(f"💰 High yield: {yield_percent:.2f}%")
        elif yield_percent >= 2:
            notes.append(f"📈 Moderate yield: {yield_percent:.2f}%")
        else:
            notes.append(f"📉 Low yield: {yield_percent:.2f}%")
        
        if growth_rate >= 8:
            notes.append(f"📊 Strong growth: {growth_rate:.2f}%")
        elif growth_rate >= 4:
            notes.append(f"📊 Moderate growth: {growth_rate:.2f}%")
        
        if payout_ratio < 40:
            notes.append(f"✅ Low payout ratio: {payout_ratio:.1f}% (room to grow)")
        elif payout_ratio > 70:
            notes.append(f"⚠️ High payout ratio: {payout_ratio:.1f}% (limited room)")
        
        return notes

    # ============================================================
    # FALLBACK DATA
    # ============================================================

    def _fallback_data(self, date: str) -> pd.DataFrame:
        """Fallback data dengan contoh dividen real."""
        fallback = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.', 'dividend': 0.25, 'sector': 'Technology'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'dividend': 0.75, 'sector': 'Technology'},
            {'symbol': 'NVDA', 'name': 'Nvidia Corp.', 'dividend': 0.04, 'sector': 'Technology'},
            {'symbol': 'AVGO', 'name': 'Broadcom Inc.', 'dividend': 5.25, 'sector': 'Technology'},
            {'symbol': 'JPM', 'name': 'JPMorgan Chase', 'dividend': 1.00, 'sector': 'Financial'},
            {'symbol': 'BAC', 'name': 'Bank of America', 'dividend': 0.24, 'sector': 'Financial'},
            {'symbol': 'PG', 'name': 'Procter & Gamble', 'dividend': 0.94, 'sector': 'Consumer'},
            {'symbol': 'KO', 'name': 'Coca-Cola Co.', 'dividend': 0.48, 'sector': 'Consumer'},
            {'symbol': 'JNJ', 'name': 'Johnson & Johnson', 'dividend': 1.19, 'sector': 'Healthcare'},
            {'symbol': 'PFE', 'name': 'Pfizer Inc.', 'dividend': 0.42, 'sector': 'Healthcare'},
            {'symbol': 'XOM', 'name': 'Exxon Mobil', 'dividend': 0.95, 'sector': 'Energy'},
            {'symbol': 'CVX', 'name': 'Chevron Corp.', 'dividend': 1.63, 'sector': 'Energy'},
            {'symbol': 'CAT', 'name': 'Caterpillar Inc.', 'dividend': 1.30, 'sector': 'Industrial'},
            {'symbol': 'HON', 'name': 'Honeywell Intl.', 'dividend': 1.08, 'sector': 'Industrial'},
            {'symbol': 'VTI', 'name': 'Vanguard Total Stock', 'dividend': 0.95, 'sector': 'ETF'},
            {'symbol': 'SPY', 'name': 'SPDR S&P 500 ETF', 'dividend': 1.80, 'sector': 'ETF'},
        ]

        records = []
        for item in fallback:
            base_date = datetime.strptime(date, "%Y-%m-%d")
            ex_date = base_date + timedelta(days=random.randint(-5, 25))
            pay_date = ex_date + timedelta(days=15)
            
            records.append({
                'symbol': item['symbol'],
                'name': item['name'],
                'dividend': item['dividend'],
                'annual_dividend': item['dividend'] * 4,
                'ex_date': ex_date.strftime("%Y-%m-%d"),
                'pay_date': pay_date.strftime("%Y-%m-%d"),
                'record_date': '',
                'announcement_date': '',
                'sector': item['sector'],
                'frequency': 'Quarterly',
                'type': 'Cash',
                'source': 'fallback'
            })

        self.df = pd.DataFrame(records)
        self.last_update = datetime.now()
        self._analyze_all()
        return self.df

    # ============================================================
    # CACHE
    # ============================================================

    def _is_cache_valid(self, key: str) -> bool:
        if key not in self._cache_time:
            return False
        return (datetime.now() - self._cache_time[key]).total_seconds() < DIVIDEND_CACHE_TTL

    def _set_cache(self, key: str, value: Any) -> None:
        self._cache[key] = value
        self._cache_time[key] = datetime.now()

    # ============================================================
    # SCREENING - MULTI CRITERIA
    # ============================================================

    def screen(
        self,
        min_dividend: float = None,
        max_dividend: float = None,
        min_yield: float = None,
        min_annual_dividend: float = None,
        min_safety_score: float = None,
        sectors: List[str] = None,
        exclude_etf: bool = True,
        min_quality: str = None,
        min_growth_rate: float = None,
    ) -> pd.DataFrame:
        """
        Screening dividen dengan multiple criteria.

        Args:
            min_dividend: Minimum dividend per share
            max_dividend: Maximum dividend per share
            min_yield: Minimum yield %
            min_annual_dividend: Minimum annual dividend
            min_safety_score: Minimum safety score (0-100)
            sectors: List of sectors to include
            exclude_etf: Exclude ETFs
            min_quality: Minimum quality (EXCELLENT, GOOD, FAIR, POOR)
            min_growth_rate: Minimum growth rate %

        Returns:
            DataFrame hasil screening
        """
        if self.df.empty:
            return pd.DataFrame()

        result = self.df.copy()

        if min_dividend:
            result = result[result['dividend'] >= min_dividend]

        if max_dividend:
            result = result[result['dividend'] <= max_dividend]

        if min_annual_dividend:
            result = result[result['annual_dividend'] >= min_annual_dividend]

        if sectors:
            result = result[result['sector'].isin(sectors)]

        if exclude_etf and 'type' in result.columns:
            result = result[~result['type'].str.contains('ETF|Preferred', case=False, na=False)]

        # Additional analysis-based filters
        if not self.analysis_df.empty:
            analysis = self.analysis_df
            
            if min_yield is not None:
                symbols = analysis[analysis['yield_percent'] >= min_yield]['symbol'].tolist()
                result = result[result['symbol'].isin(symbols)]
            
            if min_safety_score is not None:
                symbols = analysis[analysis['safety_score'] >= min_safety_score]['symbol'].tolist()
                result = result[result['symbol'].isin(symbols)]
            
            if min_growth_rate is not None:
                symbols = analysis[analysis['growth_rate'] >= min_growth_rate]['symbol'].tolist()
                result = result[result['symbol'].isin(symbols)]
            
            if min_quality:
                quality_map = {'EXCELLENT': 80, 'GOOD': 65, 'FAIR': 50, 'POOR': 30}
                min_score = quality_map.get(min_quality.upper(), 0)
                symbols = analysis[analysis['safety_score'] >= min_score]['symbol'].tolist()
                result = result[result['symbol'].isin(symbols)]

        return result.sort_values('dividend', ascending=False)

    # ============================================================
    # GET METHODS
    # ============================================================

    def get_top(self, n: int = 10, by: str = 'dividend') -> pd.DataFrame:
        """
        Dapatkan top N berdasarkan kriteria.

        Args:
            n: Number of results
            by: 'dividend', 'yield', 'safety', 'growth'
        """
        if self.df.empty:
            return pd.DataFrame()

        if by == 'dividend':
            return self.df.nlargest(n, 'dividend')
        elif by == 'yield' and not self.analysis_df.empty:
            analysis = self.analysis_df.nlargest(n, 'yield_percent')
            return self.df[self.df['symbol'].isin(analysis['symbol'])]
        elif by == 'safety' and not self.analysis_df.empty:
            analysis = self.analysis_df.nlargest(n, 'safety_score')
            return self.df[self.df['symbol'].isin(analysis['symbol'])]
        elif by == 'growth' and not self.analysis_df.empty:
            analysis = self.analysis_df.nlargest(n, 'growth_rate')
            return self.df[self.df['symbol'].isin(analysis['symbol'])]
        else:
            return self.df.nlargest(n, 'dividend')

    def get_upcoming(self, days: int = 7) -> pd.DataFrame:
        """Dapatkan dividen dalam X hari ke depan."""
        if self.df.empty or 'ex_date' not in self.df.columns:
            return pd.DataFrame()

        self.df['ex_date'] = pd.to_datetime(self.df['ex_date'], errors='coerce')
        self.df = self.df.dropna(subset=['ex_date'])
        
        if self.df.empty:
            return pd.DataFrame()
        
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff = today + timedelta(days=days)

        upcoming = self.df[
            (self.df['ex_date'] >= today) &
            (self.df['ex_date'] <= cutoff)
        ].copy()

        if not upcoming.empty:
            upcoming['days_until'] = (upcoming['ex_date'] - today).dt.days

        return upcoming.sort_values('ex_date')

    def get_by_sector(self) -> Dict[str, pd.DataFrame]:
        """Group dividen per sektor."""
        if self.df.empty or 'sector' not in self.df.columns:
            return {}
        return {sector: group for sector, group in self.df.groupby('sector')}

    def get_sector_summary(self) -> pd.DataFrame:
        """Ringkasan dividen per sektor."""
        if self.df.empty or 'sector' not in self.df.columns:
            return pd.DataFrame()

        summary = self.df.groupby('sector').agg({
            'symbol': 'count',
            'dividend': ['mean', 'sum', 'max']
        }).round(2)

        summary.columns = ['count', 'avg_dividend', 'total_dividend', 'max_dividend']
        return summary.sort_values('total_dividend', ascending=False)

    def get_analysis(self) -> pd.DataFrame:
        """Dapatkan data analisis lengkap."""
        if self.analysis_df.empty:
            self._analyze_all()
        return self.analysis_df

    def get_best_yield(self, n: int = 10) -> pd.DataFrame:
        """Dapatkan saham dengan yield tertinggi."""
        analysis = self.get_analysis()
        if analysis.empty:
            return pd.DataFrame()
        top = analysis.nlargest(n, 'yield_percent')
        return top[['symbol', 'name', 'yield_percent', 'dividend', 'safety_score', 'recommendation']]

    def get_safest(self, n: int = 10) -> pd.DataFrame:
        """Dapatkan saham dengan safety score tertinggi."""
        analysis = self.get_analysis()
        if analysis.empty:
            return pd.DataFrame()
        top = analysis.nlargest(n, 'safety_score')
        return top[['symbol', 'name', 'safety_score', 'yield_percent', 'dividend', 'recommendation']]

    # ============================================================
    # PORTFOLIO SIMULATION
    # ============================================================

    def simulate_portfolio(
        self,
        symbols: List[str],
        investment_per_stock: float = 1000.0,
        reinvest_dividends: bool = True,
        years: int = 5
    ) -> PortfolioSimulation:
        """
        Simulasi portofolio dividen.

        Args:
            symbols: List of stock symbols
            investment_per_stock: Investment per stock
            reinvest_dividends: Reinvest dividends
            years: Projection years

        Returns:
            PortfolioSimulation object
        """
        if self.df.empty:
            self.fetch()
        
        holdings = []
        total_investment = 0
        total_annual_income = 0
        
        for symbol in symbols:
            stock = self.df[self.df['symbol'] == symbol]
            if stock.empty:
                continue
            
            row = stock.iloc[0]
            dividend = float(row.get('dividend', 0))
            annual_dividend = float(row.get('annual_dividend', 0))
            price = self._get_stock_price(symbol)
            shares = investment_per_stock / price if price > 0 else 0
            
            annual_income = shares * annual_dividend
            yield_on_cost = (annual_income / investment_per_stock * 100) if investment_per_stock > 0 else 0
            
            holdings.append({
                'symbol': symbol,
                'name': row.get('name', ''),
                'investment': investment_per_stock,
                'shares': round(shares, 2),
                'price': price,
                'annual_income': round(annual_income, 2),
                'yield_on_cost': round(yield_on_cost, 2),
                'dividend_per_share': dividend,
                'annual_dividend': annual_dividend,
            })
            
            total_investment += investment_per_stock
            total_annual_income += annual_income
        
        # Projections
        projections = {}
        if reinvest_dividends:
            current_value = total_investment
            for year in range(1, years + 1):
                growth = total_annual_income * 0.08  # Assume 8% growth
                current_value += total_annual_income + growth
                projections[f'Year {year}'] = round(current_value, 2)
        else:
            for year in range(1, years + 1):
                projections[f'Year {year}'] = round(total_investment + (total_annual_income * year), 2)
        
        return PortfolioSimulation(
            total_investment=total_investment,
            annual_income=total_annual_income,
            monthly_income=total_annual_income / 12,
            yield_on_cost=(total_annual_income / total_investment * 100) if total_investment > 0 else 0,
            holdings=holdings,
            projections=projections
        )

    # ============================================================
    # ALERT SYSTEM
    # ============================================================

    def check_alerts(self, days_before: int = None) -> List[Dict]:
        """Cek alert untuk ex-date mendekat."""
        if days_before is None:
            days_before = ALERT_DAYS_BEFORE

        upcoming = self.get_upcoming(days_before)

        if upcoming.empty:
            self.alerts = []
            return []

        self.alerts = []
        for _, row in upcoming.iterrows():
            days = row.get('days_until', 0)
            
            ex_date_str = ''
            if pd.notna(row.get('ex_date')):
                if isinstance(row['ex_date'], pd.Timestamp):
                    ex_date_str = row['ex_date'].strftime('%Y-%m-%d')
                else:
                    ex_date_str = str(row['ex_date'])
            
            # Get additional info from analysis
            analysis = self.analysis_df[self.analysis_df['symbol'] == row.get('symbol', '')]
            yield_pct = analysis['yield_percent'].iloc[0] if not analysis.empty else 0
            safety = analysis['safety_score'].iloc[0] if not analysis.empty else 0
            
            alert = {
                'symbol': row.get('symbol', ''),
                'name': row.get('name', ''),
                'dividend': row.get('dividend', 0),
                'annual_dividend': row.get('annual_dividend', 0),
                'ex_date': ex_date_str,
                'pay_date': row.get('pay_date', ''),
                'days_until': int(days) if pd.notna(days) else 0,
                'sector': row.get('sector', 'Unknown'),
                'yield_percent': round(yield_pct, 2),
                'safety_score': round(safety, 2),
                'priority': 'HIGH' if days <= 2 else 'MEDIUM' if days <= 5 else 'LOW',
            }
            self.alerts.append(alert)

        return self.alerts

    def get_alert_summary(self) -> str:
        """Dapatkan ringkasan alert dalam format teks."""
        if not self.alerts:
            return "📊 No upcoming dividends found."

        summary = f"📊 DIVIDEND ALERT ({len(self.alerts)} upcoming)\n"
        summary += "=" * 50 + "\n"

        for alert in self.alerts:
            icon = "🔴" if alert['priority'] == 'HIGH' else "🟡" if alert['priority'] == 'MEDIUM' else "🔵"
            summary += (
                f"{icon} {alert['symbol']} - "
                f"${alert['dividend']:.2f} "
                f"(Yield: {alert['yield_percent']:.1f}%, Safety: {alert['safety_score']:.0f})\n"
                f"   Ex-Date: {alert['ex_date']} "
                f"({alert['days_until']} days) | Pay: {alert['pay_date']}\n"
            )

        return summary

    # ============================================================
    # DIVIDEND CALENDAR
    # ============================================================

    def get_dividend_calendar(self, month: int = None, year: int = None) -> pd.DataFrame:
        """Dapatkan kalender dividen per bulan."""
        if self.df.empty:
            self.fetch()
        
        if self.df.empty or 'ex_date' not in self.df.columns:
            return pd.DataFrame()
        
        df = self.df.copy()
        df['ex_date'] = pd.to_datetime(df['ex_date'], errors='coerce')
        df = df.dropna(subset=['ex_date'])
        
        if month is not None and year is not None:
            df = df[(df['ex_date'].dt.month == month) & (df['ex_date'].dt.year == year)]
        elif month is not None:
            df = df[df['ex_date'].dt.month == month]
        elif year is not None:
            df = df[df['ex_date'].dt.year == year]
        
        # Add day of week
        df['day_of_week'] = df['ex_date'].dt.day_name()
        df['week'] = df['ex_date'].dt.isocalendar().week
        df['month_name'] = df['ex_date'].dt.month_name()
        
        return df.sort_values('ex_date')

    def get_dividend_calendar_summary(self) -> pd.DataFrame:
        """Ringkasan kalender dividen per bulan."""
        df = self.get_dividend_calendar()
        if df.empty:
            return pd.DataFrame()
        
        summary = df.groupby([df['ex_date'].dt.year, df['ex_date'].dt.month]).agg({
            'symbol': 'count',
            'dividend': ['sum', 'mean']
        }).round(2)
        
        summary.columns = ['total_dividends', 'total_amount', 'avg_dividend']
        summary = summary.reset_index()
        summary['month_year'] = summary['ex_date'].astype(str) + '-' + summary['ex_date'].astype(str)
        
        return summary

    # ============================================================
    # STATISTICS
    # ============================================================

    def get_statistics(self) -> Dict[str, Any]:
        """Dapatkan statistik lengkap."""
        if self.df.empty:
            return {
                'total': 0,
                'avg_dividend': 0,
                'max_dividend': 0,
                'min_dividend': 0,
                'total_dividend': 0,
                'sectors': [],
                'unique_symbols': [],
                'last_update': self.last_update,
                'analysis': {}
            }

        stats = {
            'total': len(self.df),
            'avg_dividend': round(self.df['dividend'].mean(), 4),
            'max_dividend': round(self.df['dividend'].max(), 4),
            'min_dividend': round(self.df['dividend'].min(), 4),
            'total_dividend': round(self.df['dividend'].sum(), 4),
            'sectors': self.df['sector'].unique().tolist() if 'sector' in self.df.columns else [],
            'unique_symbols': self.df['symbol'].unique().tolist() if 'symbol' in self.df.columns else [],
            'last_update': self.last_update,
            'analysis': {}
        }
        
        if not self.analysis_df.empty:
            stats['analysis'] = {
                'avg_yield': round(self.analysis_df['yield_percent'].mean(), 2),
                'max_yield': round(self.analysis_df['yield_percent'].max(), 2),
                'avg_safety': round(self.analysis_df['safety_score'].mean(), 2),
                'avg_growth': round(self.analysis_df['growth_rate'].mean(), 2),
                'quality_distribution': {
                    'EXCELLENT': len(self.analysis_df[self.analysis_df['quality'] == 'EXCELLENT']),
                    'GOOD': len(self.analysis_df[self.analysis_df['quality'] == 'GOOD']),
                    'FAIR': len(self.analysis_df[self.analysis_df['quality'] == 'FAIR']),
                    'POOR': len(self.analysis_df[self.analysis_df['quality'] == 'POOR']),
                },
                'recommendations': {
                    'STRONG BUY': len(self.analysis_df[self.analysis_df['recommendation'] == 'STRONG BUY']),
                    'BUY': len(self.analysis_df[self.analysis_df['recommendation'] == 'BUY']),
                    'HOLD': len(self.analysis_df[self.analysis_df['recommendation'] == 'HOLD']),
                    'MONITOR': len(self.analysis_df[self.analysis_df['recommendation'] == 'MONITOR']),
                    'AVOID': len(self.analysis_df[self.analysis_df['recommendation'] == 'AVOID']),
                }
            }
        
        return stats

    # ============================================================
    # EXPORT
    # ============================================================

    def to_json(self, filepath: Path) -> bool:
        """Export data ke JSON."""
        try:
            data = {
                'dividends': self.df.to_dict('records'),
                'analysis': self.analysis_df.to_dict('records') if not self.analysis_df.empty else [],
                'stats': self.get_statistics(),
                'last_update': self.last_update.isoformat() if self.last_update else None,
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            logger.info(f"✅ Exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"❌ Export error: {e}")
            return False

    def to_csv(self, filepath: Path) -> bool:
        """Export data ke CSV."""
        try:
            self.df.to_csv(filepath, index=False)
            logger.info(f"✅ Exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"❌ Export error: {e}")
            return False

    def to_excel(self, filepath: Path) -> bool:
        """Export data ke Excel dengan multiple sheets."""
        try:
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                self.df.to_excel(writer, sheet_name='Dividends', index=False)
                if not self.analysis_df.empty:
                    self.analysis_df.to_excel(writer, sheet_name='Analysis', index=False)
                stats = self.get_statistics()
                stats_df = pd.DataFrame([stats])
                stats_df.to_excel(writer, sheet_name='Statistics', index=False)
                
                # Calendar
                calendar = self.get_dividend_calendar()
                if not calendar.empty:
                    calendar.to_excel(writer, sheet_name='Calendar', index=False)
                
                # Sector summary
                sector_summary = self.get_sector_summary()
                if not sector_summary.empty:
                    sector_summary.to_excel(writer, sheet_name='Sector Summary', index=False)
            
            logger.info(f"✅ Exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"❌ Export error: {e}")
            return False

    # ============================================================
    # HELP
    # ============================================================

    @staticmethod
    def get_help() -> str:
        """Dapatkan bantuan penggunaan."""
        return """
DIVIDEND MODULE v2.0 - Comprehensive Version

FUNGSI:
  fetch(date=None)              - Ambil data dividen
  screen(**kwargs)              - Screening multi-criteria
  get_top(n=10, by='dividend')  - Top N (dividend|yield|safety|growth)
  get_upcoming(days=7)          - Dividen dalam X hari
  get_by_sector()               - Group per sektor
  get_sector_summary()          - Ringkasan per sektor
  get_analysis()                - Data analisis lengkap
  get_best_yield(n=10)          - Yield tertinggi
  get_safest(n=10)              - Safety score tertinggi
  get_dividend_calendar()       - Kalender dividen
  simulate_portfolio()          - Simulasi portofolio
  check_alerts(days=3)          - Cek ex-date mendekat
  get_statistics()              - Statistik lengkap
  to_excel(path)                - Export ke Excel (multi-sheet)

CONTOH:
  from core.dividend import dividend
  
  # Fetch data
  df = dividend.fetch('2026-09-30')
  
  # Screen high yield stocks
  screened = dividend.screen(min_yield=3.0, min_safety=70)
  
  # Get top 10 safest dividends
  safest = dividend.get_safest(10)
  
  # Simulate portfolio
  portfolio = dividend.simulate_portfolio(
      symbols=['DOX', 'JOYY', 'LECO'],
      investment_per_stock=5000,
      years=10
  )
  
  # Export to Excel
  dividend.to_excel(Path('dividend_report.xlsx'))
"""


# ============================================================
# SINGLETON INSTANCE
# ============================================================

dividend = DividendModule()


# ============================================================
# SHORTCUT FUNCTIONS
# ============================================================

def fetch_dividends(date: str = None) -> pd.DataFrame:
    return dividend.fetch(date)

def screen_dividends(**kwargs) -> pd.DataFrame:
    return dividend.screen(**kwargs)

def check_dividend_alerts(days_before: int = None) -> List[Dict]:
    return dividend.check_alerts(days_before)

def get_dividend_analysis() -> pd.DataFrame:
    return dividend.get_analysis()


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    'DividendModule',
    'dividend',
    'fetch_dividends',
    'screen_dividends',
    'check_dividend_alerts',
    'get_dividend_analysis',
    'DividendAnalysis',
    'PortfolioSimulation',
    'DividendQuality',
    'DividendFrequency',
]
