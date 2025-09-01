import re, phonenumbers

def extract_phone_numbers(text):
    """
    Extract possible phone numbers via regex, validate via phonenumbers lib.
    """
    possible_numbers = re.findall(r'\+?\d[\d\s\-\(\)]{8,}\d', text)
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
        for number in sorted(valid_phones):
            print(number)