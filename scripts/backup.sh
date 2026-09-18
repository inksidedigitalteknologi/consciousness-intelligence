#!/bin/bash
# Backup memory.db + config — v2 (KEEP=3, skip-if-unchanged, cleanup legacy)
# Patch 2026-09-18

BACKUP_DIR="/root/consciousness-intelligence/backups"
LEGACY_DIR="/root/consciousness-intelligence/database/backup"
DB="/root/consciousness-intelligence/database/memory.db"
ENV_FILE="/root/consciousness-intelligence/.env"
HASH_FILE="$BACKUP_DIR/.last_db_hash"
KEEP=3
TS=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# ── 1. Backup DB (skip kalau tidak berubah) ─────────────────
if [ -f "$DB" ]; then
    CURRENT_HASH=$(md5sum "$DB" | awk '{print $1}')
    LAST_HASH=""
    [ -f "$HASH_FILE" ] && LAST_HASH=$(cat "$HASH_FILE")

    if [ "$CURRENT_HASH" = "$LAST_HASH" ]; then
        echo "[$(date)] ⏭️  DB tidak berubah (hash sama), skip backup"
    else
        cp "$DB" "$BACKUP_DIR/memory_$TS.db"
        echo "$CURRENT_HASH" > "$HASH_FILE"
        echo "[$(date)] ✅ DB backed up: memory_$TS.db"
    fi
else
    echo "[$(date)] ❌ DB not found: $DB"
fi

# ── 2. Backup .env ──────────────────────────────────────────
if [ -f "$ENV_FILE" ]; then
    cp "$ENV_FILE" "$BACKUP_DIR/env_$TS.bak"
    echo "[$(date)] ✅ .env backed up"
fi

# ── 3. Rotasi backup di $BACKUP_DIR ────────────────────────
cd "$BACKUP_DIR" || exit 0
ls -t memory_*.db 2>/dev/null | tail -n +$((KEEP+1)) | xargs -r rm
ls -t env_*.bak 2>/dev/null | tail -n +$((KEEP+1)) | xargs -r rm

# ── 4. Bersihkan legacy backup dari restart backend ────────
if [ -d "$LEGACY_DIR" ]; then
    COUNT=$(ls -1 "$LEGACY_DIR"/*.db 2>/dev/null | wc -l)
    if [ "$COUNT" -gt 0 ]; then
        ls -t "$LEGACY_DIR"/*.db 2>/dev/null | tail -n +2 | xargs -r rm
        echo "[$(date)] 🧹 Legacy backup dibersihkan (sisakan 1 terbaru, hapus $((COUNT-1)) file)"
    fi
fi

# ── 5. Ringkasan ───────────────────────────────────────────
DB_COUNT=$(ls memory_*.db 2>/dev/null | wc -l)
ENV_COUNT=$(ls env_*.bak 2>/dev/null | wc -l)
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1)
echo "[$(date)] ✅ Backup selesai — DB: $DB_COUNT file, ENV: $ENV_COUNT file, Total: $TOTAL_SIZE"
