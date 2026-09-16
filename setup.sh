#!/bin/bash
# setup.sh - One Click Setup

echo "🚀 Setting up Inkside Digital..."

cd ~/consciousness-intelligence

# Python
python3 -m venv venv
source venv/bin/activate
python install.py

# Frontend
cd frontend
npm install
npm run build
cd ..

# Start
nohup python main.py > server.log 2>&1 &

echo "✅ Setup Complete!"
echo "🌐 http://45.41.204.21"
