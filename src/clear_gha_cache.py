import requests, sys, json, humanize
from tqdm import tqdm
from urllib.parse import quote


def total_caches() -> int:
    url = f"https://api.github.com/repos/{REPO}/actions/cache/usage"
    return requests.get(url, headers=HEADERS).json()["active_caches_count"]


def get_caches():
    url = f"https://api.github.com/repos/{REPO}/actions/caches"
    response = requests.get(
        url, headers=HEADERS, params={"per_page": PAGE_SIZE, "page": 1}
    )
    assert (
        response.status_code == 200
    ), f"Cache fetch failed with status code {response.status_code}: {json.loads(response.text)['message']}"

    caches = json.loads(response.text)["actions_caches"]
    cache_count = total_caches()
    print(f"Fetching {cache_count} caches for {REPO}...")

    with tqdm(total=cache_count) as progress:
        progress.update(PAGE_SIZE)
        while "next" in response.links.keys():
            response = requests.get(
                response.links["next"]["url"],
                headers=HEADERS,
                params={"per_page": PAGE_SIZE},
            )
            progress.update(PAGE_SIZE)

            caches.extend(json.loads(response.text)["actions_caches"])
    progress.close()
    if isinstance(caches, list) and len(caches) > 0:
        return caches
    else:
        print("No caches found")
        exit(0)


def get_total_cache_size(caches: list[dict]):
    total_size = 0
    for cache in caches:
        total_size += cache.get("size_in_bytes")
    return total_size


def clear_caches(caches):
    for cache in tqdm(caches):
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

    if (
        input(
            f"Found {len(caches)} caches totalling {humanize.naturalsize(total_cache_size)} to delete, are you sure? (y/n) "
        )
        == "y"
    ):
        clear_caches(caches)
        print("Done!")
