import random

def generate_passcode():
    return str(random.randint(1000, 9999))

if __name__ == "__main__":
    print(generate_passcode())
