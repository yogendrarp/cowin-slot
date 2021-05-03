import requests

def make_get_call(url):
    return(requests.get(url, headers={"User-Agent":"PostmanRuntime/7.26.8"}, allow_redirects=True, stream=False))