# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "humanize",
#     "requests",
#     "rich",
#     "tqdm",
# ]
# ///
import requests
import sys
import json
import humanize
from tqdm import tqdm
from urllib.parse import quote
from rich import print
from rich.prompt import Confirm


def total_caches() -> int:
    url = f"https://api.github.com/repos/{REPO}/actions/cache/usage"
    return requests.get(url, headers=HEADERS).json()["active_caches_count"]


def get_caches() -> list[dict]:
    url = f"https://api.github.com/repos/{REPO}/actions/caches"
    response = requests.get(
        url, headers=HEADERS, params={"per_page": PAGE_SIZE, "page": 1}
    )
    assert (
        response.status_code == 200
    ), f"Cache fetch failed with status code {response.status_code}: {json.loads(response.text)['message']}"

    caches = json.loads(response.text)["actions_caches"]
    cache_count = total_caches()
    if cache_count != 0:
        print("Fetching caches...")
        with tqdm(total=cache_count, leave=False) as progress:
            progress.update(PAGE_SIZE)
            while "next" in response.links.keys():
                response = requests.get(
                    response.links["next"]["url"],
                    headers=HEADERS,
                    params={"per_page": PAGE_SIZE},
                )
                progress.update(PAGE_SIZE)
                caches.extend(json.loads(response.text)["actions_caches"])

    if isinstance(caches, list) and len(caches) > 0:
        return caches
    else:
        print("No caches found")
        exit(0)


def get_total_cache_size(caches: list[dict]) -> float:
    total_size = 0
    for cache in caches:
        total_size += cache.get("size_in_bytes")
    return total_size


def clear_caches(caches: list[dict]):
    for cache in tqdm(caches, leave=False):
        response = requests.delete(
            f"https://api.github.com/repos/{REPO}/actions/caches?key={quote(cache['key'])}",
            headers=HEADERS,
        )
        try:
            assert (
                response.status_code == 200
            ), f"Cache deletion failed for key {cache['key']} with status code {response.status_code}: {json.loads(response.text)['message']}"
        except AssertionError as e:
            print(e)


if __name__ == "__main__":
    try:
        TOKEN = sys.argv[1]
        REPO = sys.argv[2]
    except IndexError:
        print("Invalid Arguments. Usage: clear-gha-cache.py <token> <repo>")
        sys.exit(1)

    HEADERS = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    PAGE_SIZE = 30

    caches = get_caches()

    total_cache_size = get_total_cache_size(caches)

    if Confirm.ask(
        f"Found [blue]{len(caches)}[/] caches totalling [blue]{humanize.naturalsize(total_cache_size)}[/] to delete, are you sure?",
        default=False,
    ):
        clear_caches(caches)
        print("Done!")
    else:
        print("Cancelled")
