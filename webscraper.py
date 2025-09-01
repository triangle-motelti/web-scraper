#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup
import triangle

# import your modular extractors
from extractors import extract_links, extract_phone_numbers, extract_emails, extract_locations

triangle.ascii_art("motelti   triangle scraper", font="slant", color="blue")
# read URL from stdin (like your original)
url = sys.stdin.readline().strip()
if not url:
    print("No URL provided on stdin")
    sys.exit(1)

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except Exception as e:
    print(f"Failed to fetch {url}: {e}")
    sys.exit(2)

soup = BeautifulSoup(response.text, 'html.parser')

# Detect dnspython optionally and pass resolver module to the email extractor
try:
    import dns.resolver as dns_resolver  # type: ignore
except Exception:
    dns_resolver = None

print("What do you want to extract?")
print("1: Links")
print("2: Phone numbers")
print("3: Emails (with domain verification)")
print("4: Locations (addresses)")

choice = input("Enter the number of your choice: ").strip()

if choice == '1':
    extract_links(soup)
elif choice == '2':
    extract_phone_numbers(response.text)
elif choice == '3':
    extract_emails(response.text, dns_resolver)
elif choice == '4':
    extract_locations(soup)
else:
    print("Invalid choice! Please enter a number between 1 and 4.")