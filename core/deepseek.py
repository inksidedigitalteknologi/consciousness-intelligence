# core/deepseek.py
# INKSIDE DIGITAL - COGNITIVE AI ENGINE v3.0
# FULL INTEGRATION WITH ALL MODULES
# CAN BE ENABLED/DISABLED

import os
import json
import logging
import threading
from datetime import datetime
from typing import Optional, Dict, Any, List
from openai import OpenAI

logger = logging.getLogger(__name__)

# ============================================================
# CONFIGURATION
# ============================================================

DEEPSEEK_ENABLED = os.getenv('DEEPSEEK_ENABLED', 'true').lower() == 'true'
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_MODEL = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')

# ============================================================
# KNOWLEDGE ENHANCER
# ============================================================

class KnowledgeEnhancer:
    """Enhance knowledge with AI insights."""
    
    @staticmethod
    def enhance(item: Dict) -> Dict:
        """Enhance knowledge item with AI."""
        if not DEEPSEEK_ENABLED:
            return item
        
        try:
            content = item.get('content', '')
            category = item.get('category', 'general')
            
            # Generate tags
            tags = DeepSeekAI().generate_tags(content)
            
            # Generate summary
            summary = DeepSeekAI().summarize(content)
            
            # Extract insights
            insights = DeepSeekAI().extract_insights(content)
            
            return {
                **item,
                'ai_tags': tags,
                'ai_summary': summary,
                'ai_insights': insights,
                'ai_enhanced_at': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Knowledge enhancement error: {e}")
            return item

# ============================================================
# MAIN AI ENGINE
# ============================================================

class DeepSeekAI:
    """
    Cognitive AI Engine - Full Integration
    
    Features:
    - Can be enabled/disabled via DEEPSEEK_ENABLED
    - Integrates with Knowledge, Brain, Scanner, Signals
    - Auto-enhances knowledge items
    - Generates insights from market data
    """
    
    VERSION = "3.0.0"
    
    def __init__(self):
        self.enabled = DEEPSEEK_ENABLED
        self.api_key = DEEPSEEK_API_KEY
        self.model = DEEPSEEK_MODEL
        
        if not self.enabled:
            logger.info("🧠 DeepSeek AI is DISABLED")
            self.client = None
            return
        
        if not self.api_key:
            logger.warning("⚠️ DEEPSEEK_API_KEY not set. AI features unavailable.")
            self.client = None
            self.enabled = False
            return
        
        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com/v1"
            )
            logger.info(f"🧠 DeepSeek AI v{self.VERSION} ENABLED")
            logger.info(f"   Model: {self.model}")
        except Exception as e:
            logger.error(f"❌ DeepSeek init error: {e}")
            self.client = None
            self.enabled = False
    
    # ============================================================
    # STATUS
    # ============================================================
    
    def get_status(self) -> Dict:
        """Get AI engine status."""
        return {
            "enabled": self.enabled,
            "version": self.VERSION,
            "model": self.model,
            "api_key_configured": bool(self.api_key),
            "available": self.client is not None,
            "timestamp": datetime.now().isoformat()
        }
    
    # ============================================================
    # CORE METHODS
    # ============================================================
    
    def ask(
        self,
        question: str,
        context: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """Ask AI with context."""
        if not self.enabled or not self.client:
            return "⚠️ AI is disabled or not configured."
        
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({
                    "role": "system",
                    "content": (
                        "Anda adalah Cognitive AI Engine untuk sistem trading cerdas. "
                        "Berikan jawaban yang akurat, ringkas, dan berbasis data."
                    )
                })
            
            if context:
                messages.append({"role": "system", "content": f"Konteks:\n{context}"})
            
            messages.append({"role": "user", "content": question})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"❌ AI ask error: {e}")
            return f"⚠️ Error: {str(e)}"
    
    # ============================================================
    # KNOWLEDGE ENHANCEMENT
    # ============================================================
    
    def generate_tags(self, content: str) -> List[str]:
        """Generate tags from content."""
        if not self.enabled:
            return []
        
        prompt = f"Buat 3-5 tag untuk konten ini:\n{content[:500]}"
        result = self.ask(prompt, temperature=0.3, max_tokens=100)
        
        # Parse tags from response
        tags = []
        for word in result.lower().split(','):
            cleaned = word.strip().replace('#', '').replace('tag:', '')
            if cleaned and len(cleaned) > 2:
                tags.append(cleaned)
        
        return tags[:5] if tags else ['general']
    
    def summarize(self, content: str) -> str:
        """Generate summary from content."""
        if not self.enabled:
            return content[:100] + '...'
        
        prompt = f"Ringkas konten ini dalam 1-2 kalimat:\n{content[:1000]}"
        return self.ask(prompt, temperature=0.3, max_tokens=150)
    
    def extract_insights(self, content: str) -> List[str]:
        """Extract insights from content."""
        if not self.enabled:
            return []
        
        prompt = f"Ekstrak 3 insight penting dari konten ini:\n{content[:800]}"
        result = self.ask(prompt, temperature=0.4, max_tokens=200)
        
        insights = []
        for line in result.split('\n'):
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                insights.append(line.lstrip('- •*').strip())
            elif line and len(line) > 10:
                insights.append(line)
        
        return insights[:3]
    
    def enhance_knowledge(self, item: Dict) -> Dict:
        """Enhance knowledge item with AI."""
        if not self.enabled:
            return item
        
        try:
            content = item.get('content', '')
            if not content or len(content) < 20:
                return item
            
            return {
                **item,
                'ai_tags': self.generate_tags(content),
                'ai_summary': self.summarize(content),
                'ai_insights': self.extract_insights(content),
                'ai_enhanced': True,
                'ai_enhanced_at': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Knowledge enhancement error: {e}")
            return item
    
    # ============================================================
    # MARKET ANALYSIS (Integrasi dengan Scanner/Market Data)
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
        """Analyze market with AI."""
        if not self.enabled:
            return {"analysis": "AI is disabled"}
        
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
5. RISIKO: Faktor risiko utama"""

        result = self.ask(prompt, context=context, system_prompt="Anda adalah analis pasar crypto senior.")
        
        return {
            "pair": pair,
            "analysis": result,
            "sentiment": self._extract_sentiment(result),
            "risk_level": self._extract_risk(result),
            "timestamp": datetime.now().isoformat()
        }
    
    def _extract_sentiment(self, text: str) -> str:
        """Extract sentiment from analysis text."""
        text_lower = text.lower()
        if 'bullish' in text_lower or 'positive' in text_lower:
            return 'BULLISH'
        elif 'bearish' in text_lower or 'negative' in text_lower:
            return 'BEARISH'
        return 'NEUTRAL'
    
    def _extract_risk(self, text: str) -> str:
        """Extract risk level from analysis text."""
        text_lower = text.lower()
        if 'high' in text_lower and 'risk' in text_lower:
            return 'HIGH'
        elif 'low' in text_lower and 'risk' in text_lower:
            return 'LOW'
        return 'MODERATE'
    
    # ============================================================
    # PATTERN RECOGNITION (Integrasi dengan Pattern Engine)
    # ============================================================
    
    def analyze_pattern(self, pattern_data: Dict) -> Dict:
        """Analyze pattern with AI."""
        if not self.enabled:
            return {"analysis": "AI is disabled"}
        
        context = json.dumps(pattern_data, indent=2)
        prompt = f"Analisis pola ini:\n{context}\n\nBerikan: nama pola, bias, kekuatan, dan rekomendasi."
        
        result = self.ask(prompt, context=context, system_prompt="Anda adalah ahli pola chart.")
        
        return {
            "analysis": result,
            "timestamp": datetime.now().isoformat()
        }
    
    # ============================================================
    # SIGNAL ENHANCEMENT (Integrasi dengan Signal Engine)
    # ============================================================
    
    def enhance_signal(self, signal: Dict) -> Dict:
        """Enhance trading signal with AI."""
        if not self.enabled:
            return signal
        
        context = json.dumps(signal, indent=2)
        prompt = f"Analisis sinyal trading ini:\n{context}\n\nBerikan: validasi, kekuatan, dan saran tambahan."
        
        result = self.ask(prompt, context=context, system_prompt="Anda adalah ahli sinyal trading.")
        
        return {
            **signal,
            'ai_validation': result,
            'ai_validated_at': datetime.now().isoformat()
        }
    
    # ============================================================
    # TRADING STRATEGY (Integrasi dengan Trading Bot)
    # ============================================================
    
    def generate_strategy(
        self,
        pair: str,
        market_data: Dict,
        risk_level: str = 'moderate'
    ) -> Dict:
        """Generate trading strategy with AI."""
        if not self.enabled:
            return {"strategy": "AI is disabled"}
        
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
5. TIMEFRAME: Timeframe terbaik"""

        result = self.ask(prompt, context=context, system_prompt="Anda adalah ahli strategi trading.")
        
        return {
            "pair": pair,
            "strategy": result,
            "risk_level": risk_level,
            "timestamp": datetime.now().isoformat()
        }
    
    # ============================================================
    # GENERAL KNOWLEDGE (Integrasi dengan Knowledge Engine)
    # ============================================================
    
    def learn_from_content(self, content: str, category: str = 'general') -> Dict:
        """Learn and extract knowledge from content."""
        if not self.enabled:
            return {"content": content}
        
        prompt = f"""Ekstrak pengetahuan dari konten ini:

{content}

Berikan:
1. TOPIK: Topik utama
2. POIN PENTING: 3-5 poin penting
3. KATEGORI: Kategori yang sesuai
4. TAG: Tag yang relevan
5. LEVEL: Pemula/Menengah/Lanjutan"""

        result = self.ask(prompt, context=content, system_prompt="Anda adalah asisten pembelajaran.")
        
        return {
            "content": content,
            "ai_learning": result,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }
    
    # ============================================================
    # REFLECTION (Integrasi dengan Brain/Consciousness)
    # ============================================================
    
    def reflect(self, data: Dict, context: str = None) -> Dict:
        """AI reflection on trading decisions."""
        if not self.enabled:
            return {"reflection": "AI is disabled"}
        
        context_str = json.dumps(data, indent=2) if context is None else context
        prompt = f"Refleksikan data ini:\n{context_str}\n\nBerikan: analisis, pelajaran, dan rekomendasi."
        
        result = self.ask(prompt, context=context_str, system_prompt="Anda adalah cognitive mirror.")
        
        return {
            "reflection": result,
            "timestamp": datetime.now().isoformat()
        }
    
    # ============================================================
    # KNOWLEDGE BASE (Integrasi dengan Knowledge Engine)
    # ============================================================
    
    def process_knowledge_batch(self, items: List[Dict]) -> List[Dict]:
        """Process multiple knowledge items with AI."""
        if not self.enabled or not items:
            return items
        
        enhanced = []
        for item in items[:10]:  # Limit for performance
            try:
                enhanced.append(self.enhance_knowledge(item))
            except Exception as e:
                logger.error(f"Knowledge batch error: {e}")
                enhanced.append(item)
        
        return enhanced

# ============================================================
# SINGLETON INSTANCE
# ============================================================

deepseek_ai = DeepSeekAI()

# ============================================================
# INTEGRATION WITH KNOWLEDGE ENGINE (Auto-enhance)
# ============================================================

def auto_enhance_knowledge_item(item: Dict) -> Dict:
    """Wrapper for automatic knowledge enhancement."""
    return deepseek_ai.enhance_knowledge(item)

# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "DeepSeekAI",
    "deepseek_ai",
    "KnowledgeEnhancer",
    "auto_enhance_knowledge_item"
]
