@echo off
git branch -D latest_branch
git checkout --orphan latest_branch
git add .
git commit -m "upload"
git branch -D main
git branch -m main
git push -f origin main