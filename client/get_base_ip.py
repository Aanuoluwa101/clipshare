from ipconfig import get_wifi_config_details


def get_base_ip():
    subnet_mask = get_wifi_config_details("subnet")
    gateway = get_wifi_config_details("gateway")

    subnet_octects = subnet_mask.split(".")
    gateway_octects = gateway.split(".")

    for idx, octect in enumerate(subnet_octects):
        if octect == "0":
            break
    return ".".join(gateway_octects[:idx]) + "."

if __name__ == "__main__":    
    print(get_base_ip())