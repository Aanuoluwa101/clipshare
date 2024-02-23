"""Defines several utility functions"""

import subprocess
import re
import random


def get_all_wifi_configs():
    """Retrieves the wifi configuration section of the ipconfig output

    Returns:
    list: all wifi configuration details
    """
    wifi_config = []
    try:
        result = subprocess.run(
            ["ipconfig"], capture_output=True, text=True, check=True
        )
        lines = result.stdout.split("\n")
        for idx, line in enumerate(lines):
            if (
                line == "Wireless LAN adapter Wi-Fi:"
                or line == "Wireless LAN adapter WiFi:"
            ):
                start = idx
                try:
                    for i in range(start, start + 10):
                        wifi_config.append(lines[i])
                except IndexError:
                    pass
        return wifi_config
    except subprocess.CalledProcessError as e:
        print(f"Error running ipconfig: {e}")
        return wifi_config


def get_one_wifi_config(type):
    """Retrieves a specific wifi config detail

    Parameters:
    type (str): the wifi config detail to be retrieved.
                Possible values are 'ip', 'subnet', 'gateway'

    Returns:
    str: the wifi configuration retrieved
    """
    wifi_config = get_all_wifi_configs()
    if not wifi_config:
        return None

    if type == "ip":
        pattern = re.compile(r"IPv4 Address.*?:\s*([\d.]+)")
    elif type == "subnet":
        pattern = re.compile(r"Subnet Mask.*?:\s*([\d.]+)")
    elif type == "gateway":
        pattern = re.compile(r"Default Gateway.*?:\s*([\d.]+)")

    for line in wifi_config:
        match = pattern.search(line)
        if match:
            return match.group(1)
    return None


def get_server_name():
    """Fetches the server name from a file

    Returns:
    str: the name of the server

    Raises:
    FileNotFoundError: raises a value error if the server name file is not found
    """
    try:
        with open("server_name") as file:
            return file.readline().strip()
    except FileNotFoundError:
        raise FileNotFoundError("Server name file not found")


def generate_passcode():
    """Generates a passcode for the server

    Returns:
    str: the passcode
    """
    return str(random.randint(1000, 9999))


if __name__ == "__main__":
    print(get_one_wifi_config("ip"))
