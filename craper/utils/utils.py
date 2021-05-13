def load_proxies(filename: str = 'proxies.txt', separator: str = '\n') -> list:
    """Reads proxies from a file and parses them to be ready to use with Python's `requests` library

    Args:
        filename (str, optional): Name of the file (.txt) where are the proxies located. Defaults to 'proxies.txt'.
        separator (str, optional): Separator by which is each proxy separated. Defaults to '\\n'
        
    Returns:
        formatted_proxy_list {list [dict]}: List of dictionaries, that are formatted and ready-to-use with Python
    """

    with open(filename, "r") as f:
        file_contents = f.read()
        file_contents = file_contents.split(separator)

    formatted_proxy_list = []
    try:
        try:
            # Userpass
            for i in range(0, len(file_contents)):
                if ":" in file_contents[i]:
                    tmp = file_contents[i]
                    tmp = tmp.split(":")
                    proxies = {
                        "http": "http://" + tmp[2] + ":" + tmp[3] + "@" + tmp[0] + ":" + tmp[1] + "/",
                        "https": "http://" + tmp[2] + ":" + tmp[3] + "@" + tmp[0] + ":" + tmp[1] + "/",
                    }
                    formatted_proxy_list.append(proxies)
        except:
            # IP auth
            for n in range(0, len(file_contents)):
                if ":" in file_contents[n]:
                    temp = file_contents[n]
                    proxies = {"http": "http://" + temp, "https": "http://" + temp}
                    formatted_proxy_list.append(proxies)
    except:
        return []
    return formatted_proxy_list
