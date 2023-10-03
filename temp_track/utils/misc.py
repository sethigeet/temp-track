from requests import get


def get_ip_addr() -> str:
    res = get("http://ipinfo.io/ip")
    return res.text
