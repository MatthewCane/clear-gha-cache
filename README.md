# Clear Github Actions Cache

This script deletes all GitHub Actions cache entries for a specified repository.

## Installation

1. Clone this repository locally (it is currently not available on PyPi)
2. Ensure [uv](https://docs.astral.sh/uv/getting-started/installation/) is installed

## Usage

```bash
uv run python clear_gha_cache.py <token> <repo> [--keys-starting-with <string>]
```

`<repo>` must include the owner and the repository name, e.g. `octocat/hello-world`

`<github token>` is a GitHub personal access token with `actions:read` and `actions:write`. If you have the Github CLI installed you can use `gh auth token` to generate one, for example:

```bash
uv run python clear_gha_cache.py $(gh auth token) octocat/hello-world
```

The `--keys-starting-with` flag will filter the cache entries by their starting string, for example:

```bash
uv run python clear_gha_cache.py $(gh auth token) octocat/hello-world --keys-starting-with venv
```

will only match cache keys starting with `venv`.

The script will prompt you for confirmation before proceeding.
