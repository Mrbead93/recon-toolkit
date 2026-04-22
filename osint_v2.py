import requests
import threading
from datetime import datetime, timezone

RESET  = "\033[0m"
GREEN  = "\033[32m"
CYAN   = "\033[36m"
RED    = "\033[31m"
YELLOW = "\033[33m"
BOLD   = "\033[1m"

results = {}
lock = threading.Lock()

def check_github(username):
    try:
        r = requests.get(
            f"https://api.github.com/users/{username}",
            timeout=5
        )
        if r.status_code == 200:
            d = r.json()
            with lock:
                results["github"] = {
                    "found"    : True,
                    "name"     : d.get("name", "N/A"),
                    "bio"      : d.get("bio", "N/A"),
                    "location" : d.get("location", "N/A"),
                    "repos"    : d.get("public_repos", 0),
                    "followers": d.get("followers", 0),
                    "created"  : d.get("created_at", "N/A")[:10],
                    "url"      : d.get("html_url", "N/A")
                }
        else:
            with lock:
                results["github"] = {"found": False}
    except Exception as e:
        with lock:
            results["github"] = {"found": False, "error": str(e)}

def check_reddit(username):
    try:
        headers = {"User-Agent": "osint-tool"}
        r = requests.get(
            f"https://www.reddit.com/user/{username}/about.json",
            headers=headers,
            timeout=5
        )
        if r.status_code == 200:
            d = r.json()["data"]
            ts = d.get("created_utc", 0)
            created = datetime.fromtimestamp(
                ts, tz=timezone.utc
            ).strftime("%Y-%m-%d")
            with lock:
                results["reddit"] = {
                    "found"  : True,
                    "name"   : d.get("name", "N/A"),
                    "karma"  : d.get("total_karma", 0),
                    "created": created,
                    "url"    : f"https://reddit.com/u/{username}"
                }
        else:
            with lock:
                results["reddit"] = {"found": False}
    except Exception as e:
        with lock:
            results["reddit"] = {"found": False, "error": str(e)}

def check_hackernews(username):
    try:
        r = requests.get(
            f"https://hacker-news.firebaseio.com/v0/user/{username}.json",
            timeout=5
        )
        if r.status_code == 200 and r.json():
            d = r.json()
            ts = d.get("created", 0)
            created = datetime.fromtimestamp(
                ts, tz=timezone.utc
            ).strftime("%Y-%m-%d")
            with lock:
                results["hackernews"] = {
                    "found"  : True,
                    "karma"  : d.get("karma", 0),
                    "created": created,
                    "url"    : f"https://news.ycombinator.com/user?id={username}"
                }
        else:
            with lock:
                results["hackernews"] = {"found": False}
    except Exception as e:
        with lock:
            results["hackernews"] = {"found": False, "error": str(e)}

def check_npm(username):
    try:
        r = requests.get(
            f"https://registry.npmjs.org/-/v1/search?text=maintainer:{username}&size=5",
            timeout=5
        )
        if r.status_code == 200:
            d = r.json()
            total = d.get("total", 0)
            packages = [
                obj["package"]["name"]
                for obj in d.get("objects", [])
            ]
            with lock:
                results["npm"] = {
                    "found"   : total > 0,
                    "total"   : total,
                    "packages": packages,
                    "url"     : f"https://www.npmjs.com/~{username}"
                }
        else:
            with lock:
                results["npm"] = {"found": False}
    except Exception as e:
        with lock:
            results["npm"] = {"found": False, "error": str(e)}

def check_pypi(username):
    try:
        r = requests.get(
            f"https://pypi.org/user/{username}/",
            timeout=5
        )
        if r.status_code == 200:
            with lock:
                results["pypi"] = {
                    "found": True,
                    "url"  : f"https://pypi.org/user/{username}/"
                }
        else:
            with lock:
                results["pypi"] = {"found": False}
    except Exception as e:
        with lock:
            results["pypi"] = {"found": False, "error": str(e)}

def print_results(username):
    found_count = sum(
        1 for v in results.values() if v.get("found")
    )
    total = len(results)

    print(f"\n{BOLD}{'='*45}{RESET}")
    print(f"  OSINT Report — {CYAN}{username}{RESET}")
    print(f"  Platforms found: {GREEN}{found_count}{RESET}/{total}")
    print(f"{BOLD}{'='*45}{RESET}\n")

    gh = results.get("github", {})
    print(f"  {BOLD}[ GitHub ]{RESET}")
    if gh.get("found"):
        print(f"  {GREEN}[FOUND]{RESET}  {gh['url']}")
        print(f"  Name     : {gh['name']}")
        print(f"  Bio      : {gh['bio']}")
        print(f"  Location : {gh['location']}")
        print(f"  Repos    : {gh['repos']}")
        print(f"  Followers: {gh['followers']}")
        print(f"  Created  : {gh['created']}")
    else:
        print(f"  {RED}[NOT FOUND]{RESET}")

    print()

    rd = results.get("reddit", {})
    print(f"  {BOLD}[ Reddit ]{RESET}")
    if rd.get("found"):
        print(f"  {GREEN}[FOUND]{RESET}  {rd['url']}")
        print(f"  Username : {rd['name']}")
        print(f"  Karma    : {rd['karma']}")
        print(f"  Created  : {rd['created']}")
    else:
        print(f"  {RED}[NOT FOUND]{RESET}")

    print()

    hn = results.get("hackernews", {})
    print(f"  {BOLD}[ HackerNews ]{RESET}")
    if hn.get("found"):
        print(f"  {GREEN}[FOUND]{RESET}  {hn['url']}")
        print(f"  Karma    : {hn['karma']}")
        print(f"  Created  : {hn['created']}")
    else:
        print(f"  {RED}[NOT FOUND]{RESET}")

    print()

    np = results.get("npm", {})
    print(f"  {BOLD}[ npm ]{RESET}")
    if np.get("found"):
        print(f"  {GREEN}[FOUND]{RESET}  {np['url']}")
        print(f"  Packages : {np['total']}")
        print(f"  Top pkgs : {', '.join(np['packages'])}")
    else:
        print(f"  {RED}[NOT FOUND]{RESET}")

    print()

    pp = results.get("pypi", {})
    print(f"  {BOLD}[ PyPI ]{RESET}")
    if pp.get("found"):
        print(f"  {GREEN}[FOUND]{RESET}  {pp['url']}")
    else:
        print(f"  {RED}[NOT FOUND]{RESET}")

    print(f"\n{BOLD}{'='*45}{RESET}\n")
    return found_count

def save_report(username, found_count):
    total = len(results)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"/data/data/com.termux/files/home/projects/python/osint_{username}_{timestamp}.txt"
    with open(filepath, "w") as f:
        f.write(f"OSINT Report\n")
        f.write(f"{'='*45}\n")
        f.write(f"Target    : {username}\n")
        f.write(f"Date      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Found on  : {found_count}/{total} platforms\n")
        f.write(f"{'='*45}\n\n")
        for platform, data in results.items():
            f.write(f"[ {platform.upper()} ]\n")
            if data.get("found"):
                for k, v in data.items():
                    if k != "found":
                        f.write(f"  {k}: {v}\n")
            else:
                f.write("  NOT FOUND\n")
            f.write("\n")
    print(f"  {GREEN}[SAVED]{RESET} osint_{username}_{timestamp}.txt\n")

print(f"\n{BOLD}=== OSINT Username Tool v2 ==={RESET}\n")
username = input("Enter username to search: ")
print(f"\n{YELLOW}[*] Searching {username} across 5 platforms...{RESET}\n")

threads = [
    threading.Thread(target=check_github,     args=(username,)),
    threading.Thread(target=check_reddit,     args=(username,)),
    threading.Thread(target=check_hackernews, args=(username,)),
    threading.Thread(target=check_npm,        args=(username,)),
    threading.Thread(target=check_pypi,       args=(username,))
]

for t in threads:
    t.start()
for t in threads:
    t.join()

found_count = print_results(username)
save_report(username, found_count)
