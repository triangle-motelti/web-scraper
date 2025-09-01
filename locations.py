import requests

def extract_locations(soup):
    address_element = soup.find('p', class_='text-gray-400 text-small')
    if address_element:
        address = address_element.get_text(strip=True)
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
        try:
            r = requests.get(url, params=params, headers=headers, timeout=10)
            results = r.json()
            if results:
                print(f"{address} [VALID] Lat: {results[0]['lat']}, Lon: {results[0]['lon']}")
            else:
                print(f"{address} [NOT FOUND]")
        except Exception as e:
            print(f"{address} [ERROR: {e}]")
    else:
        print("No address found!")