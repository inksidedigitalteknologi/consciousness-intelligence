#!/bin/bash
set -e

echo "🔨 Building frontend..."
cd "$(dirname "$0")"
npm run build

echo "📦 Deploying to /var/www/inkside..."
rm -rf /var/www/inkside/*
cp -r dist/* /var/www/inkside/

echo "✅ Deployed! Files:"
ls -la /var/www/inkside/
