import re

def is_valid_ip(ip):
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

    if ip_pattern.match(ip):
        return True
    return False

if __name__ == "__main__":
    print(is_valid_ip("123.232.2"))
