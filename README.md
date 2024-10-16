# Clear Github Actions Cache

This script deletes all GitHub Actions cache entries for a specified repository.

## Installation

1. Clone this repository locally (it is currently not available on PyPi)
2. Ensure [uv](https://docs.astral.sh/uv/getting-started/installation/) is installed

## Usage

```bash
uv run python clear_gha_cache.py <github token> <username>/<repo>
```

`<github token>` is a GitHub personal access token with `actions:read` and `actions:write`. If you have the Github CLI installed you can use `gh auth token` to generate one, for example:

```bash
uv run python clear_gha_cache.py $(gh auth token) octocat/hello-world
```

The script will prompt you for confirmation before proceeding.
