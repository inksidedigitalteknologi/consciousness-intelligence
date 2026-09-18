# core/log_reader.py
# ============================================================
# LOG READER ENGINE — baca log untuk dashboard
# ============================================================

import logging
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

LOG_DIR = Path("/root/consciousness-intelligence/logs")

# File log yang boleh dibaca (whitelist)
ALLOWED_LOGS = {
    "main.log": "Main Application Log",
    "error.log": "Application Errors",
    "security.log": "Security Events",
    "system.log": "System Output",
    "backup.log": "Backup Log",
    "learn.log": "Learning Log",
    "track_outcomes.log": "Outcomes Tracking",
}

LEVEL_RE = re.compile(r"\|\s*(DEBUG|INFO|WARNING|ERROR|CRITICAL)\s*\|")


class LogReader:
    """Baca log untuk dashboard."""

    def list_logs(self) -> List[Dict[str, Any]]:
        """Daftar log yang tersedia + ukuran."""
        result = []
        for name, desc in ALLOWED_LOGS.items():
            p = LOG_DIR / name
            if p.exists():
                stat = p.stat()
                result.append({
                    "name": name,
                    "description": desc,
                    "size_bytes": stat.st_size,
                    "size_kb": round(stat.st_size / 1024, 1),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })
        return result

    def read_tail(self, filename: str, lines: int = 100,
                  level: Optional[str] = None) -> Dict[str, Any]:
        """Baca N baris terakhir dari log."""
        if filename not in ALLOWED_LOGS:
            return {"error": f"File '{filename}' not allowed"}

        path = LOG_DIR / filename
        if not path.exists():
            return {"error": f"File '{filename}' not found"}

        try:
            # Baca semua lalu ambil tail
            with open(path, "r", errors="ignore") as f:
                all_lines = f.readlines()

            # Filter by level
            if level and level.upper() in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
                filtered = [
                    l for l in all_lines
                    if re.search(rf"\|\s*{level.upper()}\s*\|", l)
                ]
            else:
                filtered = all_lines

            tail = filtered[-lines:]

            return {
                "filename": filename,
                "total_lines": len(all_lines),
                "filtered_lines": len(filtered),
                "returned": len(tail),
                "lines": [l.rstrip("\n") for l in tail],
            }
        except Exception as e:
            return {"error": str(e)}

    def search(self, query: str, filename: Optional[str] = None,
               limit: int = 200) -> Dict[str, Any]:
        """Cari di log."""
        if not query or len(query) < 2:
            return {"error": "Query too short (min 2 chars)"}

        try:
            query_lower = query.lower()
            results = []

            files = [filename] if filename and filename in ALLOWED_LOGS else list(ALLOWED_LOGS.keys())

            for fname in files:
                path = LOG_DIR / fname
                if not path.exists():
                    continue
                with open(path, "r", errors="ignore") as f:
                    for i, line in enumerate(f):
                        if query_lower in line.lower():
                            results.append({
                                "file": fname,
                                "line_no": i + 1,
                                "text": line.rstrip("\n")[:500],
                            })
                            if len(results) >= limit:
                                break
                if len(results) >= limit:
                    break

            return {
                "query": query,
                "count": len(results),
                "results": results,
            }
        except Exception as e:
            return {"error": str(e)}

    def get_stats(self) -> Dict[str, Any]:
        """Ringkasan log — jumlah level."""
        stats = {}
        for name in ALLOWED_LOGS:
            path = LOG_DIR / name
            if not path.exists():
                continue
            try:
                counts = {"DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}
                with open(path, "r", errors="ignore") as f:
                    for line in f:
                        m = LEVEL_RE.search(line)
                        if m:
                            counts[m.group(1)] += 1
                stats[name] = counts
            except Exception:
                pass
        return stats


log_reader = LogReader()


if __name__ == "__main__":
    import json
    print("=== LIST LOGS ===")
    print(json.dumps(log_reader.list_logs(), indent=2))
    print("\n=== STATS ===")
    print(json.dumps(log_reader.get_stats(), indent=2))
