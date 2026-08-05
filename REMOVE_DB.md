# How to remove tracked db.sqlite3 from the repository

I cannot delete a tracked file from the git index from here, so please run the following commands locally to remove the checked-in SQLite DB and update the repository. These commands will remove db.sqlite3 from tracking while keeping the file locally (git rm --cached). Make sure you have a backup/export of any data you need before running them.

Commands:

```bash
# on your local machine
git checkout deploy-render
git pull origin deploy-render

# keep a backup copy just in case
cp db.sqlite3 db.sqlite3.backup

# stop tracking the file and commit
git rm --cached db.sqlite3
echo "db.sqlite3" >> .gitignore
git add .gitignore
git commit -m "Remove tracked sqlite DB and ignore it"

git push origin deploy-render
```

After you push, open the PR page and create the pull request from deploy-render → main:
https://github.com/yashkansal12/Paper-Trading-using-AI-strategies/compare/main...deploy-render?expand=1

If you'd like, I can attempt the removal on the branch for you, but I will need either a GitHub API scope that allows deleting files (not available via the current tools) or you can run the commands above locally and I will continue with Render guidance.
