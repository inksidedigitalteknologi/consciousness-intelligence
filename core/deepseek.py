#!/usr/bin/env python
# -*- coding: utf-8 -*-
# core/deepseek.py
# INKSIDE DIGITAL - COGNITIVE AI ENGINE v3.1
# FULL INTEGRATION WITH ALL MODULES
# CAN BE ENABLED/DISABLED
# FIXED: load_dotenv() added, better error handling

import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from openai import OpenAI
from dotenv import load_dotenv

# ============================================================
# LOAD .env FILE - IMPORTANT!
# ============================================================

load_dotenv()

logger = logging.getLogger(__name__)

# ============================================================
# CONFIGURATION - READ FROM .env
# ============================================================

def _get_env(key: str, default: str = '') -> str:
    """Get environment variable with proper error handling."""
    value = os.getenv(key, default)
    if not value or value.startswith('your_') or value == '':
        logger.warning(f"⚠️ {key} appears to be placeholder or empty")
    return value

DEEPSEEK_ENABLED = os.getenv('DEEPSEEK_ENABLED', 'true').lower() == 'true'
DEEPSEEK_API_KEY = _get_env('DEEPSEEK_API_KEY', '')
DEEPSEEK_MODEL = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')

# Debug: Log API Key status
if DEEPSEEK_API_KEY:
    preview = f"{DEEPSEEK_API_KEY[:8]}...{DEEPSEEK_API_KEY[-8:]}" if len(DEEPSEEK_API_KEY) > 16 else "***"
    logger.info(f"🔑 API Key loaded: {preview}")
else:
    logger.warning("⚠️ API Key is EMPTY or not set in .env")

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
            if not content or len(content) < 20:
                return item
            
            ai = DeepSeekAI()
            if not ai.enabled or not ai.client:
                return item
            
            tags = ai.generate_tags(content)
            summary = ai.summarize(content)
            insights = ai.extract_insights(content)
            
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
    
    VERSION = "3.1.0"
    
    def __init__(self):
        self.enabled = DEEPSEEK_ENABLED
        self.api_key = DEEPSEEK_API_KEY
        self.model = DEEPSEEK_MODEL
        self.client = None
        
        if not self.enabled:
            logger.info("🧠 DeepSeek AI is DISABLED")
            return
        
        if not self.api_key or self.api_key.startswith('your_'):
            logger.error("❌ DEEPSEEK_API_KEY is not set or is placeholder!")
            logger.error("   Please set a valid API key in .env file")
            self.enabled = False
            return
        
        try:
            # Validate API key format
            if not self.api_key.startswith('sk-'):
                logger.warning("⚠️ API Key doesn't start with 'sk-'")
            
            logger.info(f"🔑 Initializing DeepSeek AI with key: {self.api_key[:8]}...{self.api_key[-8:]}")
            
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com/v1",
                timeout=30.0,
                max_retries=2
            )
            
            # Test connection with a simple request
            logger.info("🧠 Testing DeepSeek API connection...")
            test_response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Say 'OK'"}],
                max_tokens=5
            )
            logger.info(f"✅ DeepSeek API test successful: {test_response.choices[0].message.content}")
            
            logger.info(f"🧠 DeepSeek AI v{self.VERSION} ENABLED")
            logger.info(f"   Model: {self.model}")
            logger.info(f"   Base URL: https://api.deepseek.com/v1")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ DeepSeek init error: {error_msg}")
            
            # Specific error handling
            if "401" in error_msg or "Authentication" in error_msg:
                logger.error("   🔑 API Key is INVALID or REVOKED!")
                logger.error("   Please get a new API key from: https://platform.deepseek.com/")
            elif "429" in error_msg:
                logger.error("   ⚠️ Rate limit exceeded. Please wait and try again.")
            elif "Connection" in error_msg or "timeout" in error_msg.lower():
                logger.error("   🌐 Connection error. Check your internet connection.")
            
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
            "api_key_configured": bool(self.api_key and not self.api_key.startswith('your_')),
            "api_key_preview": f"{self.api_key[:8]}...{self.api_key[-8:]}" if self.api_key and len(self.api_key) > 16 else "***",
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
            return "⚠️ AI is disabled or not configured. Please check DEEPSEEK_API_KEY in .env"
        
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
            
            logger.debug(f"🤖 Sending request to DeepSeek API...")
            logger.debug(f"   Model: {self.model}")
            logger.debug(f"   Temperature: {temperature}")
            logger.debug(f"   Max tokens: {max_tokens}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            result = response.choices[0].message.content
            logger.debug(f"✅ DeepSeek response received ({len(result)} chars)")
            return result
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ AI ask error: {error_msg}")
            
            # Provide user-friendly error messages
            if "401" in error_msg:
                return "⚠️ API Key invalid or expired. Please update DEEPSEEK_API_KEY in .env"
            elif "429" in error_msg:
                return "⚠️ Rate limit exceeded. Please wait a moment and try again."
            elif "Connection" in error_msg:
                return "⚠️ Connection error. Please check your internet connection."
            elif "timeout" in error_msg.lower():
                return "⚠️ Request timeout. Please try again."
            else:
                return f"⚠️ Error: {error_msg[:200]}"
    
    # ============================================================
    # KNOWLEDGE ENHANCEMENT
    # ============================================================
    
    def generate_tags(self, content: str) -> List[str]:
        """Generate tags from content."""
        if not self.enabled or not self.client:
            return ['general']
        
        try:
            prompt = f"Buat 3-5 tag untuk konten ini:\n{content[:500]}"
            result = self.ask(prompt, temperature=0.3, max_tokens=100)
            
            tags = []
            for word in result.lower().split(','):
                cleaned = word.strip().replace('#', '').replace('tag:', '')
                if cleaned and len(cleaned) > 2:
                    tags.append(cleaned)
            
            return tags[:5] if tags else ['general']
        except Exception as e:
            logger.error(f"Tag generation error: {e}")
            return ['general']
    
    def summarize(self, content: str) -> str:
        """Generate summary from content."""
        if not self.enabled or not self.client:
            return content[:100] + '...'
        
        try:
            prompt = f"Ringkas konten ini dalam 1-2 kalimat:\n{content[:1000]}"
            return self.ask(prompt, temperature=0.3, max_tokens=150)
        except Exception as e:
            logger.error(f"Summarization error: {e}")
            return content[:100] + '...'
    
    def extract_insights(self, content: str) -> List[str]:
        """Extract insights from content."""
        if not self.enabled or not self.client:
            return []
        
        try:
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
        except Exception as e:
            logger.error(f"Insight extraction error: {e}")
            return []
    
    def enhance_knowledge(self, item: Dict) -> Dict:
        """Enhance knowledge item with AI."""
        if not self.enabled or not self.client:
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
    # MARKET ANALYSIS
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
        if not self.enabled or not self.client:
            return {"analysis": "AI is disabled or not configured", "sentiment": "NEUTRAL", "risk_level": "MODERATE"}
        
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
5. RISIKO: Faktor risiko utama"""

            result = self.ask(prompt, context=context, system_prompt="Anda adalah analis pasar crypto senior.")
            
            return {
                "pair": pair,
                "analysis": result,
                "sentiment": self._extract_sentiment(result),
                "risk_level": self._extract_risk(result),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Market analysis error: {e}")
            return {
                "pair": pair,
                "analysis": f"Error: {str(e)[:200]}",
                "sentiment": "NEUTRAL",
                "risk_level": "MODERATE",
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
    # PATTERN RECOGNITION
    # ============================================================
    
    def analyze_pattern(self, pattern_data: Dict) -> Dict:
        """Analyze pattern with AI."""
        if not self.enabled or not self.client:
            return {"analysis": "AI is disabled or not configured"}
        
        try:
            context = json.dumps(pattern_data, indent=2)
            prompt = f"Analisis pola ini:\n{context}\n\nBerikan: nama pola, bias, kekuatan, dan rekomendasi."
            
            result = self.ask(prompt, context=context, system_prompt="Anda adalah ahli pola chart.")
            
            return {
                "analysis": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Pattern analysis error: {e}")
            return {"analysis": f"Error: {str(e)[:200]}", "timestamp": datetime.now().isoformat()}
    
    # ============================================================
    # SIGNAL ENHANCEMENT
    # ============================================================
    
    def enhance_signal(self, signal: Dict) -> Dict:
        """Enhance trading signal with AI."""
        if not self.enabled or not self.client:
            return {**signal, 'ai_validation': 'AI disabled', 'ai_validated': False}
        
        try:
            context = json.dumps(signal, indent=2)
            prompt = f"Analisis sinyal trading ini:\n{context}\n\nBerikan: validasi, kekuatan, dan saran tambahan."
            
            result = self.ask(prompt, context=context, system_prompt="Anda adalah ahli sinyal trading.")
            
            return {
                **signal,
                'ai_validation': result,
                'ai_validated': True,
                'ai_validated_at': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Signal enhancement error: {e}")
            return {**signal, 'ai_validation': f"Error: {str(e)[:200]}", 'ai_validated': False}
    
    # ============================================================
    # TRADING STRATEGY
    # ============================================================
    
    def generate_strategy(
        self,
        pair: str,
        market_data: Dict,
        risk_level: str = 'moderate'
    ) -> Dict:
        """Generate trading strategy with AI."""
        if not self.enabled or not self.client:
            return {"strategy": "AI is disabled or not configured", "pair": pair}
        
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
5. TIMEFRAME: Timeframe terbaik"""

            result = self.ask(prompt, context=context, system_prompt="Anda adalah ahli strategi trading.")
            
            return {
                "pair": pair,
                "strategy": result,
                "risk_level": risk_level,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Strategy generation error: {e}")
            return {"pair": pair, "strategy": f"Error: {str(e)[:200]}", "risk_level": risk_level}
    
    # ============================================================
    # GENERAL KNOWLEDGE
    # ============================================================
    
    def learn_from_content(self, content: str, category: str = 'general') -> Dict:
        """Learn and extract knowledge from content."""
        if not self.enabled or not self.client:
            return {"content": content, "ai_learning": "AI disabled"}
        
        try:
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
        except Exception as e:
            logger.error(f"Learning error: {e}")
            return {"content": content, "ai_learning": f"Error: {str(e)[:200]}", "category": category}
    
    # ============================================================
    # REFLECTION
    # ============================================================
    
    def reflect(self, data: Dict, context: str = None) -> Dict:
        """AI reflection on trading decisions."""
        if not self.enabled or not self.client:
            return {"reflection": "AI is disabled or not configured"}
        
        try:
            context_str = json.dumps(data, indent=2) if context is None else context
            prompt = f"Refleksikan data ini:\n{context_str}\n\nBerikan: analisis, pelajaran, dan rekomendasi."
            
            result = self.ask(prompt, context=context_str, system_prompt="Anda adalah cognitive mirror.")
            
            return {
                "reflection": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Reflection error: {e}")
            return {"reflection": f"Error: {str(e)[:200]}", "timestamp": datetime.now().isoformat()}
    
    # ============================================================
    # KNOWLEDGE BATCH PROCESSING
    # ============================================================
    
    def process_knowledge_batch(self, items: List[Dict]) -> List[Dict]:
        """Process multiple knowledge items with AI."""
        if not self.enabled or not self.client or not items:
            return items
        
        enhanced = []
        for item in items[:10]:
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
