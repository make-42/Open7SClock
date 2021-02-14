import requests

def geteuroprice():
    r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    rjson = r.json()
    return rjson["bpi"]["EUR"]["rate_float"]
