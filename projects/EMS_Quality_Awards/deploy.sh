#!/bin/bash
# Deploy to ppakpoomm/EMS_Quality_Awards
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_URL="https://github.com/ppakpoomm/EMS_Quality_Awards.git"
TARGET_DIR="${1:-/tmp/EMS_Quality_Awards-deploy}"

echo "📦 Cloning EMS_Quality_Awards..."
rm -rf "$TARGET_DIR"
git clone "$REPO_URL" "$TARGET_DIR" 2>/dev/null || git init "$TARGET_DIR"

cd "$TARGET_DIR"
git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"

echo "📋 Copying files..."
rsync -av --delete \
  --exclude='.git' \
  --exclude='deploy.sh' \
  "$SCRIPT_DIR/" ./

git add -A
git commit -m "feat: EMS Quality Awards tracker — อปท.มาตรฐาน 2569" || echo "Nothing to commit"
git branch -M main
git push -u origin main

echo "✅ Deployed to $REPO_URL"
