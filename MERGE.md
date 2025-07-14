# How to Merge `s04-assignment` into `main`

## 1. Merge via GitHub Pull Request (Recommended)

1. Go to your repository on GitHub: https://github.com/chakkasanthosh21/AIE7
2. You should see a prompt to "Compare & pull request" for `s04-assignment`.
3. Click it, review the changes, and submit the pull request.
4. After review, click "Merge pull request" to merge into `main`.

---

## 2. Merge via GitHub CLI

If you prefer the command line and have the GitHub CLI installed:

```sh
gh pr create --base main --head s04-assignment --title "Merge s04-assignment" --body "Cleaned history and ready to merge"
gh pr merge --merge
```

- Make sure you are authenticated with `gh auth login` if needed.

---

## Notes
- The `.venv` directory and all large files have been removed from git history.
- Always use a `.gitignore` to avoid committing virtual environments or large files. 