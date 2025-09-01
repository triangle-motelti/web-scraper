#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup
import triangle

from extractors import extract_links, extract_phone_numbers, extract_emails, extract_locations


def main():
    triangle.ascii_art("moteLti triangLe", font="slant", color="blue")

    print("put a link to the web page that you want to scrap:")
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

    try:
        import dns.resolver as dns_resolver
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

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
