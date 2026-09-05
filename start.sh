#!/bin/bash
# start.sh - One Click Start Inkside Digital

echo "🚀 Starting Inkside Digital..."

# Aktifkan venv
cd ~/consciousness-intelligence
source venv/bin/activate

# Jalankan server
nohup python main.py > server.log 2>&1 &

echo "✅ Server started at http://45.41.204.21"
echo "📡 API running at http://45.41.204.21:5000"
