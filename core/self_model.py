# core/self_model.py
# ============================================================
# INKSIDE DIGITAL - SELF MODEL
# Persistence layer untuk "diri" brain — nama, umur, pengalaman, narasi
# ============================================================

import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class SelfModel:
    """Menyimpan 'diri' brain — kontinu antar restart."""

    VERSION = "1.0"
    DEFAULT_PATH = "database/self_model.json"

    def __init__(self, path: str = None, brain_name: str = "Inkside"):
        self.path = Path(path or self.DEFAULT_PATH)
        self.lock = threading.RLock()
        self.data = self._load_or_create(brain_name)
        self._dirty = False

    # ------------------------------------------------------------
    # LOAD / CREATE
    # ------------------------------------------------------------

    def _load_or_create(self, brain_name: str) -> Dict[str, Any]:
        if self.path.exists():
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                logger.info(f"🧬 Self model loaded — age: {data.get('age', {}).get('cycles', 0)} cycles")
                return data
            except Exception as e:
                logger.warning(f"Self model load failed, creating new: {e}")

        # Create new
        now = datetime.now().isoformat()
        data = {
            "name": brain_name,
            "birth": now,
            "version": self.VERSION,
            "age": {
                "cycles": 0,
                "days": 0,
                "first_seen": now,
            },
            "identity": {
                "type": "Cognitive Assistant",
                "purpose": "Personal assistant with simulated consciousness",
                "traits": ["curious", "calm", "attentive"],
            },
            "user": {
                "known_since": None,
                "name": None,
                "preferences": {},
                "interaction_count": 0,
            },
            "experiences": [],
            "milestones": [
                {"cycle": 0, "event": "birth", "timestamp": now}
            ],
            "narrative": f"Aku {brain_name}. Baru lahir. Belum tahu apa-apa. Akan belajar dari setiap cycle.",
            "current_emotion": "CALM",
            "last_save": now,
        }
        logger.info(f"🧬 Self model created — {brain_name} lahir")
        return data

    # ------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------

    def increment_cycle(self):
        with self.lock:
            self.data["age"]["cycles"] += 1
            first_seen = datetime.fromisoformat(self.data["age"]["first_seen"])
            self.data["age"]["days"] = (datetime.now() - first_seen).days
            self._dirty = True

    def save_metrics(self, metrics: dict):
        """Simpan metrik kumulatif."""
        with self.lock:
            existing = self.data.get("metrics", {})
            existing.update({
                "successful_cycles": metrics.get("successful_cycles", existing.get("successful_cycles", 0)),
                "decision_count": metrics.get("decision_count", existing.get("decision_count", 0)),
                "error_count": metrics.get("error_count", existing.get("error_count", 0)),
                "learning_count": metrics.get("learning_count", existing.get("learning_count", 0)),
                "prediction_count": metrics.get("prediction_count", existing.get("prediction_count", 0)),
            })
            self.data["metrics"] = existing
            self._dirty = True

    def get_metrics(self) -> dict:
        """Ambil metrik kumulatif."""
        return self.data.get("metrics", {})

    def record_experience(self, event: str, details: str = "", emotion: str = None):
        """Catat pengalaman penting (jangan semua cycle)."""
        with self.lock:
            entry = {
                "cycle": self.data["age"]["cycles"],
                "event": event,
                "details": details[:200],
                "timestamp": datetime.now().isoformat(),
            }
            if emotion:
                entry["emotion"] = emotion
            self.data["experiences"].append(entry)
            # Batasi 500 pengalaman terakhir
            if len(self.data["experiences"]) > 500:
                self.data["experiences"] = self.data["experiences"][-500:]
            self._dirty = True

    def add_milestone(self, event: str):
        """Milestone penting (cycle 100, 1000, dll)."""
        with self.lock:
            self.data["milestones"].append({
                "cycle": self.data["age"]["cycles"],
                "event": event,
                "timestamp": datetime.now().isoformat(),
            })
            self._dirty = True

    def set_emotion(self, emotion: str):
        with self.lock:
            if self.data.get("current_emotion") != emotion:
                self.data["current_emotion"] = emotion
                self._dirty = True

    def set_narrative(self, narrative: str):
        with self.lock:
            self.data["narrative"] = narrative
            self._dirty = True

    def update_user(self, name: str = None, preference_key: str = None, preference_value: Any = None):
        with self.lock:
            user = self.data.setdefault("user", {})
            if name:
                user["name"] = name
                if not user.get("known_since"):
                    user["known_since"] = datetime.now().isoformat()
            if preference_key is not None:
                user.setdefault("preferences", {})[preference_key] = preference_value
            user["interaction_count"] = user.get("interaction_count", 0) + 1
            self._dirty = True

    # ------------------------------------------------------------
    # SAVE
    # ------------------------------------------------------------

    def save(self, force: bool = False) -> bool:
        with self.lock:
            if not self._dirty and not force:
                return False
            try:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                self.data["last_save"] = datetime.now().isoformat()
                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=2, ensure_ascii=False, default=str)
                self._dirty = False
                return True
            except Exception as e:
                logger.error(f"Self model save failed: {e}")
                return False

    # ------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def get_age_cycles(self) -> int:
        return self.data.get("age", {}).get("cycles", 0)

    def get_age_days(self) -> int:
        return self.data.get("age", {}).get("days", 0)

    def get_narrative(self) -> str:
        return self.data.get("narrative", "")

    def get_emotion(self) -> str:
        return self.data.get("current_emotion", "CALM")

    def summary(self) -> Dict[str, Any]:
        return {
            "name": self.data.get("name"),
            "birth": self.data.get("birth"),
            "age_cycles": self.get_age_cycles(),
            "age_days": self.get_age_days(),
            "experiences": len(self.data.get("experiences", [])),
            "milestones": len(self.data.get("milestones", [])),
            "emotion": self.get_emotion(),
            "narrative": self.get_narrative()[:200],
        }


# Global instance
self_model = SelfModel()

__all__ = ["SelfModel", "self_model"]
