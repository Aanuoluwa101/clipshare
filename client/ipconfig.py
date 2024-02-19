import subprocess
import re

def get_wifi_configuration():
    wifi_config = []
    try:
        # Run the ipconfig command and capture the output
        result = subprocess.run(['ipconfig'], capture_output=True, text=True, check=True)
        #print(result)
        lines = result.stdout.split("\n")
        length = len(lines)
        for idx, line in enumerate(lines):
            if line == "Wireless LAN adapter Wi-Fi:" or line == "Wireless LAN adapter WiFi:":
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


def get_wifi_config_details(type):
    wifi_config = get_wifi_configuration()
    if not wifi_config:
        return None
    
    if type == "ip":
        pattern = re.compile(r'IPv4 Address.*?:\s*([\d.]+)')
    elif type == "subnet":
        pattern = re.compile(r'Subnet Mask.*?:\s*([\d.]+)')
    elif type == "gateway":
        pattern = re.compile(r'Default Gateway.*?:\s*([\d.]+)')

    for line in wifi_config:
        match = pattern.search(line)
        if match:
            return(match.group(1))
    return None



if __name__ == "__main__":
    print(get_wifi_config_details("ip"))
    