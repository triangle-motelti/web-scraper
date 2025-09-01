import requests

def extract_links(soup, check_reachable=True, timeout=5):
    links = soup.find_all('a')
    found = False
    for link in links:
        href = link.get('href')
        if href and href.startswith(('http', 'https')):
            found = True
            print(f"Checking {href} ... ", end="")
            if not check_reachable:
                print("skipped reachability check")
                continue
            try:
                r = requests.get(href, timeout=timeout)
                if r.status_code == 200:
                    print("Reachable!")
                else:
                    print(f"Returned status: {r.status_code}")
            except Exception as e:
                print(f"Not reachable ({e})")
    if not found:
        print("Doesn't contain any links!")