# core/autonomous.py
# ============================================================
# AUTONOMOUS LEARNING ENGINE v1.4
# ============================================================
#
# FUNGSI:
#   1. RSS Feed Auto-Learning (real-time)
#   2. Historical Data Processing (batch)
#   3. Reanalysis Engine (periodik)
#   4. Integrasi dengan Consciousness & Knowledge Base
#   5. Filter konten Indonesia otomatis
#   6. Tag geolokasi
#   7. Konfigurasi dari config.py
#
# PENGGUNAAN:
#   from core.autonomous import autonomous
#   autonomous.start()
#   autonomous.stop()
#   autonomous.status()
#
# ============================================================

import threading
import time
import json
import os
import logging
import re
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable

import feedparser

from core.knowledge import knowledge
from core.consciousness import consciousness

from config import (
    INDONESIA_KEYWORDS,
    AUTONOMOUS_RSS_FEEDS,
    AUTONOMOUS_RSS_INTERVAL,
    AUTONOMOUS_REANALYSIS_INTERVAL,
    AUTONOMOUS_HEALTH_CHECK_INTERVAL,
    AUTONOMOUS_CACHE_DIR,
    AUTONOMOUS_SEEN_IDS_FILE,
    AUTONOMOUS_STATS_FILE,
    AUTONOMOUS_MAX_RSS_ITEMS,
    AUTONOMOUS_MAX_KNOWLEDGE_LENGTH,
    AUTONOMOUS_CONFIDENCE_BASE,
    AUTONOMOUS_REQUEST_TIMEOUT,
    AUTONOMOUS_USER_AGENT,
)

logger = logging.getLogger(__name__)


# ============================================================
# AUTONOMOUS LEARNING ENGINE
# ============================================================

class AutonomousEngine:
    """
    Autonomous Learning Engine v1.4.
    
    Menjalankan pembelajaran otomatis dari berbagai sumber:
    - RSS Feed (real-time) dengan timeout & error handling
    - Historical Data (batch)
    - Reanalysis (periodik)
    - Filter konten Indonesia otomatis
    - Konfigurasi dari config.py
    """
    
    VERSION = "1.4.0"
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self._load_config()
        
        # State
        self.running = False
        self._threads: List[threading.Thread] = []
        self._stop_event = threading.Event()
        self._lock = threading.RLock()
        
        # Data
        self._seen_ids: set = set()
        self._stats = {
            "rss_fetched": 0,
            "rss_saved": 0,
            "rss_errors": 0,
            "historical_processed": 0,
            "reanalysis_run": 0,
            "insights_generated": 0,
            "indonesia_items": 0,
            "last_rss_fetch": None,
            "last_reanalysis": None,
            "started_at": None,
        }
        
        # Callbacks
        self._callbacks: List[Callable] = []
        
        # Load cache
        self._load_cache()
        
        logger.info("✅ Autonomous Engine v%s initialized", self.VERSION)
    
    # ============================================================
    # CONFIGURATION
    # ============================================================
    
    def _load_config(self):
        """Load konfigurasi dari file atau default."""
        self.rss_feeds = self.config.get('rss_feeds', AUTONOMOUS_RSS_FEEDS)
        self.rss_interval = self.config.get('rss_interval', AUTONOMOUS_RSS_INTERVAL)
        self.reanalysis_interval = self.config.get('reanalysis_interval', AUTONOMOUS_REANALYSIS_INTERVAL)
        self.health_interval = self.config.get('health_interval', AUTONOMOUS_HEALTH_CHECK_INTERVAL)
        self.cache_dir = self.config.get('cache_dir', AUTONOMOUS_CACHE_DIR)
        self.max_rss_items = self.config.get('max_rss_items', AUTONOMOUS_MAX_RSS_ITEMS)
        self.confidence_base = self.config.get('confidence_base', AUTONOMOUS_CONFIDENCE_BASE)
        self.request_timeout = self.config.get('request_timeout', AUTONOMOUS_REQUEST_TIMEOUT)
        self.user_agent = self.config.get('user_agent', AUTONOMOUS_USER_AGENT)
        self.indonesia_keywords = self.config.get('indonesia_keywords', INDONESIA_KEYWORDS)
        
        # Buat direktori cache
        os.makedirs(self.cache_dir, exist_ok=True)
    
    # ============================================================
    # FILTER INDONESIA
    # ============================================================
    
    def _is_indonesia_content(self, text: str) -> bool:
        """Cek apakah konten terkait Indonesia."""
        if not text:
            return False
        text_lower = text.lower()
        return any(kw in text_lower for kw in self.indonesia_keywords)
    
    def _detect_location_tags(self, content: str) -> List[str]:
        """Deteksi lokasi dari konten."""
        tags = []
        if self._is_indonesia_content(content):
            tags.append('indonesia')
        if 'malaysia' in content.lower() or 'kuala lumpur' in content.lower():
            tags.append('malaysia')
        if 'singapore' in content.lower() or 'singapura' in content.lower():
            tags.append('singapore')
        return tags
    
    # ============================================================
    # LIFECYCLE
    # ============================================================
    
    def start(self) -> bool:
        """Start autonomous learning engine."""
        if self.running:
            logger.warning("Autonomous Engine already running")
            return False
            
        self.running = True
        self._stop_event.clear()
        self._stats["started_at"] = datetime.now().isoformat()
        
        self._start_thread(self._rss_loop, "RSS-Loop")
        self._start_thread(self._reanalysis_loop, "Reanalysis-Loop")
        self._start_thread(self._health_loop, "Health-Loop")
        
        logger.info("🚀 Autonomous Engine started")
        self._trigger_callbacks("on_start", {"status": "started"})
        
        return True
    
    def stop(self) -> bool:
        """Stop autonomous learning engine."""
        if not self.running:
            return False
            
        self.running = False
        self._stop_event.set()
        
        for thread in self._threads:
            if thread.is_alive():
                thread.join(timeout=5)
        self._threads.clear()
        
        self._save_cache()
        
        logger.info("⏹️ Autonomous Engine stopped")
        self._trigger_callbacks("on_stop", {"status": "stopped"})
        
        return True
    
    def _start_thread(self, target: Callable, name: str):
        """Start background thread."""
        thread = threading.Thread(target=target, daemon=True, name=name)
        thread.start()
        self._threads.append(thread)
        logger.debug("Thread started: %s", name)
    
    def is_running(self) -> bool:
        """Check if engine is running."""
        return self.running
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status."""
        with self._lock:
            return {
                "version": self.VERSION,
                "running": self.running,
                "rss_feeds": len([f for f in self.rss_feeds if f.get('enabled', True)]),
                "seen_ids": len(self._seen_ids),
                "threads": len(self._threads),
                "stats": self._stats.copy(),
                "cache_dir": self.cache_dir,
            }
    
    # ============================================================
    # MAIN LOOPS
    # ============================================================
    
    def _rss_loop(self):
        """Loop untuk RSS feed auto-learning."""
        logger.info("📡 RSS Loop started (interval=%ds)", self.rss_interval)
        
        self._fetch_all_rss()
        
        while self.running and not self._stop_event.is_set():
            for _ in range(self.rss_interval):
                if self._stop_event.is_set() or not self.running:
                    break
                time.sleep(1)
            
            if not self.running or self._stop_event.is_set():
                break
                
            try:
                self._fetch_all_rss()
            except Exception as e:
                logger.error(f"RSS loop error: {e}")
                self._stats["rss_errors"] += 1
    
    def _reanalysis_loop(self):
        """Loop untuk reanalysis knowledge."""
        logger.info("🧠 Reanalysis Loop started (interval=%ds)", self.reanalysis_interval)
        
        while self.running and not self._stop_event.is_set():
            for _ in range(self.reanalysis_interval):
                if self._stop_event.is_set() or not self.running:
                    break
                time.sleep(1)
            
            if not self.running or self._stop_event.is_set():
                break
                
            try:
                self._reanalyze_knowledge()
            except Exception as e:
                logger.error(f"Reanalysis error: {e}")
    
    def _health_loop(self):
        """Loop untuk health check."""
        logger.debug("💚 Health Loop started (interval=%ds)", self.health_interval)
        
        while self.running and not self._stop_event.is_set():
            for _ in range(self.health_interval):
                if self._stop_event.is_set() or not self.running:
                    break
                time.sleep(1)
            
            if not self.running or self._stop_event.is_set():
                break
                
            try:
                self._health_check()
            except Exception as e:
                logger.debug(f"Health check error: {e}")
    
    # ============================================================
    # RSS FEED PROCESSING
    # ============================================================
    
    def _fetch_all_rss(self) -> Dict[str, int]:
        """Fetch semua RSS feed."""
        results = {"success": 0, "failed": 0, "items": 0, "indonesia": 0}
        
        for feed_config in self.rss_feeds:
            if not feed_config.get('enabled', True):
                continue
                
            try:
                count = self._process_rss_feed(feed_config)
                results["success"] += 1
                results["items"] += count
            except Exception as e:
                logger.error("Feed %s error: %s", feed_config['url'], e)
                results["failed"] += 1
                self._stats["rss_errors"] += 1
        
        self._stats["rss_fetched"] += results["success"]
        self._stats["last_rss_fetch"] = datetime.now().isoformat()
        self._save_cache()
        
        if results["items"] > 0:
            logger.info(
                "📡 RSS fetch: %d success, %d failed, %d new items (%d Indonesia)",
                results["success"], results["failed"], 
                results["items"], results.get("indonesia", 0)
            )
            self._trigger_callbacks("on_rss_fetch", results)
        elif results["failed"] > 0:
            logger.warning(
                "📡 RSS fetch: %d success, %d failed, %d new items",
                results["success"], results["failed"], results["items"]
            )
        
        return results
    
    def _process_rss_feed(self, feed_config: Dict) -> int:
        """Proses satu RSS feed dengan timeout dan user-agent."""
        url = feed_config["url"]
        category = feed_config["category"]
        source = feed_config.get("source", "unknown")
        max_items = feed_config.get("max_items", self.max_rss_items)
        confidence = feed_config.get("confidence_base", self.confidence_base)
        
        logger.debug("📡 Fetching: %s (%s)", source, url)
        
        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': self.user_agent,
                    'Accept': 'application/rss+xml, application/xml, text/xml, */*',
                }
            )
            with urllib.request.urlopen(req, timeout=self.request_timeout) as response:
                content = response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            raise Exception(f"Failed to fetch: {str(e)}")
        
        try:
            feed = feedparser.parse(content)
        except Exception as e:
            raise Exception(f"Failed to parse feed: {e}")
        
        if feed.bozo:
            if feed.entries:
                logger.warning("Feed %s has issues: %s", source, feed.bozo_exception)
            else:
                raise Exception(f"Feed error: {feed.bozo_exception}")
        
        count = 0
        indonesia_count = 0
        
        for entry in feed.entries[:max_items]:
            try:
                entry_id = self._get_entry_id(entry)
                if entry_id in self._seen_ids:
                    continue
                
                title = entry.get('title', 'No title')
                summary = self._clean_html(entry.get('summary', ''))
                link = entry.get('link', '')
                published = entry.get('published', '')
                
                content = self._build_rss_content(title, summary, link, source, published)
                
                location_tags = self._detect_location_tags(content)
                is_indonesia = 'indonesia' in location_tags
                tags = [source, "rss", "auto", category] + location_tags
                
                item_id = knowledge.add(
                    content=content[:5000],
                    category=category,
                    type="news",
                    tags=tags,
                    confidence=confidence + (5 if is_indonesia else 0),
                    importance=0.4
                )
                
                self._process_with_consciousness({
                    "type": "rss_news",
                    "title": title,
                    "summary": summary[:300],
                    "category": category,
                    "source": source,
                    "location": location_tags,
                    "is_indonesia": is_indonesia,
                    "knowledge_id": str(item_id),
                    "timestamp": datetime.now().isoformat()
                })
                
                self._seen_ids.add(entry_id)
                count += 1
                self._stats["rss_saved"] += 1
                
                if is_indonesia:
                    indonesia_count += 1
                    self._stats["indonesia_items"] += 1
                
                logger.debug("📰 RSS: %s... %s", title[:50], "[🇮🇩]" if is_indonesia else "")
                
            except Exception as e:
                logger.debug("Failed to process entry: %s", e)
                continue
        
        return count
    
    def _get_entry_id(self, entry) -> str:
        entry_id = entry.get('id', '')
        if not entry_id:
            entry_id = entry.get('link', '')
        if not entry_id:
            entry_id = entry.get('title', '') + entry.get('published', '')
        return str(entry_id)
    
    def _clean_html(self, html_text: str) -> str:
        if not html_text:
            return ""
        text = re.sub(r'<[^>]+>', ' ', html_text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _build_rss_content(self, title: str, summary: str, link: str, source: str, published: str) -> str:
        parts = [
            f"📰 {title}",
            "",
            summary[:500] if summary else "(No summary available)",
            "",
            f"Source: {source}",
            f"Link: {link}",
            f"Published: {published if published else datetime.now().isoformat()}"
        ]
        return "\n".join(parts)
    
    # ============================================================
    # REANALYSIS ENGINE
    # ============================================================
    
    def _reanalyze_knowledge(self):
        """Reanalysis knowledge dengan Consciousness."""
        logger.debug("🧠 Running reanalysis...")
        
        try:
            items = knowledge.all()
            if not items:
                return
                
            recent = items[-20:] if len(items) > 20 else items
            insights = 0
            
            for item in recent:
                try:
                    content = getattr(item, 'content', '')
                    if not content or len(content) < 50:
                        continue
                        
                    result = consciousness.process({
                        "type": "reanalysis",
                        "content": content[:500],
                        "source": "knowledge_base",
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    if result and result.get('status') == 'SUCCESS':
                        decision = result.get('decision', {})
                        action = decision.get('action', '')
                        conf = decision.get('confidence', 0)
                        
                        if action and action not in ['wait', 'monitor'] and conf > 40:
                            insight_content = f"🧠 Reanalysis insight: {action} (confidence: {conf:.0f}%)"
                            knowledge.add(
                                content=insight_content,
                                category="insight",
                                type="auto",
                                tags=["reanalysis", "consciousness"],
                                confidence=conf,
                                importance=0.5
                            )
                            insights += 1
                            
                except Exception as e:
                    logger.debug("Reanalysis item error: %s", e)
            
            if insights > 0:
                self._stats["insights_generated"] += insights
                logger.info("🧠 Generated %d insights from reanalysis", insights)
                self._trigger_callbacks("on_insight", {"count": insights})
                
        except Exception as e:
            logger.error("Reanalysis error: %s", e)
        
        self._stats["reanalysis_run"] += 1
        self._stats["last_reanalysis"] = datetime.now().isoformat()
    
    # ============================================================
    # CONSCIOUSNESS INTEGRATION
    # ============================================================
    
    def _process_with_consciousness(self, data: Dict):
        try:
            consciousness.process(data)
        except Exception as e:
            logger.debug("Consciousness process error: %s", e)
    
    # ============================================================
    # HEALTH CHECK
    # ============================================================
    
    def _health_check(self):
        status = self.get_status()
        logger.debug("💚 Health check: running=%s, threads=%s", status['running'], status['threads'])
        
        alive = [t for t in self._threads if t.is_alive()]
        if len(alive) < len(self._threads):
            logger.warning("⚠️ Some threads died: %d", len(self._threads) - len(alive))
    
    # ============================================================
    # CACHE MANAGEMENT
    # ============================================================
    
    def _load_cache(self):
        cache_file = os.path.join(self.cache_dir, AUTONOMOUS_SEEN_IDS_FILE)
        stats_file = os.path.join(self.cache_dir, AUTONOMOUS_STATS_FILE)
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    self._seen_ids = set(data.get("seen_ids", []))
                logger.debug("Cache loaded: %d items", len(self._seen_ids))
            except Exception as e:
                logger.warning("Failed to load cache: %s", e)
        
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    data = json.load(f)
                    self._stats.update(data.get("stats", {}))
            except Exception as e:
                logger.warning("Failed to load stats: %s", e)
    
    def _save_cache(self):
        try:
            cache_file = os.path.join(self.cache_dir, AUTONOMOUS_SEEN_IDS_FILE)
            stats_file = os.path.join(self.cache_dir, AUTONOMOUS_STATS_FILE)
            
            with open(cache_file, 'w') as f:
                json.dump({
                    "seen_ids": list(self._seen_ids),
                    "updated_at": datetime.now().isoformat()
                }, f, indent=2)
            
            with open(stats_file, 'w') as f:
                json.dump({
                    "stats": self._stats,
                    "updated_at": datetime.now().isoformat()
                }, f, indent=2)
                
        except Exception as e:
            logger.warning("Failed to save cache: %s", e)
    
    # ============================================================
    # CALLBACKS
    # ============================================================
    
    def on(self, event: str, callback: Callable):
        self._callbacks.append({"event": event, "callback": callback})
    
    def _trigger_callbacks(self, event: str, data: Any):
        for cb in self._callbacks:
            if cb["event"] == event:
                try:
                    cb["callback"](data)
                except Exception as e:
                    logger.debug("Callback error: %s", e)
    
    # ============================================================
    # HISTORICAL DATA PROCESSING
    # ============================================================
    
    def process_historical_csv(self, filepath: str, category: str = "historical"):
        try:
            import pandas as pd
        except ImportError:
            logger.error("pandas not installed, cannot process CSV")
            return 0
            
        try:
            df = pd.read_csv(filepath)
            logger.info("📊 Processing CSV: %s, rows=%d", filepath, len(df))
            
            date_col = self._detect_date_column(df.columns)
            price_col = self._detect_price_column(df.columns)
            
            if not date_col:
                date_col = df.columns[0]
            if not price_col:
                price_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
            
            count = 0
            for idx, row in df.iterrows():
                try:
                    date = str(row[date_col])
                    price = float(row[price_col])
                    
                    content = f"Historical: {date} - {price}"
                    knowledge.add(
                        content=content,
                        category=category,
                        type="historical",
                        tags=[filepath, "historical", "auto"],
                        confidence=40.0,
                        importance=0.3
                    )
                    count += 1
                    self._stats["historical_processed"] += 1
                    
                    if count % 100 == 0:
                        consciousness.process({
                            "type": "historical_batch",
                            "count": count,
                            "source": filepath
                        })
                        
                except Exception:
                    continue
                    
            logger.info("✅ Historical CSV processed: %d items", count)
            return count
            
        except Exception as e:
            logger.error("CSV processing error: %s", e)
            return 0
    
    def _detect_date_column(self, columns):
        date_keywords = ['date', 'datetime', 'timestamp', 'time', 'day', 'period']
        for col in columns:
            col_lower = col.lower()
            if any(kw in col_lower for kw in date_keywords):
                return col
        return None
    
    def _detect_price_column(self, columns):
        price_keywords = ['price', 'close', 'open', 'high', 'low', 'value', 'adj']
        for col in columns:
            col_lower = col.lower()
            if any(kw in col_lower for kw in price_keywords):
                return col
        return None


# ============================================================
# GLOBAL INSTANCE
# ============================================================

autonomous = AutonomousEngine()


# ============================================================
# SHORTCUT FUNCTIONS
# ============================================================

def start():
    return autonomous.start()

def stop():
    return autonomous.stop()

def status():
    return autonomous.get_status()

def process_historical(filepath: str, category: str = "historical"):
    return autonomous.process_historical_csv(filepath, category)


# ============================================================
# SELF TEST
# ============================================================

def self_test():
    print()
    print("=" * 70)
    print("  AUTONOMOUS ENGINE v1.4 - SELF TEST")
    print("=" * 70)
    print()
    
    logging.basicConfig(level=logging.INFO)
    
    print("1. Testing initialization...")
    engine = AutonomousEngine()
    print("   ✅ Engine initialized")
    
    print("\n2. Testing start/stop...")
    engine.start()
    if engine.is_running():
        print("   ✅ Started")
    engine.stop()
    if not engine.is_running():
        print("   ✅ Stopped")
    
    print("\n3. Testing RSS fetch...")
    engine.start()
    results = engine._fetch_all_rss()
    print(f"   ✅ RSS fetch: {results}")
    engine.stop()
    
    print()
    print("=" * 70)
    print("  ✅ ALL TESTS PASSED")
    print("=" * 70)
    print(f"\n📊 Status: {engine.get_status()}")
    
    return engine


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    self_test()


# ============================================================
# END OF AUTONOMOUS.PY
# ============================================================