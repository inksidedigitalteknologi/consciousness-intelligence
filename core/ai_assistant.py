"""
AI Universal Assistant — bisa jawab apapun dengan format visual.
Menggabungkan knowledge base + general knowledge + real-time data.
"""
import re
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

try:
    from core.deepseek import deepseek_ai
    DEEPSEEK_AVAILABLE = True
except Exception:
    DEEPSEEK_AVAILABLE = False
    deepseek_ai = None


class AIAssistant:
    """Universal AI Assistant — flexible untuk semua tipe pertanyaan."""

    # ============================================================
    # QUESTION TYPE DETECTION
    # ============================================================

    @staticmethod
    def detect_question_type(question: str) -> str:
        """Deteksi tipe pertanyaan berdasarkan keyword + pattern."""
        q = question.lower().strip()

        # Realtime data
        if any(k in q for k in ['harga sekarang', 'harga live', 'current price',
                                  'harga btc', 'harga eth', 'price now']):
            return "realtime"

        # Location / alamat
        if any(k in q for k in ['alamat', 'address', 'di mana', 'dimana',
                                  'lokasi', 'where is', 'location']):
            return "location"

        # Recipe / how-to
        if any(k in q for k in ['resep', 'recipe', 'cara membuat', 'cara bikin',
                                  'how to make', 'how to cook']):
            return "recipe"

        if any(k in q for k in ['cara', 'bagaimana', 'how to', 'how do i',
                                  'tutorial', 'step by step', 'langkah']):
            return "how_to"

        # Comparison
        if any(k in q for k in ['bandingkan', 'compare', ' vs ', 'versus',
                                  'lebih baik', 'difference between', 'perbedaan']):
            return "comparison"

        # Analysis (kenapa, mengapa)
        if any(k in q for k in ['kenapa', 'mengapa', 'why', 'sebab', 'alasan',
                                  'analisis', 'analyze', 'explain why']):
            return "analysis"

        # Knowledge base query
        if any(k in q for k in ['knowledge base', 'yang kamu tahu',
                                  'yang kamu pelajari', 'observasi',
                                  'catatan saya', 'data saya', 'sistem saya',
                                  'brain saya', 'trading saya', 'bot saya']):
            return "knowledge_base"

        # Definition (apa itu)
        if any(k in q for k in ['apa itu', 'what is', 'apa yang dimaksud',
                                  'definisi', 'pengertian', 'jelaskan',
                                  'explain', 'terangkan']):
            return "definition"

        # Creative
        if any(k in q for k in ['tulis', 'ceritakan', 'write', 'story',
                                  'puisi', 'poem', 'cerita', 'story']):
            return "creative"

        # Default
        return "general"

    # ============================================================
    # BUILD PROMPT PER TYPE
    # ============================================================

    @staticmethod
    def build_system_prompt() -> str:
        """System personality — AI universal assistant."""
        return """Anda adalah Inkside Digital AI Assistant — asisten cerdas yang:
- Menjawab pertanyaan apapun: sains, teknologi, masakan, tempat, sejarah, trading, dll.
- Punya akses ke knowledge base pengguna (trading bot data).
- Berpikir kritis, jujur, dan tidak bertele-tele.
- Selalu berusaha memberi jawaban yang akurat + berguna.
- TIDAK PERNAH bilang "saya tidak tahu" untuk topik umum — 
  kalau ragu, berikan info terbaik yang Anda tahu + disclaimer.

Bahasa: ikuti bahasa user (Indonesia/English)."""

    @staticmethod
    def build_prompt(question: str, q_type: str, kb_context: str = "") -> str:
        """Build prompt spesifik per tipe pertanyaan — output JSON terstruktur."""

        # Base context section
        context_section = ""
        if kb_context:
            context_section = f"""

=== KNOWLEDGE BASE CONTEXT ===
{kb_context[:2500]}

Gunakan context di atas KALAU relevan dengan pertanyaan.
Kalau tidak relevan, jawab dari pengetahuan umum Anda.
"""

        # Base JSON format instruction
        json_format = """
OUTPUT FORMAT (WAJIB JSON VALID):
{
  "title": "Judul singkat jawaban (maks 8 kata)",
  "summary": "Ringkasan inti 1-2 kalimat — ini yang user baca pertama",
  "sections": [
    {
      "heading": "Nama section (maks 4 kata)",
      "type": "list" | "text" | "steps" | "quote",
      "items": ["poin 1", "poin 2"] // untuk list/steps
      // ATAU
      "content": "teks paragraf" // untuk type "text"
    }
  ],
  "metrics": [
    {"label": "Label", "value": "Angka/Nilai", "color": "green|red|yellow|blue|purple"}
  ],
  "actions": ["Saran konkret 1", "Saran konkret 2"],
  "sources_used": true | false,
  "confidence": 0.0-1.0,
  "follow_up_questions": ["Pertanyaan lanjutan 1", "Pertanyaan lanjutan 2"]
}

ATURAN:
- sections: 2-4 section, jangan lebih
- Setiap section max 5 items
- metrics: kosongkan [] kalau tidak ada angka penting
- actions: 1-3 langkah konkret
- follow_up_questions: 2-3 pertanyaan yang user mungkin tanya
"""

        # Prompt per type
        prompts = {
            "definition": f"""User menanyakan DEFINISI/KONSEP. Jawab dengan jelas + contoh konkret.
{context_section}

Pertanyaan: {question}
{json_format}

Fokus: definisi akurat, contoh nyata, kapan dipakai.""",

            "general": f"""Jawab pertanyaan umum user dengan informatif.
{context_section}

Pertanyaan: {question}
{json_format}

Kalau topik random (resep, alamat, dll), jawab langsung dengan info yang berguna.""",

            "recipe": f"""User minta RESEP. Berikan resep lengkap + tips.
{context_section}

Pertanyaan: {question}
{json_format}

Sertakan: bahan-bahan (list), cara membuat (steps), tips (quote/text).""",

            "location": f"""User menanyakan LOKASI/ALAMAT. Berikan info lengkap.
{context_section}

Pertanyaan: {question}
{json_format}

Sertakan: alamat lengkap, koordinat (kalau tahu), cara akses, jam buka, tiket (kalau relevan).""",

            "how_to": f"""User minta TUTORIAL/CARA. Berikan langkah-langkah.
{context_section}

Pertanyaan: {question}
{json_format}

Fokus: langkah-langkah praktis, tips penting, common mistake.""",

            "comparison": f"""User minta PERBANDINGAN. Berikan analisis side-by-side.
{context_section}

Pertanyaan: {question}
{json_format}

Fokus: tabel perbandingan (gunakan metrics), rekomendasi jelas.""",

            "analysis": f"""User minta ANALISIS (kenapa/mengapa). Berikan analisis mendalam.
{context_section}

Pertanyaan: {question}
{json_format}

Fokus: penyebab utama, faktor pendukung, data konkret dari KB kalau ada.""",

            "realtime": f"""User minta DATA REAL-TIME. Berikan data + konteks.
{context_section}

Pertanyaan: {question}
{json_format}

Kalau ada data dari KB, pakai. Kalau tidak, jelaskan bahwa data real-time
butuh API dan berikan info konteks.""",

            "knowledge_base": f"""User menanyakan KNOWLEDGE BASE mereka sendiri.
{context_section}

Pertanyaan: {question}
{json_format}

WAJIB pakai context dari knowledge base. Kalau context kosong, bilang
tidak ada data relevan di KB — tapi tetap bantu dengan saran.""",

            "creative": f"""User minta KONTEN KREATIF (cerita, puisi, dll).
{context_section}

Pertanyaan: {question}
{json_format}

Fokus: karya kreatif, menarik, engaging.""",
        }

        return prompts.get(q_type, prompts["general"])

    # ============================================================
    # ASK — entry point
    # ============================================================

    def ask(
        self,
        question: str,
        kb_search_func=None,
        context: str = "",
        kb_items: Optional[List] = None,
    ) -> Dict[str, Any]:
        """
        Main entry — jawab pertanyaan apapun.
        Return structured dict untuk frontend rendering.
        """
        if not DEEPSEEK_AVAILABLE or not deepseek_ai:
            return {
                "title": "AI Tidak Tersedia",
                "summary": "AI (DeepSeek) tidak aktif. Cek konfigurasi.",
                "sections": [],
                "metrics": [],
                "actions": [],
                "sources_used": False,
                "confidence": 0.0,
                "follow_up_questions": [],
                "question_type": "error",
                "error": True,
            }

        # 1. Detect type
        q_type = self.detect_question_type(question)
        logger.info(f"🤖 AI Assistant: type={q_type}, question='{question[:60]}...'")

        # 2. Retrieve KB context
        if kb_search_func and q_type in ["knowledge_base", "analysis", "comparison", "hybrid", "realtime"]:
            try:
                relevant = kb_search_func(question, max_results=5) or []
                if relevant and not context:
                    context = "\n\n".join([
                        f"[{getattr(i, 'category', 'KB')}] {getattr(i, 'content', '')}"
                        for i in relevant
                    ])
                    kb_items = relevant
            except Exception as e:
                logger.warning(f"KB search failed: {e}")

        # 3. Build prompt
        system = self.build_system_prompt()
        user_prompt = self.build_prompt(question, q_type, context)

        # 4. Call AI — minta output JSON
        try:
            # Coba minta JSON response
            raw = deepseek_ai.ask(
                question=user_prompt,
                system_prompt=system,
                temperature=0.6,
                max_tokens=2000,
                use_cache=True,
            )
            result = self._parse_json_response(raw, question, q_type)

        except Exception as e:
            logger.error(f"AI Assistant error: {e}")
            return {
                "title": "Error",
                "summary": f"Gagal memanggil AI: {str(e)[:100]}",
                "sections": [],
                "metrics": [],
                "actions": [],
                "sources_used": False,
                "confidence": 0.0,
                "follow_up_questions": [],
                "question_type": q_type,
                "error": True,
            }

        # 5. Attach metadata
        result["question_type"] = q_type
        result["sources_used"] = bool(context)
        result["kb_items_count"] = len(kb_items) if kb_items else 0
        result["timestamp"] = datetime.now().isoformat()

        return result

    # ============================================================
    # JSON PARSER — robust
    # ============================================================

    @staticmethod
    def _parse_json_response(raw: str, question: str, q_type: str) -> Dict:
        """Parse AI response jadi JSON. Fallback ke markdown kalau gagal."""
        if not raw:
            return AIAssistant._fallback_response(question, q_type, "Empty response")

        # Coba parse JSON langsung
        try:
            # Buang markdown code fence kalau ada
            cleaned = raw.strip()
            if cleaned.startswith('```'):
                # Hapus ```json ... ```
                cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
                cleaned = re.sub(r'\s*```$', '', cleaned)

            # Cari JSON object pertama
            match = re.search(r'\{.*\}', cleaned, re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))
                # Validasi minimal
                if isinstance(parsed, dict) and 'summary' in parsed:
                    return AIAssistant._normalize(parsed)
        except Exception as e:
            logger.warning(f"JSON parse failed: {e}")

        # Fallback: render sebagai markdown section
        return AIAssistant._markdown_fallback(raw, question, q_type)

    @staticmethod
    def _normalize(data: Dict) -> Dict:
        """Normalize JSON — pastikan semua field ada."""
        return {
            "title": data.get("title", "Jawaban"),
            "summary": data.get("summary", ""),
            "sections": data.get("sections", [])[:5],
            "metrics": data.get("metrics", [])[:6],
            "actions": data.get("actions", [])[:5],
            "follow_up_questions": data.get("follow_up_questions", [])[:4],
            "confidence": float(data.get("confidence", 0.7)),
        }

    @staticmethod
    def _markdown_fallback(raw: str, question: str, q_type: str) -> Dict:
        """Kalau AI tidak output JSON, parse markdown → sections."""
        lines = raw.split('\n')
        sections = []
        current_section = None
        current_items = []

        for line in lines:
            line = line.rstrip()
            # Heading
            if line.startswith('##'):
                if current_section:
                    sections.append({
                        "heading": current_section,
                        "type": "list" if current_items else "text",
                        "items": current_items if current_items else [],
                        "content": "" if current_items else "",
                    })
                current_section = line.lstrip('#').strip()
                current_items = []
            # List item
            elif line.strip().startswith(('-', '*', '•')) or re.match(r'^\d+\.', line.strip()):
                item = re.sub(r'^[\s\-\*•]+|^\d+\.\s*', '', line)
                item = item.replace('**', '').strip()
                if item:
                    current_items.append(item)
            # Text biasa
            elif line.strip() and current_section:
                if not current_items:
                    current_items.append(line.strip())

        if current_section:
            sections.append({
                "heading": current_section,
                "type": "list" if current_items else "text",
                "items": current_items if current_items else [],
                "content": "" if current_items else "",
            })

        # Kalau tidak ada section, pakai raw sebagai summary
        if not sections:
            return AIAssistant._fallback_response(question, q_type, raw[:500])

        return {
            "title": sections[0]["heading"] if sections else "Jawaban",
            "summary": " ".join(sections[0].get("items", [])[:2])[:300] if sections else raw[:300],
            "sections": sections[:5],
            "metrics": [],
            "actions": [],
            "follow_up_questions": [],
            "confidence": 0.7,
        }

    @staticmethod
    def _fallback_response(question: str, q_type: str, raw: str) -> Dict:
        """Last resort — tampilkan raw text."""
        return {
            "title": "Jawaban",
            "summary": raw[:300],
            "sections": [{
                "heading": "Detail",
                "type": "text",
                "content": raw,
                "items": [],
            }] if raw else [],
            "metrics": [],
            "actions": [],
            "follow_up_questions": [],
            "confidence": 0.5,
        }


# Singleton
ai_assistant = AIAssistant()
