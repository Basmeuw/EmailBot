from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options 
from bs4 import BeautifulSoup
import requests
import time
import json
import random
import urllib3
from colorama import Fore

emailUrl = 'https://passport.yandex.com/registration/mail?from=mail&require_hint=1&origin=hostroot_homer_reg_com&retpath=https%3A%2F%2Fmail.yandex.com%2F&backpath=https%3A%2F%2Fmail.yandex.com%3Fnoretpath%3D1'
phoneUrl = 'https://freephonenum.com/us'

names = []
surnames = []
emails = {}

with open('popularnames.json') as json_file:
    names = json.load(json_file)['names']
with open('popularsurnames.json') as json_file:
    surnames = json.load(json_file)['surnames']

with open('emails.json') as f:
    emails = json.load(f)

def genPass(name):
    return "X#" + name

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
    return None

def isProxyWorking(proxy):
    url = "https://google.com"
    try:
        requests.get(url, proxies={'https':'https://'+proxy}, timeout=(3.05,27))
    except requests.exceptions.ConnectionError as e:
        # print(Fore.RED+'Error',e)
        return False
    except requests.exceptions.ConnectTimeout as e:
        # print(Fore.RED+'ERROR! Connection timeout',e)
        return False
    except requests.exceptions.HTTPError as e:
        # print(Fore.RED+'Error code',e.code)
        return False
    except requests.exceptions.Timeout as e:
        # print(Fore.RED+'Error! Connection Timeout!',e)
        return False
    except urllib3.exceptions.ProxySchemeUnknown as e:
        # print(Fore.RED+'ERROR',e)
        return False
    return True

def setupNewDriver():
    # Set up the webdriver with a proxy
    print("------Creating new driver------")
    allProxies = getProxies()       
    proxyName = getRandomProxy(allProxies)
    print("Using proxy: %s" % proxyName)
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = proxyName
    proxy.socks_proxy = proxyName
    proxy.ssl_proxy = proxyName

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--enable-javascript")

    capabilities = webdriver.DesiredCapabilities.CHROME
    proxy.add_to_capabilities(capabilities)

    driver = webdriver.Chrome('J:/Python/Insta/chromedriver_win32/chromedriver', desired_capabilities=capabilities, chrome_options=options)
    driver.maximize_window()
    return driver


while True:
    driver = setupNewDriver()
    # Use every proxy 10 times
    for i in range(0, 10):
        try:
            # Go to the website sign up
            driver.switch_to.window(driver.window_handles[0])
            driver.get(emailUrl)
            time.sleep(5)
            print(driver.find_element_by_tag_name('body').get_attribute('innerHTML'))
            # Create details
            firstName = names[random.randint(0, len(names))]
            lastName = surnames[random.randint(0, len(surnames))]
            username = firstName + lastName + str(random.randint(100, 999))
            password = genPass(username)

            # Enter the details
            driver.find_element_by_id("firstname").send_keys(firstName)
            time.sleep(0.5)
            driver.find_element_by_id("lastname").send_keys(lastName)
            time.sleep(0.5)
            driver.find_element_by_id("login").send_keys(username)
            time.sleep(0.5)
            driver.find_element_by_id("password").send_keys(password)
            time.sleep(0.5)
            driver.find_element_by_id("password_confirm").send_keys(password)
            time.sleep(0.5)

            #Open new tab with fake phone number
            driver.execute_script("window.open('');")
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1)
            driver.get(phoneUrl)
            time.sleep(1.5)

            # Get all phone numbers
            actions = ActionChains(driver)
            actions.move_to_element_with_offset(driver.find_element_by_tag_name('body'), 0,0)
            # actions.move_by_offset(100 , 100).click().perform()
            numberDivs = driver.find_elements_by_class_name("col-lg-3")
            # print("Number of phone numbers: " + str(len(numberDivs)))
            numberDiv = numberDivs[random.randint(0, 12)]
            # button = numberDiv.find_element_by_xpath('.//a[@class = "numbers-btn btn btn-secondary btn-block "]')
            button = numberDiv.find_element_by_xpath('.//a[@href]')
            button.click()
            time.sleep(2)

            # Get phone number
            text = driver.find_element_by_xpath('.//h3[@class = "text-md"]').text
            phoneNumber = "+" + text.split("+")[1]
            phoneNumber = phoneNumber.replace('-', ' ')
            phoneNumber = phoneNumber[:13] + " " + phoneNumber[13:]
            print("Phone number: %s" % phoneNumber)

            # Switch back to the login
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
            driver.find_element_by_id("phone").send_keys(phoneNumber)
            time.sleep(0.5)
            sendDiv = driver.find_element_by_xpath('.//div[@class = "registration__send-code show-block"]')
            sendDiv.find_element_by_tag_name("button").click()
            time.sleep(0.5)

            # Back to phone to get the code
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(7)
            driver.refresh()
            time.sleep(1)

            # Get the code
            table = driver.find_element_by_xpath('.//div[@class = "col-lg-9"]')
            tbody = table.find_element_by_tag_name("tbody")
            tr = tbody.find_element_by_tag_name("tr")
            fullText = tr.find_elements_by_tag_name("td")[2].text


            code = 0
            for s in fullText.split():
                s = s.replace('.', '')
                if(s.isdigit()):
                    code = int(s)
            print("Confirmation code: %s" % str(code))    
            # Back the the sign up page
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
            driver.find_element_by_id("phoneCode").send_keys(code)
            time.sleep(1)

            # Register button
            driver.find_element_by_xpath('.//button[@class = "control button2 button2_view_classic button2_size_l button2_theme_action button2_width_max button2_type_submit js-submit"]').click()
            time.sleep(1.5)
            # Accept privacy
            driver.find_element_by_xpath('.//button[@class = "control button2 button2_view_classic button2_size_m button2_theme_action button2_width_max"]').click()

            emails[username + "@yandex.com"] = password
            print("Created new account: %s@yandex.com" % username)
            print("Password: %s" % password)
            print("------Next-------")

            with open('emails.json', 'w') as f:
                json.dump(emails, f)

        except Exception as e:
            print(str(e))
            driver.close()
            driver.quit()
            time.sleep(10)
            driver = setupNewDriver()

