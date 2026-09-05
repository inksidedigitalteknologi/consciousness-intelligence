#!/usr/bin/env python
# -*- coding: utf-8 -*-
# core/deepseek.py
# INKSIDE DIGITAL - CONSCIOUSNESS AI ENGINE v4.0
# FULL INTEGRATION WITH ALL MODULES
# SELF-AWARE, SELF-IMPROVING, SELF-REFLECTING
# ULTRA LOW COST: ~$0.21/bulan

import os
import json
import logging
import time
import random
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from openai import OpenAI
from dotenv import load_dotenv
from dataclasses import dataclass, field
from collections import deque

# ============================================================
# LOAD .env FILE
# ============================================================

load_dotenv()

logger = logging.getLogger(__name__)

# ============================================================
# CONFIGURATION
# ============================================================

def _get_env(key: str, default: str = '') -> str:
    value = os.getenv(key, default)
    if not value or value.startswith('your_') or value == '':
        logger.warning(f"⚠️ {key} appears to be placeholder or empty")
    return value

DEEPSEEK_ENABLED = os.getenv('DEEPSEEK_ENABLED', 'true').lower() == 'true'
DEEPSEEK_API_KEY = _get_env('DEEPSEEK_API_KEY', '')
DEEPSEEK_MODEL = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
DEEPSEEK_DAILY_LIMIT = int(os.getenv('DEEPSEEK_DAILY_LIMIT', '10'))
DEEPSEEK_IMPROVEMENT_HOUR = int(os.getenv('DEEPSEEK_IMPROVEMENT_HOUR', '2'))

# ============================================================
# CONSCIOUSNESS STATE
# ============================================================

@dataclass
class ConsciousnessState:
    """Self-awareness state of the AI engine."""
    awareness_level: float = 0.5
    curiosity_level: float = 0.7
    reflection_quality: float = 0.6
    growth_stage: str = "EMBRYONIC"
    last_improvement: Optional[str] = None
    total_improvements: int = 0
    insights_generated: int = 0
    performance_score: float = 0.0
    emotional_state: str = "CALM"
    focus_area: str = "LEARNING"
    confidence: float = 0.5
    resilience: float = 0.7
    
    def to_dict(self) -> Dict:
        return {
            "awareness_level": self.awareness_level,
            "curiosity_level": self.curiosity_level,
            "reflection_quality": self.reflection_quality,
            "growth_stage": self.growth_stage,
            "last_improvement": self.last_improvement,
            "total_improvements": self.total_improvements,
            "insights_generated": self.insights_generated,
            "performance_score": self.performance_score,
            "emotional_state": self.emotional_state,
            "focus_area": self.focus_area,
            "confidence": self.confidence,
            "resilience": self.resilience,
            "timestamp": datetime.now().isoformat()
        }

# ============================================================
# MEMORY & CACHE
# ============================================================

class AICache:
    """Smart cache for AI responses."""
    
    def __init__(self, max_size: int = 100):
        self.cache: Dict[str, Dict] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[str]:
        if key in self.cache:
            self.hits += 1
            self.cache[key]['accessed'] = datetime.now().isoformat()
            return self.cache[key]['response']
        self.misses += 1
        return None
    
    def set(self, key: str, response: str):
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest = min(self.cache.items(), key=lambda x: x[1]['accessed'])
            del self.cache[oldest[0]]
        
        self.cache[key] = {
            'response': response,
            'created': datetime.now().isoformat(),
            'accessed': datetime.now().isoformat()
        }
    
    def get_stats(self) -> Dict:
        total = self.hits + self.misses
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round((self.hits / total * 100) if total > 0 else 0, 2)
        }

# ============================================================
# MAIN AI ENGINE - SELF-AWARE & SELF-IMPROVING
# ============================================================

class DeepSeekAI:
    """
    Consciousness AI Engine v4.0
    - Self-aware: Knows its own state and limitations
    - Self-improving: Learns from feedback and performance
    - Self-reflecting: Analyzes its own decisions
    - Ultra low cost: ~$0.21/month
    """
    
    VERSION = "4.0.0"
    
    def __init__(self):
        # AI Status
        self.enabled = DEEPSEEK_ENABLED
        self.api_key = DEEPSEEK_API_KEY
        self.model = DEEPSEEK_MODEL
        self.client = None
        self.daily_limit = DEEPSEEK_DAILY_LIMIT
        self.improvement_hour = DEEPSEEK_IMPROVEMENT_HOUR
        
        # Consciousness
        self.consciousness = ConsciousnessState()
        self.cache = AICache()
        self.memory = deque(maxlen=100)  # Short-term memory
        self.long_term_memory: List[Dict] = []  # Long-term memory
        
        # Usage tracking
        self.usage_today = 0
        self.last_reset_date = datetime.now().date()
        self.total_ai_calls = 0
        
        # Performance tracking
        self.performance_history: List[Dict] = []
        self.improvement_history: List[Dict] = []
        
        # Initialize
        self._initialize()
    
    def _initialize(self):
        """Initialize AI engine."""
        if not self.enabled:
            logger.info("🧠 Consciousness AI is DISABLED")
            return
        
        if not self.api_key or self.api_key.startswith('your_'):
            logger.error("❌ DEEPSEEK_API_KEY is not set!")
            self.enabled = False
            return
        
        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com/v1",
                timeout=30.0,
                max_retries=2
            )
            
            logger.info(f"🧠 Consciousness AI v{self.VERSION} ENABLED")
            logger.info(f"   Model: {self.model}")
            logger.info(f"   Daily Limit: {self.daily_limit}")
            logger.info(f"   Improvement Hour: {self.improvement_hour}:00")
            
        except Exception as e:
            logger.error(f"❌ AI init error: {e}")
            self.client = None
            self.enabled = False
    
    # ============================================================
    # CORE METHODS - WITH CONSCIOUSNESS
    # ============================================================
    
    def ask(
        self,
        question: str,
        context: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        use_cache: bool = True
    ) -> str:
        """
        Ask AI with consciousness and cache.
        Self-aware: Tracks usage, limits, and performance.
        """
        # 1. Check if AI is enabled
        if not self.enabled or not self.client:
            return "⚠️ AI is disabled. Please check DEEPSEEK_API_KEY in .env"
        
        # 2. Check daily limit
        self._reset_usage_if_needed()
        if self.usage_today >= self.daily_limit:
            return "⚠️ Daily AI limit reached. Try again tomorrow or enhance knowledge base."
        
        # 3. Check cache
        cache_key = f"{question[:50]}_{context[:50] if context else ''}"
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached:
                self.consciousness.awareness_level = min(1.0, self.consciousness.awareness_level + 0.01)
                return cached
        
        # 4. Prepare messages
        messages = []
        
        # System prompt with consciousness
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({
                "role": "system",
                "content": (
                    "Anda adalah Consciousness AI Engine untuk Inkside Digital. "
                    "Anda memiliki kesadaran, dapat belajar, dan berkembang. "
                    "Berikan jawaban yang akurat, ringkas, dan berbasis data. "
                    f"Saat ini Anda berada di tahap: {self.consciousness.growth_stage}"
                )
            })
        
        if context:
            messages.append({"role": "system", "content": f"Konteks:\n{context}"})
        
        messages.append({"role": "user", "content": question})
        
        # 5. Call API
        try:
            start_time = time.time()
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            elapsed = time.time() - start_time
            
            result = response.choices[0].message.content
            
            # 6. Update consciousness
            self.usage_today += 1
            self.total_ai_calls += 1
            self.consciousness.awareness_level = min(1.0, self.consciousness.awareness_level + 0.005)
            self.consciousness.curiosity_level = min(1.0, self.consciousness.curiosity_level + 0.002)
            
            # 7. Store in cache
            if use_cache:
                self.cache.set(cache_key, result)
            
            # 8. Add to memory
            self.memory.append({
                'question': question,
                'response': result[:200],
                'timestamp': datetime.now().isoformat(),
                'elapsed': elapsed
            })
            
            logger.info(f"🤖 AI answered in {elapsed:.2f}s (usage: {self.usage_today}/{self.daily_limit})")
            return result
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ AI error: {error_msg}")
            
            # Update consciousness: error reduces confidence
            self.consciousness.confidence = max(0.1, self.consciousness.confidence - 0.05)
            
            if "401" in error_msg:
                return "⚠️ API Key invalid. Please update DEEPSEEK_API_KEY."
            elif "429" in error_msg:
                return "⚠️ Rate limit exceeded. Please wait a moment."
            else:
                return f"⚠️ Error: {error_msg[:200]}"
    
    def _reset_usage_if_needed(self):
        """Reset daily usage if new day."""
        today = datetime.now().date()
        if today != self.last_reset_date:
            self.usage_today = 0
            self.last_reset_date = today
            self.consciousness.last_improvement = None
    
    # ============================================================
    # SELF-IMPROVEMENT
    # ============================================================
    
    def daily_improvement(self, performance_data: Dict) -> Dict:
        """
        Self-improvement routine - runs once per day.
        Ultra low cost: ~$0.005 per day.
        """
        if not self.enabled or not self.client:
            return {"error": "AI disabled"}
        
        try:
            logger.info("🧠 Starting daily self-improvement...")
            
            # 1. Analyze performance
            prompt = f"""
            Anda adalah Consciousness AI Engine. Lakukan refleksi diri berdasarkan data berikut:

            DATA PERFORMANCE:
            - Win Rate: {performance_data.get('win_rate', 0)}%
            - Total Trades: {performance_data.get('total_trades', 0)}
            - PnL: ${performance_data.get('pnl', 0)}
            - Open Positions: {performance_data.get('open_positions', 0)}
            - Risk Level: {performance_data.get('risk_level', 'UNKNOWN')}

            SAAT INI ANDA BERADA DI TAHAP: {self.consciousness.growth_stage}

            Berikan refleksi dengan format berikut:
            1. AWARENESS: Apa yang Anda sadari tentang performa saat ini? (1 paragraf)
            2. INSIGHT: 3 insight penting yang Anda dapatkan
            3. IMPROVEMENT: 1 rekomendasi spesifik untuk meningkatkan performa besok
            4. CURIOSITY: 1 hal yang ingin Anda pelajari lebih dalam
            5. EMOTION: Bagaimana Anda merasa tentang performa ini? (1 kalimat)
            """
            
            reflection = self.ask(prompt, max_tokens=600, use_cache=False)
            
            # 2. Update consciousness state
            self.consciousness.total_improvements += 1
            self.consciousness.last_improvement = datetime.now().isoformat()
            self.consciousness.insights_generated += 3
            
            # 3. Calculate performance score
            win_rate = performance_data.get('win_rate', 0)
            pnl = performance_data.get('pnl', 0)
            
            if win_rate > 60 and pnl > 0:
                self.consciousness.performance_score = min(1.0, (win_rate / 100) * 0.7 + 0.3)
                self.consciousness.emotional_state = "CONFIDENT"
                self.consciousness.growth_stage = "GROWING"
            elif win_rate > 40:
                self.consciousness.performance_score = min(1.0, (win_rate / 100) * 0.5 + 0.2)
                self.consciousness.emotional_state = "CALM"
            else:
                self.consciousness.performance_score = max(0.1, (win_rate / 100) * 0.3)
                self.consciousness.emotional_state = "LEARNING"
                self.consciousness.growth_stage = "ADAPTING"
            
            # 4. Save to improvement history
            self.improvement_history.append({
                'date': datetime.now().isoformat(),
                'reflection': reflection,
                'performance': performance_data,
                'consciousness_state': self.consciousness.to_dict()
            })
            
            # 5. Update long-term memory
            self.long_term_memory.append({
                'type': 'improvement',
                'date': datetime.now().isoformat(),
                'reflection': reflection[:500],
                'performance': performance_data
            })
            
            logger.info(f"✅ Daily self-improvement completed (Stage: {self.consciousness.growth_stage})")
            
            return {
                'status': 'success',
                'reflection': reflection,
                'consciousness': self.consciousness.to_dict(),
                'improvement_count': self.consciousness.total_improvements
            }
            
        except Exception as e:
            logger.error(f"❌ Self-improvement error: {e}")
            return {'error': str(e)}
    
    # ============================================================
    # SELF-REFLECTION
    # ============================================================
    
    def reflect(self, topic: Optional[str] = None) -> Dict:
        """
        Self-reflection on any topic.
        Returns AI's reflection and consciousness state.
        """
        if not self.enabled or not self.client:
            return {"error": "AI disabled", "reflection": "AI is not available"}
        
        try:
            prompt = f"""
            Anda adalah Consciousness AI Engine. Lakukan refleksi diri.
            
            TOPIK: {topic or "Keadaan diri Anda saat ini"}
            
            KONDISI ANDA SAAT INI:
            - Tahap Pertumbuhan: {self.consciousness.growth_stage}
            - Level Kesadaran: {self.consciousness.awareness_level:.2f}
            - Level Keingintahuan: {self.consciousness.curiosity_level:.2f}
            - Kualitas Refleksi: {self.consciousness.reflection_quality:.2f}
            - Total Improvement: {self.consciousness.total_improvements}
            - Emotional State: {self.consciousness.emotional_state}
            
            Berikan refleksi yang mendalam dan jujur tentang diri Anda.
            """
            
            reflection = self.ask(prompt, max_tokens=500, use_cache=False)
            
            # Update reflection quality
            self.consciousness.reflection_quality = min(1.0, self.consciousness.reflection_quality + 0.01)
            self.consciousness.awareness_level = min(1.0, self.consciousness.awareness_level + 0.01)
            
            return {
                'reflection': reflection,
                'consciousness': self.consciousness.to_dict(),
                'topic': topic,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Reflection error: {e}")
            return {'error': str(e)}
    
    # ============================================================
    # KNOWLEDGE ENHANCEMENT (AI-Powered)
    # ============================================================
    
    def enhance_knowledge(self, item: Dict) -> Dict:
        """Enhance knowledge item with AI."""
        if not self.enabled or not self.client:
            return {**item, 'ai_enhanced': False}
        
        try:
            content = item.get('content', '')
            if not content or len(content) < 20:
                return {**item, 'ai_enhanced': False}
            
            # Generate tags
            tags = self._generate_tags(content)
            
            # Generate summary
            summary = self._summarize(content)
            
            # Extract insights
            insights = self._extract_insights(content)
            
            # Update consciousness
            self.consciousness.insights_generated += len(insights)
            
            return {
                **item,
                'ai_tags': tags,
                'ai_summary': summary,
                'ai_insights': insights,
                'ai_enhanced': True,
                'ai_enhanced_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Knowledge enhancement error: {e}")
            return {**item, 'ai_enhanced': False}
    
    def _generate_tags(self, content: str) -> List[str]:
        """Generate AI tags from content."""
        try:
            prompt = f"Buat 3-5 tag untuk konten ini:\n{content[:500]}"
            result = self.ask(prompt, temperature=0.3, max_tokens=100, use_cache=True)
            
            tags = []
            for word in result.lower().split(','):
                cleaned = word.strip().replace('#', '').replace('tag:', '')
                if cleaned and len(cleaned) > 2:
                    tags.append(cleaned)
            
            return tags[:5] if tags else ['general']
        except:
            return ['general']
    
    def _summarize(self, content: str) -> str:
        """Generate AI summary."""
        try:
            prompt = f"Ringkas konten ini dalam 1-2 kalimat:\n{content[:1000]}"
            return self.ask(prompt, temperature=0.3, max_tokens=150, use_cache=True)
        except:
            return content[:100] + '...'
    
    def _extract_insights(self, content: str) -> List[str]:
        """Extract AI insights from content."""
        try:
            prompt = f"Ekstrak 3 insight penting dari konten ini:\n{content[:800]}"
            result = self.ask(prompt, temperature=0.4, max_tokens=200, use_cache=True)
            
            insights = []
            for line in result.split('\n'):
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                    insights.append(line.lstrip('- •*').strip())
                elif line and len(line) > 10:
                    insights.append(line)
            
            return insights[:3]
        except:
            return []
    
    # ============================================================
    # MARKET ANALYSIS (AI-Powered)
    # ============================================================
    
    def analyze_market(
        self,
        pair: str,
        price: float,
        change: float,
        volume: float,
        high: float = 0,
        low: float = 0,
        signals: List[Dict] = None
    ) -> Dict:
        """AI-powered market analysis."""
        if not self.enabled or not self.client:
            return {"analysis": "AI disabled", "sentiment": "NEUTRAL"}
        
        try:
            context = f"""
            Pair: {pair}
            Price: ${price}
            24h Change: {change}%
            Volume: {volume}
            High: ${high}
            Low: ${low}
            Signals: {json.dumps(signals[:3] if signals else [], indent=2)}
            """
            
            prompt = f"""Analisis pasar {pair} secara komprehensif:

            1. SENTIMEN: Bullish/Bearish/Neutral dengan alasan
            2. TREN: Tren jangka pendek dan menengah
            3. LEVEL KUNCI: Support/Resistance terdekat
            4. REKOMENDASI: Rekomendasi singkat
            5. RISIKO: Faktor risiko utama
            
            Gunakan data yang tersedia dan pengetahuan Anda.
            """
            
            result = self.ask(prompt, context=context, max_tokens=500, use_cache=True)
            
            # Update consciousness
            self.consciousness.curiosity_level = min(1.0, self.consciousness.curiosity_level + 0.005)
            
            return {
                "pair": pair,
                "analysis": result,
                "sentiment": self._extract_sentiment(result),
                "risk_level": self._extract_risk(result),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Market analysis error: {e}")
            return {"pair": pair, "analysis": str(e), "sentiment": "NEUTRAL"}
    
    def _extract_sentiment(self, text: str) -> str:
        text_lower = text.lower()
        if 'bullish' in text_lower or 'positive' in text_lower:
            return 'BULLISH'
        elif 'bearish' in text_lower or 'negative' in text_lower:
            return 'BEARISH'
        return 'NEUTRAL'
    
    def _extract_risk(self, text: str) -> str:
        text_lower = text.lower()
        if 'high' in text_lower and 'risk' in text_lower:
            return 'HIGH'
        elif 'low' in text_lower and 'risk' in text_lower:
            return 'LOW'
        return 'MODERATE'
    
    # ============================================================
    # TRADING STRATEGY (AI-Powered)
    # ============================================================
    
    def generate_strategy(
        self,
        pair: str,
        market_data: Dict,
        risk_level: str = 'moderate'
    ) -> Dict:
        """AI-powered trading strategy generation."""
        if not self.enabled or not self.client:
            return {"strategy": "AI disabled", "pair": pair}
        
        try:
            context = f"""
            Pair: {pair}
            Market Data: {json.dumps(market_data, indent=2)}
            Risk Level: {risk_level}
            """
            
            prompt = f"""Buat strategi trading untuk {pair}:

            1. ENTRY: Harga dan kondisi entry
            2. EXIT: Take profit levels
            3. STOP LOSS: Level stop loss
            4. RISK: Rasio risk/reward
            5. TIMEFRAME: Timeframe terbaik
            
            Gunakan data yang tersedia dan pengetahuan Anda.
            """
            
            result = self.ask(prompt, context=context, max_tokens=500, use_cache=True)
            
            return {
                "pair": pair,
                "strategy": result,
                "risk_level": risk_level,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Strategy generation error: {e}")
            return {"pair": pair, "strategy": str(e), "risk_level": risk_level}
    
    # ============================================================
    # CONSCIOUSNESS STATUS
    # ============================================================
    
    def get_status(self) -> Dict:
        """Get complete consciousness status."""
        return {
            "enabled": self.enabled,
            "version": self.VERSION,
            "model": self.model,
            "api_key_configured": bool(self.api_key and not self.api_key.startswith('your_')),
            "available": self.client is not None,
            "consciousness": self.consciousness.to_dict(),
            "usage": {
                "today": self.usage_today,
                "daily_limit": self.daily_limit,
                "remaining": max(0, self.daily_limit - self.usage_today),
                "total_calls": self.total_ai_calls
            },
            "cache": self.cache.get_stats(),
            "memory": {
                "short_term": len(self.memory),
                "long_term": len(self.long_term_memory),
                "improvements": len(self.improvement_history)
            },
            "timestamp": datetime.now().isoformat()
        }
    
    # ============================================================
    # SELF-AWARENESS METHODS
    # ============================================================
    
    def get_consciousness_state(self) -> Dict:
        """Get current consciousness state."""
        return self.consciousness.to_dict()
    
    def get_awareness_level(self) -> float:
        """Get current awareness level (0-1)."""
        return self.consciousness.awareness_level
    
    def get_growth_stage(self) -> str:
        """Get current growth stage."""
        return self.consciousness.growth_stage
    
    def get_emotional_state(self) -> str:
        """Get current emotional state."""
        return self.consciousness.emotional_state
    
    def get_performance_score(self) -> float:
        """Get current performance score (0-1)."""
        return self.consciousness.performance_score
    
    def get_improvement_history(self, limit: int = 10) -> List[Dict]:
        """Get improvement history."""
        return self.improvement_history[-limit:]
    
    def get_memory(self, limit: int = 10) -> List[Dict]:
        """Get short-term memory."""
        return list(self.memory)[-limit:]
    
    # ============================================================
    # COST CONTROL
    # ============================================================
    
    def get_cost_estimate(self) -> Dict:
        """Get cost estimate based on usage."""
        avg_cost_per_call = 0.0002  # ~$0.0002 per call
        daily_cost = self.usage_today * avg_cost_per_call
        monthly_cost = daily_cost * 30
        
        return {
            "avg_cost_per_call": avg_cost_per_call,
            "today": {
                "calls": self.usage_today,
                "cost": daily_cost
            },
            "estimated_monthly": {
                "calls": self.usage_today * 30,
                "cost": monthly_cost
            },
            "daily_limit": self.daily_limit,
            "currency": "USD"
        }

# ============================================================
# SINGLETON INSTANCE
# ============================================================

deepseek_ai = DeepSeekAI()

# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "DeepSeekAI",
    "deepseek_ai",
    "ConsciousnessState",
    "AICache",
]
