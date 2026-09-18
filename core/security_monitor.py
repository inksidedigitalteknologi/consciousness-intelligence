# core/security_monitor.py
# ============================================================
# SECURITY MONITOR ENGINE v2.0 — Comprehensive
# ============================================================
#
# FUNGSI:
#   1. Parse auth.log (SSH failed/success, sudo)
#   2. Parse nginx access.log (bot scan, exploit)
#   3. Klasifikasi serangan (10+ pattern)
#   4. Update ip_intelligence, username_attempts,
#      attack_patterns, user_agents
#   5. Update hourly_timeline & daily_summary
#   6. Hitung threat score per IP
#   7. Generate alerts otomatis
#
# ============================================================

import logging
import re
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# ── Setup security logger terpisah ─────────────────────────
SECURITY_LOG_PATH = Path("/root/consciousness-intelligence/logs/security.log")
SECURITY_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
security_logger = logging.getLogger("security")

if not security_logger.handlers:
    _sec_handler = logging.FileHandler(str(SECURITY_LOG_PATH), encoding="utf-8")
    _sec_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    ))
    security_logger.addHandler(_sec_handler)
    security_logger.setLevel(logging.INFO)
    security_logger.propagate = False  # jangan tulis ke main.log

# ── Config ──────────────────────────────────────────────────
DB_PATH = Path("/root/consciousness-intelligence/database/security.db")
AUTH_LOG_PATH = Path("/var/log/auth.log")
NGINX_ACCESS_PATH = Path("/var/log/nginx/access.log")

# ── Whitelist IP (tidak muncul di dashboard) ────────────────
WHITELIST_IPS = set()  # TEMPORARY DISABLED

# ── Attack Patterns ────────────────────────────────────────
ATTACK_PATTERNS = {
    "phpunit": r"phpunit|eval-stdin",
    "shellshock": r"\(\)\s*\{\s*:;\s*\}",
    "cgi_scan": r"cgi-bin|cgi/",
    "wp_scan": r"wp-admin|wp-login|xmlrpc\.php",
    "env_scan": r"\.env|\.git/|\.svn",
    "admin_scan": r"admin\.php|admin/config|phpmyadmin|myadmin",
    "traversal": r"\.\./|\.\.%2f|etc/passwd|etc/shadow",
    "sql_inject": r"union.*select|select.*from|information_schema|sleep\(\d+\)",
    "xss": r"<script|javascript:|onerror=|onload=",
    "docker_api": r"containers/json|/v1\.\d+/|docker",
    "thinkphp": r"think\\\\app|invokefunction|call_user_func",
    "iot_scan": r"goform|device\.rsp|cstecgi|password_change\.cgi",
    "http_probe": r"hello\.world|SDK/webLanguage|/login$|/test$",
}

# ── Event Types ─────────────────────────────────────────────
EVENT_SSH_FAILED = "ssh_failed"
EVENT_SSH_SUCCESS = "ssh_success"
EVENT_NGINX_SCAN = "nginx_scan"
EVENT_NGINX_EXPLOIT = "nginx_exploit"

# ── Severity mapping ───────────────────────────────────────
SEVERITY_MAP = {
    "phpunit": "high",
    "shellshock": "critical",
    "sql_inject": "critical",
    "traversal": "high",
    "xss": "medium",
    "docker_api": "high",
    "thinkphp": "critical",
    "iot_scan": "high",
    "wp_scan": "medium",
    "env_scan": "medium",
    "admin_scan": "low",
    "cgi_scan": "medium",
    "http_probe": "low",
    "ssh_failed": "low",
    "ssh_success": "info",
    "nginx_scan": "low",
    "nginx_exploit": "high",
}


class SecurityMonitor:
    """Engine monitoring keamanan komprehensif."""

    def __init__(self):
        self.db_path = DB_PATH
        self._init_state()

    # ── DB helpers ──────────────────────────────────────────

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_path))

    def _init_state(self):
        """Pastikan scan_state ada baris untuk setiap source."""
        try:
            conn = self._conn()
            cursor = conn.cursor()
            for source in ("auth_log", "nginx_log"):
                cursor.execute(
                    "INSERT OR IGNORE INTO scan_state (source, last_offset) VALUES (?, 0)",
                    (source,),
                )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"_init_state error: {e}")

    def _get_offset(self, source: str) -> int:
        try:
            conn = self._conn()
            cursor = conn.cursor()
            cursor.execute("SELECT last_offset FROM scan_state WHERE source=?", (source,))
            row = cursor.fetchone()
            conn.close()
            return row[0] if row else 0
        except Exception:
            return 0

    def _update_offset(self, source: str, offset: int, event_count: int):
        try:
            conn = self._conn()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE scan_state
                SET last_offset=?, last_scan=?, total_scans=total_scans+1,
                    total_events=total_events+?
                WHERE source=?
            """, (offset, datetime.now().isoformat(), event_count, source))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"_update_offset error: {e}")

    # ── Classify attack ─────────────────────────────────────

    def classify_attack(self, path: str, user_agent: str = "") -> Tuple[Optional[str], str]:
        """Return (attack_type, severity)."""
        combined = f"{path} {user_agent}".lower()
        for attack_type, pattern in ATTACK_PATTERNS.items():
            if re.search(pattern, combined, re.IGNORECASE):
                return attack_type, SEVERITY_MAP.get(attack_type, "low")
        return None, "low"

    # ── Parse auth.log ──────────────────────────────────────

    def parse_auth_log(self) -> int:
        if not AUTH_LOG_PATH.exists():
            return 0
        try:
            offset = self._get_offset("auth_log")
            current_size = AUTH_LOG_PATH.stat().st_size
            if current_size <= offset:
                return 0

            with open(AUTH_LOG_PATH, "r", errors="ignore") as f:
                f.seek(offset)
                lines = f.readlines()

            self._update_offset("auth_log", current_size, 0)

            failed_re = re.compile(
                r"Failed password for (?:invalid user )?(\S+) from (\S+) port (\d+)"
            )
            accepted_re = re.compile(
                r"Accepted (?:password|publickey) for (\S+) from (\S+) port (\d+)"
            )

            events = []
            for line in lines:
                ts = line[:19] if len(line) > 19 and line[:4].isdigit() else datetime.now().isoformat()

                m = failed_re.search(line)
                if m:
                    username, ip, _ = m.groups()
                    events.append({
                        "timestamp": ts, "ip": ip,
                        "event_type": EVENT_SSH_FAILED,
                        "severity": SEVERITY_MAP[EVENT_SSH_FAILED],
                        "username": username, "path": None,
                        "method": None, "status_code": None,
                        "user_agent": None, "source": "auth_log",
                        "raw": line.strip()[:500],
                    })
                    continue

                m = accepted_re.search(line)
                if m:
                    username, ip, _ = m.groups()
                    events.append({
                        "timestamp": ts, "ip": ip,
                        "event_type": EVENT_SSH_SUCCESS,
                        "severity": SEVERITY_MAP[EVENT_SSH_SUCCESS],
                        "username": username, "path": None,
                        "method": None, "status_code": None,
                        "user_agent": None, "source": "auth_log",
                        "raw": line.strip()[:500],
                    })

            if events:
                self._save_events(events)
                self._update_offset("auth_log", current_size, len(events))
                self._aggregate_events(events)

            if events:
                security_logger.info(f"🔒 auth.log: {len(events)} events")
            return len(events)
        except Exception as e:
            security_logger.error(f"parse_auth_log error: {e}")
            return 0

    # ── Parse nginx ─────────────────────────────────────────

    def parse_nginx_log(self) -> int:
        if not NGINX_ACCESS_PATH.exists():
            return 0
        try:
            offset = self._get_offset("nginx_log")
            current_size = NGINX_ACCESS_PATH.stat().st_size
            if current_size <= offset:
                return 0

            with open(NGINX_ACCESS_PATH, "r", errors="ignore") as f:
                f.seek(offset)
                lines = f.readlines()

            self._update_offset("nginx_log", current_size, 0)

            nginx_re = re.compile(
                r'(\S+) - - \[([^\]]+)\] "(\S+) (\S+) [^"]*" (\d+) \S+ "[^"]*" "([^"]*)"'
            )

            events = []
            for line in lines:
                m = nginx_re.search(line)
                if not m:
                    continue
                ip, ts, method, path, status, ua = m.groups()
                status = int(status)
                attack_type, severity = self.classify_attack(path, ua)

                # Skip request normal (bukan bot)
                if not attack_type and status < 400:
                    continue

                # Skip request dari IP Anda (bukan bot)
                if ip in ("127.0.0.1", "121.121.162.72", "14.192.246.97"):
                    continue

                # Tentukan tipe event
                if attack_type and severity in ("high", "critical"):
                    ev_type = EVENT_NGINX_EXPLOIT
                elif attack_type:
                    ev_type = EVENT_NGINX_SCAN
                elif status in (403, 404):
                    ev_type = EVENT_NGINX_SCAN
                else:
                    continue

                events.append({
                    "timestamp": ts, "ip": ip,
                    "event_type": ev_type,
                    "severity": severity if attack_type else SEVERITY_MAP[ev_type],
                    "username": None, "path": path,
                    "method": method, "status_code": status,
                    "user_agent": ua[:200], "source": "nginx_log",
                    "raw": line.strip()[:500],
                })

            if events:
                self._save_events(events)
                self._update_offset("nginx_log", current_size, len(events))
                self._aggregate_events(events)

            if events:
                security_logger.info(f"🌐 nginx.log: {len(events)} events")
            return len(events)
        except Exception as e:
            security_logger.error(f"parse_nginx_log error: {e}")
            return 0

    # ── Save & aggregate ────────────────────────────────────

    def _save_events(self, events: List[Dict[str, Any]]):
        if not events:
            return
        try:
            conn = self._conn()
            cursor = conn.cursor()
            cursor.executemany("""
                INSERT INTO security_events
                (timestamp, ip, event_type, severity, username, path,
                 method, status_code, user_agent, source, raw)
                VALUES (:timestamp, :ip, :event_type, :severity, :username, :path,
                        :method, :status_code, :user_agent, :source, :raw)
            """, events)
            conn.commit()
            conn.close()
            security_logger.info(f"💾 Saved {len(events)} security events")
        except Exception as e:
            logger.error(f"_save_events error: {e}")

    def _aggregate_events(self, events: List[Dict[str, Any]]):
        """Update ip_intelligence, username_attempts, attack_patterns, user_agents."""
        try:
            conn = self._conn()
            cursor = conn.cursor()
            now = datetime.now().isoformat()

            for e in events:
                ip = e.get("ip")
                if not ip:
                    continue

                # ── ip_intelligence ────────────────────────
                cursor.execute("SELECT ip FROM ip_intelligence WHERE ip=?", (ip,))
                exists = cursor.fetchone()

                if not exists:
                    cursor.execute("""
                        INSERT INTO ip_intelligence
                        (ip, first_seen, last_seen, total_hits)
                        VALUES (?, ?, ?, 1)
                    """, (ip, now, now))
                    # GeoIP lookup — langsung (blocking, ~10ms per IP)
                    try:
                        geo = self.lookup_geoip(ip)
                        if geo.get("country") and geo["country"] != "Unknown":
                            cursor.execute(
                                "UPDATE ip_intelligence SET country=? WHERE ip=?",
                                (geo["country"], ip)
                            )
                    except Exception:
                        pass
                else:
                    cursor.execute("""
                        UPDATE ip_intelligence SET
                            last_seen=?,
                            total_hits=total_hits+1
                        WHERE ip=?
                    """, (now, ip))

                # Update counter per tipe
                ev_type = e.get("event_type")
                if ev_type == EVENT_SSH_FAILED:
                    cursor.execute("UPDATE ip_intelligence SET ssh_failed=ssh_failed+1 WHERE ip=?", (ip,))
                elif ev_type == EVENT_SSH_SUCCESS:
                    cursor.execute("UPDATE ip_intelligence SET ssh_success=ssh_success+1 WHERE ip=?", (ip,))
                elif ev_type == EVENT_NGINX_SCAN:
                    cursor.execute("UPDATE ip_intelligence SET nginx_scans=nginx_scans+1 WHERE ip=?", (ip,))
                elif ev_type == EVENT_NGINX_EXPLOIT:
                    cursor.execute("UPDATE ip_intelligence SET exploits=exploits+1 WHERE ip=?", (ip,))

                # ── username_attempts ──────────────────────
                username = e.get("username")
                if username:
                    cursor.execute("SELECT username FROM username_attempts WHERE username=?", (username,))
                    if cursor.fetchone():
                        cursor.execute("""
                            UPDATE username_attempts SET
                                count=count+1, last_seen=?
                            WHERE username=?
                        """, (now, username))
                        if ev_type == EVENT_SSH_SUCCESS:
                            cursor.execute("UPDATE username_attempts SET success_count=success_count+1 WHERE username=?", (username,))
                    else:
                        cursor.execute("""
                            INSERT INTO username_attempts
                            (username, count, first_seen, last_seen, success_count)
                            VALUES (?, 1, ?, ?, ?)
                        """, (username, now, now, 1 if ev_type == EVENT_SSH_SUCCESS else 0))

                # ── attack_patterns ───────────────────────
                path = e.get("path") or ""
                ua = e.get("user_agent") or ""
                attack_type, _ = self.classify_attack(path, ua)
                if attack_type:
                    cursor.execute("SELECT id FROM attack_patterns WHERE pattern_type=?", (attack_type,))
                    if cursor.fetchone():
                        cursor.execute("""
                            UPDATE attack_patterns SET
                                count=count+1, last_seen=?
                            WHERE pattern_type=?
                        """, (now, attack_type))
                    else:
                        cursor.execute("""
                            INSERT INTO attack_patterns
                            (pattern_type, pattern_value, count, first_seen, last_seen)
                            VALUES (?, ?, 1, ?, ?)
                        """, (attack_type, path[:200], now, now))

                # ── user_agents ───────────────────────────
                if ua and len(ua) < 500:
                    ua_short = ua[:200]
                    cursor.execute("SELECT user_agent FROM user_agents WHERE user_agent=?", (ua_short,))
                    if cursor.fetchone():
                        cursor.execute("""
                            UPDATE user_agents SET count=count+1, last_seen=?
                            WHERE user_agent=?
                        """, (now, ua_short))
                    else:
                        is_mal = 1 if re.search(r"libredtail|nikto|sqlmap|nmap|masscan|zgrab", ua, re.I) else 0
                        cursor.execute("""
                            INSERT INTO user_agents
                            (user_agent, count, first_seen, last_seen, is_malicious)
                            VALUES (?, 1, ?, ?, ?)
                        """, (ua_short, now, now, is_mal))

                # ── hourly_timeline ───────────────────────
                hour_key = datetime.now().strftime("%Y-%m-%d %H:00")
                cursor.execute("SELECT hour_key FROM hourly_timeline WHERE hour_key=?", (hour_key,))
                if cursor.fetchone():
                    cursor.execute("""
                        UPDATE hourly_timeline SET total_events=total_events+1
                        WHERE hour_key=?
                    """, (hour_key,))
                    if ev_type == EVENT_SSH_FAILED:
                        cursor.execute("UPDATE hourly_timeline SET ssh_failed=ssh_failed+1 WHERE hour_key=?", (hour_key,))
                    elif ev_type == EVENT_NGINX_SCAN:
                        cursor.execute("UPDATE hourly_timeline SET nginx_scans=nginx_scans+1 WHERE hour_key=?", (hour_key,))
                else:
                    cursor.execute("""
                        INSERT INTO hourly_timeline
                        (hour_key, total_events, ssh_failed, nginx_scans)
                        VALUES (?, 1, ?, ?)
                    """, (hour_key,
                          1 if ev_type == EVENT_SSH_FAILED else 0,
                          1 if ev_type == EVENT_NGINX_SCAN else 0))

            # ── update threat_score ───────────────────────
            cursor.execute("""
                UPDATE ip_intelligence SET threat_score =
                    MIN(100,
                        ssh_failed * 1 +
                        nginx_scans * 3 +
                        exploits * 10 +
                        ssh_success * 50
                    )
            """)

            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"_aggregate_events error: {e}")

    # ── Public API ──────────────────────────────────────────

    def scan_all(self) -> Dict[str, int]:
        return {
            "auth_log": self.parse_auth_log(),
            "nginx_log": self.parse_nginx_log(),
        }

    def lookup_geoip(self, ip: str) -> Dict[str, str]:
        """
        Lookup GeoIP untuk IP pakai geoiplookup (subprocess).
        Cache di database — tidak query ulang.
        """
        import subprocess
        
        # Skip private IPs
        if ip.startswith(("10.", "192.168.", "172.16.", "172.17.", "172.18.", "172.19.",
                          "172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.",
                          "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31.",
                          "127.")):
            return {"country": "Local", "country_code": "LO"}
        
        # Cek cache di database dulu
        try:
            conn = self._conn()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT country FROM ip_intelligence WHERE ip=? AND country IS NOT NULL AND country != ''",
                (ip,)
            )
            row = cursor.fetchone()
            conn.close()
            if row and row[0]:
                return {"country": row[0], "country_code": ""}
        except Exception:
            pass
        
        # Query geoiplookup
        try:
            result = subprocess.run(
                ["geoiplookup", ip],
                capture_output=True, text=True, timeout=3
            )
            output = result.stdout.strip()
            
            # Output: "GeoIP Country Edition: GB, United Kingdom"
            if ":" in output:
                parts = output.split(":", 1)[1].strip()
                if "," in parts:
                    code, country = parts.split(",", 1)
                    code = code.strip()
                    country = country.strip()
                    if country and country != "--":
                        # Simpan ke cache database
                        try:
                            conn = self._conn()
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE ip_intelligence SET country=? WHERE ip=?",
                                (country, ip)
                            )
                            conn.commit()
                            conn.close()
                        except Exception:
                            pass
                        return {"country": country, "country_code": code}
        except Exception as e:
            logger.debug(f"GeoIP lookup failed for {ip}: {e}")
        
        return {"country": "Unknown", "country_code": "??"}


    def _whitelist_filter(self, column: str = "ip") -> str:
        """Return SQL WHERE fragment untuk exclude whitelist."""
        if not WHITELIST_IPS:
            return "1=1"
        ips = ", ".join(f"'{ip}'" for ip in WHITELIST_IPS)
        return f"{column} NOT IN ({ips})"

    def get_stats(self, hours: int = 24) -> Dict[str, Any]:
        try:
            conn = self._conn()
            cursor = conn.cursor()
            since = (datetime.now() - timedelta(hours=hours)).isoformat()

            cursor.execute("""
                SELECT COUNT(*), COUNT(DISTINCT ip) FROM security_events
                WHERE timestamp >= ? OR created_at >= ?
            """, (since, since))
            total, unique_ips = cursor.fetchone()

            cursor.execute("""
                SELECT event_type, COUNT(*) FROM security_events
                WHERE timestamp >= ? OR created_at >= ?
                GROUP BY event_type
            """, (since, since))
            by_type = dict(cursor.fetchall())

            cursor.execute("""
                SELECT severity, COUNT(*) FROM security_events
                WHERE timestamp >= ? OR created_at >= ?
                GROUP BY severity
            """, (since, since))
            by_severity = dict(cursor.fetchall())

            conn.close()
            return {
                "period_hours": hours,
                "total_events": total or 0,
                "unique_ips": unique_ips or 0,
                "by_type": by_type,
                "by_severity": by_severity,
            }
        except Exception as e:
            logger.error(f"get_stats error: {e}")
            return {"error": str(e)}

    def get_events(self, limit: int = 50, event_type: Optional[str] = None,
                   severity: Optional[str] = None) -> List[Dict]:
        try:
            conn = self._conn()
            cursor = conn.cursor()
            wl = self._whitelist_filter("ip")
            query = f"""
                SELECT timestamp, ip, event_type, severity, username,
                       path, method, status_code, user_agent
                FROM security_events
                WHERE {wl}
            """
            params = []
            where = []
            if event_type:
                where.append("event_type = ?")
                params.append(event_type)
            if severity:
                where.append("severity = ?")
                params.append(severity)
            if where:
                query += " AND " + " AND ".join(where)
            query += " ORDER BY id DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            return [
                {
                    "timestamp": r[0], "ip": r[1], "event_type": r[2],
                    "severity": r[3], "username": r[4], "path": r[5],
                    "method": r[6], "status_code": r[7], "user_agent": r[8],
                }
                for r in rows
            ]
        except Exception as e:
            logger.error(f"get_events error: {e}")
            return []

    def get_top_attackers(self, limit: int = 10, hours: int = 24) -> List[Dict]:
        try:
            conn = self._conn()
            cursor = conn.cursor()
            since = (datetime.now() - timedelta(hours=hours)).isoformat()
            wl = self._whitelist_filter("ip")
            cursor.execute(f"""
                SELECT ip, total_hits, ssh_failed, nginx_scans, exploits,
                       ssh_success, threat_score, country, is_blocked
                FROM ip_intelligence
                WHERE last_seen >= ? AND {wl}
                ORDER BY threat_score DESC, total_hits DESC
                LIMIT ?
            """, (since, limit))
            rows = cursor.fetchall()
            conn.close()
            return [
                {
                    "ip": r[0], "total_hits": r[1], "ssh_failed": r[2],
                    "nginx_scans": r[3], "exploits": r[4], "ssh_success": r[5],
                    "threat_score": r[6], "country": r[7], "is_blocked": r[8],
                }
                for r in rows
            ]
        except Exception as e:
            logger.error(f"get_top_attackers error: {e}")
            return []

    def get_top_usernames(self, limit: int = 15) -> List[Dict]:
        try:
            conn = self._conn()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT username, count, unique_ips, success_count, last_seen
                FROM username_attempts
                WHERE success_count = 0 OR count > success_count
                ORDER BY count DESC LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            conn.close()
            return [
                {"username": r[0], "count": r[1], "unique_ips": r[2],
                 "success_count": r[3], "last_seen": r[4]}
                for r in rows
            ]
        except Exception as e:
            logger.error(f"get_top_usernames error: {e}")
            return []

    def get_top_patterns(self, limit: int = 15) -> List[Dict]:
        try:
            conn = self._conn()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pattern_type, count, unique_ips, last_seen
                FROM attack_patterns ORDER BY count DESC LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            conn.close()
            return [
                {"pattern_type": r[0], "count": r[1], "unique_ips": r[2], "last_seen": r[3]}
                for r in rows
            ]
        except Exception as e:
            logger.error(f"get_top_patterns error: {e}")
            return []

    def get_timeline(self, hours: int = 24) -> List[Dict]:
        try:
            conn = self._conn()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT hour_key, total_events, ssh_failed, nginx_scans
                FROM hourly_timeline
                ORDER BY hour_key DESC LIMIT ?
            """, (hours,))
            rows = cursor.fetchall()
            conn.close()
            return [
                {"hour": r[0], "total": r[1], "ssh_failed": r[2], "nginx_scans": r[3]}
                for r in rows
            ][::-1]
        except Exception as e:
            logger.error(f"get_timeline error: {e}")
            return []

    def get_top_user_agents(self, limit: int = 15) -> List[Dict]:
        try:
            conn = self._conn()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_agent, count, is_malicious, last_seen
                FROM user_agents ORDER BY count DESC LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            conn.close()
            return [
                {"user_agent": r[0], "count": r[1], "is_malicious": bool(r[2]), "last_seen": r[3]}
                for r in rows
            ]
        except Exception as e:
            logger.error(f"get_top_user_agents error: {e}")
            return []


# ── Singleton ───────────────────────────────────────────────
security_monitor = SecurityMonitor()


# ── Test standalone ─────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    print("=== TEST SECURITY MONITOR v2.0 ===\n")

    print("1. Scan all logs...")
    result = security_monitor.scan_all()
    print(f"   {result}\n")

    print("2. Stats 24 jam...")
    stats = security_monitor.get_stats(24)
    print(f"   Total: {stats.get('total_events', 0)}")
    print(f"   Unique IPs: {stats.get('unique_ips', 0)}")
    print(f"   By type: {stats.get('by_type', {})}")
    print(f"   By severity: {stats.get('by_severity', {})}\n")

    print("3. Top 10 attackers...")
    for a in security_monitor.get_top_attackers(10):
        print(f"   [{a['threat_score']:3d}] {a['ip']:20s} hits={a['total_hits']:6d} ssh={a['ssh_failed']:6d} scans={a['nginx_scans']}")
    print()

    print("4. Top 10 usernames...")
    for u in security_monitor.get_top_usernames(10):
        print(f"   {u['username']:20s} count={u['count']:6d} success={u['success_count']}")
    print()

    print("5. Top 10 attack patterns...")
    for p in security_monitor.get_top_patterns(10):
        print(f"   {p['pattern_type']:20s} count={p['count']:6d}")
    print()

    print("6. Timeline (last 10 hours)...")
    for t in security_monitor.get_timeline(10):
        print(f"   {t['hour']} | total={t['total']:6d} ssh={t['ssh_failed']:6d} nginx={t['nginx_scans']}")
    print()

    print("7. Last 10 events...")
    for e in security_monitor.get_events(10):
        print(f"   [{e['severity']:8s}] {e['ip']:20s} {e['event_type']:16s} {e.get('username') or e.get('path') or ''}")
