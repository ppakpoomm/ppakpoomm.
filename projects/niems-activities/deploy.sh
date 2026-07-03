#!/bin/bash
# Deploy projects/niems-activities/ to ppakpoomm/niems-activities repo
# Run this locally with push access to niems-activities

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${1:-../niems-activities-clone}"

echo "📦 Cloning niems-activities..."
git clone https://github.com/ppakpoomm/niems-activities.git "$TARGET_DIR" 2>/dev/null || true
cd "$TARGET_DIR"

echo "📋 Copying files..."
rsync -av --delete \
  --exclude='.git' \
  --exclude='deploy.sh' \
  "$SCRIPT_DIR/" ./

echo "🚀 Committing and pushing..."
git add -A
git status
git commit -m "feat: ระบบติดตาม อปท.มาตรฐาน/คุณภาพ NIEMS" || echo "Nothing to commit"
git push origin main

echo "✅ Deployed to https://github.com/ppakpoomm/niems-activities"
