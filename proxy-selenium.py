#https://www.youtube.com/watch?v=n3uSyqoBgQI
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
import requests
from bs4 import BeautifulSoup
import random
import urllib3
from colorama import Fore

def isProxyWorking(proxy):
    url = "https://google.com"
    try:
        requests.get(url, proxies={'https':'https://'+proxy}, timeout=(3.05,27))
    except requests.exceptions.ConnectionError as e:
        print(Fore.RED+'Error',e)
        return e
    except requests.exceptions.ConnectTimeout as e:
        print(Fore.RED+'ERROR! Connection timeout',e)
        return e
    except requests.exceptions.HTTPError as e:
        print(Fore.RED+'Error code',e.code)
        return e.code
    except requests.exceptions.Timeout as e:
        print(Fore.RED+'Error! Connection Timeout!',e)
        return e
    except urllib3.exceptions.ProxySchemeUnknown as e:
        print(Fore.RED+'ERROR',e)
        return e
    


def getProxies():
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
    proxies = []
    for ip, port in zip(ips, ports):
        proxies.append(ip + ":" + port)

    return proxies

def getRandomProxy(proxies):
    for i in range(0, 20):
        proxy = proxies[random.randint(0, len(proxies) - 1)]
        print("Checking proxy: %s" % proxy)
        if(isProxyWorking(proxy)):
            return proxy
            break
    return None

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

# Set up the webdriver with a proxy
allProxies = getProxies()       
proxyName = getRandomProxy(allProxies)
print("Chosen proxy: " + proxyName)

proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = proxyName
proxy.socks_proxy = proxyName
proxy.ssl_proxy = proxyName

capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)

driver = webdriver.Chrome('J:/Python/Insta/chromedriver_win32/chromedriver', desired_capabilities=capabilities)
driver.maximize_window()

driver.get("https://www.whatsmyip.org/")

    

