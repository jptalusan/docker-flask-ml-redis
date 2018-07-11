import requests

def classify(): 
    uri = "http://163.221.68.242:8081/classify?f1=5.1&f2=3.5&f3=1.4&f4=0.2"
    resp = requests.get(uri)
    return resp.text
