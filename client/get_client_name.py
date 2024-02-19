def get_client_name():
    try:
        with open("client_name") as file:
            return file.readline()
    except Exception:
        return "Client name not found"
        
    
if __name__ == "__main__":
    print(get_client_name())