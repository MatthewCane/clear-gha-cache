# clear-gha-cache.py

This script deletes all GitHub Actions caches for a specified repository.

## Installation

- Make sure [poetry](https://python-poetry.org/docs/#installation) is installed
- Install dependencies with `poetry install`

## Usage

```bash
poetry run python src/clear_gha_cache.py <token> <repo>
```

Where:

- \<token> is a GitHub personal access token with `actions:read` and `actions:write`
- \<repo> is the repository name in owner/repo format e.g. octocat/hello-world.

The script will prompt you for confirmation before proceeding.
