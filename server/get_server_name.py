def get_server_name():
    try:
        with open("server_name") as file:
            return file.readline()
    except Exception as e:
        return "server name not found"
        
    
if __name__ == "__main__":
    print(get_server_name())