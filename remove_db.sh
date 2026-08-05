#!/bin/bash
# backup and untrack db.sqlite3 (run locally)
set -e
cp db.sqlite3 db.sqlite3.backup
git rm --cached db.sqlite3
if ! grep -qxF "db.sqlite3" .gitignore; then
  echo "db.sqlite3" >> .gitignore
  git add .gitignore
fi
git commit -m "Remove tracked sqlite DB and ignore it" || echo "No changes to commit"
git push origin deploy-render

echo "db.sqlite3 removed from tracking and pushed to deploy-render branch"
