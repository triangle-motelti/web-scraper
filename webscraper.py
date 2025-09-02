#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup
import triangle
import argparse
from interactive_in import get_interactive_input

from extractors import extract_links, extract_phone_numbers, extract_emails, extract_locations

triangle.ascii_art("moteLti triangLe", font="slant", color="blue")

def green(text):
    return f"\033[32m{text}\033[0m"

def red(text):
    return f"\033[31m{text}\033[0m"

def main(url, choice):

    print(red("Scraping URL:"), url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(red(f"Failed to fetch {url}: {e}"))
        sys.exit(2)

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        import dns.resolver as dns_resolver
    except Exception:
        dns_resolver = None

    print(green("<What do you want to extract?>"))
    print(green("[0]: All (links, phone numbers, emails, locations)"))
    print(green("[1]: Links"))
    print(green("[2]: Phone numbers"))
    print(green("[3]: Emails (with domain verification)"))
    print(green("[4]: Locations (addresses)"))

    if choice is None:
        choice = get_interactive_input(green("<Enter the number of your choice:> "))
        if not choice:
            print(red("Error: No choice provided. Please enter a number between 1 and 4."))
            sys.exit(1)
    else:
        print(green(f"Selected choice: {choice}"))

    if choice not in ['0', '1', '2', '3', '4']:
        print(red("Invalid choice! Please enter a number between 1 and 4."))
        sys.exit(1)

    if choice == '0':
        extract_links(soup)
        extract_phone_numbers(response.text)
        extract_emails(response.text, dns_resolver)
        extract_locations(soup)
    elif choice == '1':
        extract_links(soup)
    elif choice == '2':
        extract_phone_numbers(response.text)
    elif choice == '3':
        extract_emails(response.text, dns_resolver)
    elif choice == '4':
        extract_locations(soup)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web scraper for extracting links, phone numbers, emails, or locations.")
    parser.add_argument('--choice', type=str, choices=['0', '1', '2', '3', '4'], help="Extraction choice (0: All, 1: Links, 2: Phone numbers, 3: Emails, 4: Locations)")
    args = parser.parse_args()

    try:
        if not sys.stdin.isatty():
            url = sys.stdin.readline().strip()
            if not url:
                print(red("No URL provided on stdin"))
                sys.exit(1)
        else:
            print(green("<put a link to the web page that you want to scrap>:"))
            url = input().strip()
            if not url:
                print(red("[No URL provided]"))
                sys.exit(1)

        main(url, args.choice)
    except KeyboardInterrupt:
        sys.exit(0)
