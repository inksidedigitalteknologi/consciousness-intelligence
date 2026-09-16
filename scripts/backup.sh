#!/bin/bash
# Backup memory.db + config

BACKUP_DIR="/root/consciousness-intelligence/backups"
DB="/root/consciousness-intelligence/database/memory.db"
KEEP=7
TS=$(date +%Y%m%d_%H%M%S)

# Backup DB
if [ -f "$DB" ]; then
    cp "$DB" "$BACKUP_DIR/memory_$TS.db"
    echo "[$(date)] ✅ DB backed up: memory_$TS.db"
else
    echo "[$(date)] ❌ DB not found: $DB"
fi

# Backup .env
if [ -f "/root/consciousness-intelligence/.env" ]; then
    cp "/root/consciousness-intelligence/.env" "$BACKUP_DIR/env_$TS.bak"
    echo "[$(date)] ✅ .env backed up"
fi

# Rotasi — hapus backup lebih dari $KEEP
cd "$BACKUP_DIR"
ls -t memory_*.db 2>/dev/null | tail -n +$((KEEP+1)) | xargs -r rm
ls -t env_*.bak 2>/dev/null | tail -n +$((KEEP+1)) | xargs -r rm

echo "[$(date)] ✅ Backup selesai — total: $(ls memory_*.db 2>/dev/null | wc -l) file"
