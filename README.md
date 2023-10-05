# clear-gha-cache.py

This script deletes all GitHub Actions caches for a specified repository.

It will prompt you for conformation before proceeding.

## Usage

```bash
poetry run python clear-gha-cache.py <token> <repo>
```

Where:

- \<token> is a GitHub personal access token with `actions:read` and `actions:write`
- \<repo> is the repository name in owner/repo format e.g. octocat/hello-world.
