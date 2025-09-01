import re

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

def extract_emails(text, dns_resolver=None):
    """
    Find emails in text. If dns_resolver (module) is passed, verify MX records.
    dns_resolver should be the imported dns.resolver module or None.
    """
    emails = set(re.findall(EMAIL_RE, text))
    if not emails:
        print("Doesn't contain any emails!")
        return

    for email in sorted(emails):
        print(f"{email} ", end="")
        if dns_resolver is not None:
            domain = email.split('@', 1)[1]
            try:
                dns_resolver.resolve(domain, 'MX')
                print("[domain has MX records]")
            except Exception:
                print("[domain has NO MX records!]")
        else:
            print("[domain verification unavailable: dnspython not installed]")