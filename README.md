```markdown
#  Web Scraper

A compact, terminal-first Python web scraper for fetching a page and extracting links, phone numbers, emails (optional MX verification) and addresses. The project is modular, CLI-friendly, prints a small ASCII banner on startup, and exits quietly on Ctrl+C.

## Requirements

A cleaned `requirements.txt` is included in this repository with the packages needed:

- pyfiglet>=0.8.1
- colorama>=0.4.6
- requests>=2.28.2
- beautifulsoup4>=4.12.2
- phonenumbers>=8.13.12
- dnspython>=2.4.2
- Pillow>=9.5.0

Notes:
- `dnspython` is optional and only required if you want MX-record verification when extracting emails.
- `Pillow` is optional and only required for features that need image processing.

## Install system packages (Debian / Ubuntu)

Install Python 3 and pip3 first (administrator privileges may be required):

```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

(If you use another OS or package manager, install the equivalent Python 3 and pip packages for your platform.)

## Install Python dependencies

From the project root run:

```bash
python3 -m pip install -r requirements.txt
```

Tip: use a virtual environment to avoid modifying the system Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

To regenerate or update `requirements.txt` after adding new dependencies, you can:
- Install the new packages in your virtualenv and run `python3 -m pip freeze > requirements.txt` (pins exact versions), or
- Use `pipreqs .` (installable via `python3 -m pip install pipreqs`) to generate a requirements file based on imports in the project.

## Usage

The scraper can operate non-interactively (URL via stdin) or interactively.

Examples:

- Non-interactive, choose option 1 (links) on the command line:
```bash
echo "https://example.com/" | python3 webscraper.py --choice 1
```

- Non-interactive, provide URL via stdin and interrupt early (script exits quietly on Ctrl+C):
```bash
echo "https://example.com/" | python3 webscraper.py
```

- Interactive mode (run and type/paste URL when prompted):
```bash
python3 webscraper.py
# then enter the URL and follow the menu prompts
```

After the page is fetched you will be prompted to choose:
1 — Links (optionally checks reachability)
2 — Phone numbers
3 — Emails (optional MX verification if dnspython installed)
4 — Locations (address lookup via OpenStreetMap Nominatim)

The program prints a banner on startup and will exit quietly with code 0 if you press Ctrl+C.

## Behavior & troubleshooting

- If a dependency is missing you'll get an ImportError when running; make sure you installed the packages from `requirements.txt` with the same `python3` interpreter used to run the script.
- The scraper uses `requests` timeouts to stay responsive; network errors are printed but won't crash the process.
- Email domain MX checks are attempted only if `dnspython` is available — otherwise the script will still extract emails but report that domain verification is unavailable.
- If you want to disable the ASCII banner, open `triangle.py` or remove the import/call from `webscraper.py`.

## Contributing

Feel free to add new extractors (place under `extractors/`) and update `requirements.txt` accordingly. For reproducible installs in CI, prefer pinned versions using `pip freeze` or a lockfile.

---
Enjoy using Triangle Web Scraper!
```