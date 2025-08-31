import sys, requests, webbrowser, re,  phonenumbers
from bs4 import BeautifulSoup

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

url = sys.stdin.readline().strip()
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

print("What do you want to extract?")
print("1: Links")
print("2: Phone numbers")
print("3: Emails (with domain verification)")
print("4: Locations (addresses)")

choice = input("Enter the number of your choice: ").strip()

def extract_links():
    links = soup.find_all('a')
    found = False
    for link in links:
        href = link.get('href')
        if href and href.startswith(('http', 'https')):
            found = True
            print(f"Checking {href} ... ", end="")
            try:
                r = requests.get(href, timeout=5)
                if r.status_code == 200:
                    print("Reachable!")
                else:
                    print(f"Returned status: {r.status_code}")
            except Exception as e:
                print(f"Not reachable ({e})")
    if not found:
        print("Doesn't contain any links!")

def extract_phone_numbers():
    # Find all digit groups that could be phone numbers
    possible_numbers = re.findall(r'\+?\d[\d\s\-\(\)]{8,}\d', response.text)
    valid_phones = set()
    for number in possible_numbers:
        try:
            parsed = phonenumbers.parse(number, None)
            if phonenumbers.is_valid_number(parsed):
                valid_phones.add(phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
        except phonenumbers.phonenumberutil.NumberParseException:
            continue
    if not valid_phones:
        print("Doesn't contain any valid phone numbers!")
    else:
        for number in valid_phones:
            print(number)


def extract_emails():
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    emails = set(re.findall(email_pattern, response.text))
    if not emails:
        print("Doesn't contain any emails!")
    else:
        for email in emails:
            print(f"{email} ", end="")
            if DNS_AVAILABLE:
                domain = email.split('@')[1]
                try:
                    dns.resolver.resolve(domain, 'MX')
                    print("[domain has MX records]")
                except Exception:
                    print("[domain has NO MX records!]")
            else:
                print("[domain verification unavailable: dnspython not installed]")


def extract_locations():
    # Get all visible text from the page
    page_text = soup.get_text(separator=' ', strip=True)
    address_pattern = re.compile(r'([A-Za-z\s\.,\-]+,\s*[A-Za-z\s\.,\-]+,\s*[A-Za-z\s\.,\-]+)')
    addresses = set(re.findall(address_pattern, page_text))
    def verify_address(address):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': address,
            'format': 'json',
            'addressdetails': 1,
            'limit': 1,
        }
        headers = {
            'User-Agent': 'AddressVerifier/1.0'
        }
        response = requests.get(url, params=params, headers=headers)
        results = response.json()
        if results:
            print(f"{address} [VALID] Lat: {results[0]['lat']}, Lon: {results[0]['lon']}")
        else:
            print(f"{address} [NOT FOUND]")
    if not addresses:
        print("No addresses found!")
    else:
        for address in addresses:
            verify_address(address)

if choice == '1':
    extract_links()
elif choice == '2':
    extract_phone_numbers()
elif choice == '3':
    extract_emails()
elif choice == '4':
    extract_locations()
else:
    print("Invalid choice! Please enter a number between 1 and 4.")