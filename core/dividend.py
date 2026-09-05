# core/dividend.py
# DIVIDEND HUNTER MODULE
# Cognitive Mirror Engine - Dividend Tracking & Screening
# 
# Fitur:
# - Auto-fetch data dividen dari Nasdaq API
# - Screening berdasarkan kriteria
# - Alert ex-date mendekat
# - Integrasi dengan Telegram

import os
import json
import logging
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)

# ============================================================
# CONFIGURATION
# ============================================================

NASDAQ_DIVIDEND_API = os.getenv("NASDAQ_DIVIDEND_API", "https://api.nasdaq.com/api/calendar/dividends")
MIN_DIVIDEND = float(os.getenv("MIN_DIVIDEND", "0.10"))
ALERT_DAYS_BEFORE = int(os.getenv("ALERT_DAYS_BEFORE", "3"))

# ============================================================
# DIVIDEND MODULE
# ============================================================

class DividendModule:
    """
    Dividend Hunter Module - Cari, Lacak, dan Screening Dividen.
    Terintegrasi dengan Cognitive Mirror Engine.
    """

    def __init__(self):
        self.df = pd.DataFrame()
        self.alerts = []
        self.last_update = None
        self._cache = {}
        self._cache_time = {}

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
                dividends = data.get('data', {}).get('dividends', [])

                records = []
                for item in dividends:
                    records.append({
                        'symbol': item.get('symbol', ''),
                        'name': item.get('name', ''),
                        'dividend': float(item.get('dividend', 0)),
                        'ex_date': item.get('exDate', ''),
                        'pay_date': item.get('payDate', ''),
                        'sector': item.get('sector', 'Unknown'),
                        'frequency': item.get('frequency', 'Quarterly'),
                        'type': item.get('type', 'Cash'),
                    })

                self.df = pd.DataFrame(records)
                self.last_update = datetime.now()
                self._set_cache(cache_key, self.df)

                logger.info(f"✅ Found {len(self.df)} dividends for {date}")
                return self.df

            else:
                logger.warning(f"⚠️ API error {response.status_code}, using fallback data")
                return self._fallback_data(date)

        except Exception as e:
            logger.error(f"❌ Fetch error: {e}, using fallback data")
            return self._fallback_data(date)

    def _fallback_data(self, date: str) -> pd.DataFrame:
        """Fallback data ketika API gagal."""
        fallback = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.', 'dividend': 0.24, 'sector': 'Technology'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'dividend': 0.75, 'sector': 'Technology'},
            {'symbol': 'JPM', 'name': 'JPMorgan Chase', 'dividend': 1.00, 'sector': 'Financial'},
            {'symbol': 'PG', 'name': 'Procter & Gamble', 'dividend': 0.94, 'sector': 'Consumer'},
            {'symbol': 'JNJ', 'name': 'Johnson & Johnson', 'dividend': 1.19, 'sector': 'Healthcare'},
            {'symbol': 'XOM', 'name': 'Exxon Mobil', 'dividend': 0.95, 'sector': 'Energy'},
            {'symbol': 'KO', 'name': 'Coca-Cola Co.', 'dividend': 0.46, 'sector': 'Consumer'},
            {'symbol': 'VTI', 'name': 'Vanguard Total Stock', 'dividend': 0.95, 'sector': 'ETF'},
            {'symbol': 'DOX', 'name': 'Amdocs Ltd', 'dividend': 0.45, 'sector': 'Technology'},
            {'symbol': 'PFE', 'name': 'Pfizer Inc.', 'dividend': 0.42, 'sector': 'Healthcare'},
            {'symbol': 'VZ', 'name': 'Verizon', 'dividend': 0.67, 'sector': 'Telecom'},
            {'symbol': 'T', 'name': 'AT&T', 'dividend': 0.52, 'sector': 'Telecom'},
        ]

        records = []
        for item in fallback:
            records.append({
                'symbol': item['symbol'],
                'name': item['name'],
                'dividend': item['dividend'],
                'ex_date': date,
                'pay_date': (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=15)).strftime("%Y-%m-%d"),
                'sector': item['sector'],
                'frequency': 'Quarterly',
                'type': 'Cash',
            })

        self.df = pd.DataFrame(records)
        self.last_update = datetime.now()
        return self.df

    def _is_cache_valid(self, key: str) -> bool:
        if key not in self._cache_time:
            return False
        return (datetime.now() - self._cache_time[key]).total_seconds() < 3600

    def _set_cache(self, key: str, value: Any) -> None:
        self._cache[key] = value
        self._cache_time[key] = datetime.now()

    # ============================================================
    # SCREENING & FILTER
    # ============================================================

    def screen(
        self,
        min_dividend: float = None,
        sectors: List[str] = None,
        exclude_etf: bool = True,
        max_dividend: float = None,
    ) -> pd.DataFrame:
        """
        Screening dividen berdasarkan kriteria.

        Args:
            min_dividend: Minimum dividen per share
            sectors: Hanya sektor tertentu
            exclude_etf: Exclude ETF
            max_dividend: Maksimum dividen per share

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

        if sectors:
            result = result[result['sector'].isin(sectors)]

        if exclude_etf and 'type' in result.columns:
            result = result[~result['type'].str.contains('ETF|Preferred', case=False, na=False)]

        return result.sort_values('dividend', ascending=False)

    def get_top(self, n: int = 10) -> pd.DataFrame:
        """Dapatkan N dividen tertinggi."""
        if self.df.empty:
            return pd.DataFrame()
        return self.df.nlargest(n, 'dividend')

    def get_upcoming(self, days: int = 7) -> pd.DataFrame:
        """Dapatkan dividen dalam X hari ke depan."""
        if self.df.empty or 'ex_date' not in self.df.columns:
            return pd.DataFrame()

        self.df['ex_date'] = pd.to_datetime(self.df['ex_date'])
        today = datetime.now().normalize()
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

    # ============================================================
    # ALERT SYSTEM
    # ============================================================

    def check_alerts(self, days_before: int = None) -> List[Dict]:
        """
        Cek alert untuk ex-date mendekat.

        Args:
            days_before: Jumlah hari sebelum ex-date

        Returns:
            List of alert dictionaries
        """
        if days_before is None:
            days_before = ALERT_DAYS_BEFORE

        upcoming = self.get_upcoming(days_before)

        if upcoming.empty:
            self.alerts = []
            return []

        self.alerts = []
        for _, row in upcoming.iterrows():
            days = row.get('days_until', 0)
            alert = {
                'symbol': row.get('symbol', ''),
                'name': row.get('name', ''),
                'dividend': row.get('dividend', 0),
                'ex_date': row['ex_date'].strftime('%Y-%m-%d'),
                'pay_date': row.get('pay_date', ''),
                'days_until': days,
                'sector': row.get('sector', 'Unknown'),
                'priority': 'HIGH' if days <= 2 else 'MEDIUM' if days <= 5 else 'LOW',
            }
            self.alerts.append(alert)

        return self.alerts

    def get_alert_summary(self) -> str:
        """Dapatkan ringkasan alert dalam format teks."""
        if not self.alerts:
            return "📊 No upcoming dividends found."

        summary = f"📊 DIVIDEND ALERT ({len(self.alerts)} upcoming)\n"
        summary += "=" * 40 + "\n"

        for alert in self.alerts:
            icon = "🔴" if alert['priority'] == 'HIGH' else "🟡" if alert['priority'] == 'MEDIUM' else "🔵"
            summary += (
                f"{icon} {alert['symbol']} - "
                f"${alert['dividend']:.2f}, "
                f"Ex-Date: {alert['ex_date']} "
                f"({alert['days_until']} days)\n"
            )

        return summary

    def send_telegram_alert(self) -> bool:
        """Kirim alert ke Telegram."""
        try:
            from core.telegram import send_message
        except ImportError:
            logger.warning("Telegram module not available")
            return False

        if not self.alerts:
            return False

        message = self.get_alert_summary()
        return send_message(message)

    # ============================================================
    # STATISTICS
    # ============================================================

    def get_statistics(self) -> Dict[str, Any]:
        """Dapatkan statistik dividen."""
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
            }

        return {
            'total': len(self.df),
            'avg_dividend': self.df['dividend'].mean(),
            'max_dividend': self.df['dividend'].max(),
            'min_dividend': self.df['dividend'].min(),
            'total_dividend': self.df['dividend'].sum(),
            'sectors': self.df['sector'].unique().tolist(),
            'unique_symbols': self.df['symbol'].unique().tolist(),
            'last_update': self.last_update,
        }

    # ============================================================
    # EXPORT
    # ============================================================

    def to_json(self, filepath: Path) -> bool:
        """Export data ke JSON."""
        try:
            self.df.to_json(filepath, orient='records', indent=2)
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

    # ============================================================
    # STATIC METHODS
    # ============================================================

    @staticmethod
    def get_help() -> str:
        """Dapatkan bantuan penggunaan."""
        return """
DIVIDEND MODULE - Cognitive Mirror Engine

Fungsi:
  fetch(date=None)           - Ambil data dividen
  screen(min_dividend=0.10)  - Screening dividen
  get_top(n=10)              - Top N dividen tertinggi
  get_upcoming(days=7)       - Dividen dalam X hari
  get_by_sector()            - Group per sektor
  check_alerts(days=3)       - Cek ex-date mendekat
  get_statistics()           - Statistik dividen
  to_json(path)              - Export ke JSON
  to_csv(path)               - Export ke CSV

Contoh:
  from core.dividend import dividend
  df = dividend.fetch()
  top = dividend.get_top(5)
  alerts = dividend.check_alerts()
  print(dividend.get_alert_summary())
"""


# ============================================================
# SINGLETON INSTANCE
# ============================================================

dividend = DividendModule()


# ============================================================
# SHORTCUT FUNCTIONS
# ============================================================

def fetch_dividends(date: str = None) -> pd.DataFrame:
    """Ambil data dividen."""
    return dividend.fetch(date)

def screen_dividends(**kwargs) -> pd.DataFrame:
    """Screening dividen."""
    return dividend.screen(**kwargs)

def check_dividend_alerts(days_before: int = None) -> List[Dict]:
    """Cek alert dividen."""
    return dividend.check_alerts(days_before)


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    'DividendModule',
    'dividend',
    'fetch_dividends',
    'screen_dividends',
    'check_dividend_alerts',
    'NASDAQ_DIVIDEND_API',
    'MIN_DIVIDEND',
    'ALERT_DAYS_BEFORE',
]
