#https://www.youtube.com/watch?v=n3uSyqoBgQI

import requests
from bs4 import BeautifulSoup
import random

url = "https://sslproxies.org/" 

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')


# Get all ips
row1 = soup.findAll('td')[::8]
parsed = map(lambda x:x.text, row1)
ips = []
# Check if the value is an ip
for ip in parsed:
    isIP = True
    for value in ip.split('.'):
        if(not value.isdigit()):
            isIP = False
    if(isIP):
        ips.append(ip)

# Get all ports
row2 = soup.findAll('td')[1::8]
parsed = map(lambda x:x.text, row2)
ports = []
for port in parsed:
    if (port.isdigit()):
        ports.append(port)
        

# for ip, port in zip(ips, ports):
#     print(ip + ":" + port)

def proxyRequest(url, **kwargs):
    while True:
        
        try:
            i = random.randint(0, len(ips))
            proxy = {'https' : ips[i] + ":" + ports[i]}
            print("Using proxy: " + proxy['https'])
            r = requests.request('get', url, proxies=proxy, timeout=5, **kwargs)
            break
        except:
            pass

    return r

# r = proxyRequest("https://youtube.com/")
# print(r.text.encode('utf-8'))


    

