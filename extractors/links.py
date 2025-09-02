import requests

def green(text):
    return f"\033[32m{text}\033[0m"

def red(text):
    return f"\033[31m{text}\033[0m"

def extract_links(soup, check_reachable=True, timeout=5):
    links = soup.find_all('a')
    found = False
    for link in links:
        href = link.get('href')
        if href and href.startswith(('http', 'https')):
            found = True
            print(green("[checking]:"), f"{href} ... ", end="")
            if not check_reachable:
                print("skipped reachability check")
                continue
            try:
                r = requests.get(href, timeout=timeout)
                if r.status_code == 200:
                    print(green("Reachable!"))
                else:
                    print(red(f"Returned status: "), green(f"{r.status_code}"))
            except Exception as e:
                print(red(f"Not reachable ({e})"))
    if not found:
        print(red("Doesn't contain any links!"))
