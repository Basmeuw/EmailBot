from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import random

emailUrl = 'https://passport.yandex.com/registration/mail?from=mail&require_hint=1&origin=hostroot_homer_reg_com&retpath=https%3A%2F%2Fmail.yandex.com%2F&backpath=https%3A%2F%2Fmail.yandex.com%3Fnoretpath%3D1'
phoneUrl = 'https://freephonenum.com/us'

names = []
surnames = []

with open('popularnames.json') as json_file:
    names = json.load(json_file)['names']
with open('popularsurnames.json') as json_file:
    surnames = json.load(json_file)['surnames']

emails = {}
with open('emails.json') as f:
    emails = json.load(f)

def genPass(name):
    return "X#" + name


driver = webdriver.Chrome('J:/Python/Insta/chromedriver_win32/chromedriver')
driver.maximize_window()

for i in range(0, 20):
    # Go to the website sign up
    driver.switch_to.window(driver.window_handles[0])
    driver.get(emailUrl)
    time.sleep(2)
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
    actions.move_by_offset(100 , 100).click().perform()
    numberDivs = driver.find_elements_by_class_name("col-lg-3")
    print("Number of phone numbers: " + str(len(numberDivs)))
    numberDiv = numberDivs[random.randint(0, 12)]
    button = numberDiv.find_element_by_xpath('.//a[@class = "numbers-btn btn btn-secondary btn-block "]')
    print("click")
    button.click()
    time.sleep(2)

    # Get phone number
    text = driver.find_element_by_xpath('.//h3[@class = "text-md"]').text
    phoneNumber = "+" + text.split("+")[1]
    phoneNumber = phoneNumber.replace('-', ' ')
    phoneNumber = phoneNumber[:13] + " " + phoneNumber[13:]
    print(phoneNumber)

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
    print(fullText)

    code = 0
    for s in fullText.split():
        s = s.replace('.', '')
        if(s.isdigit()):
            code = int(s)
            
    # Back the the sign up page
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    driver.find_element_by_id("phoneCode").send_keys(code)
    time.sleep(1)

    # Register button
    driver.find_element_by_xpath('.//button[@class = "control button2 button2_view_classic button2_size_l button2_theme_action button2_width_max button2_type_submit js-submit"]').click()
    # Accept privacy
    driver.find_element_by_xpath('.//button[@class = "control button2 button2_view_classic button2_size_m button2_theme_action button2_width_max"]').click()

    emails[username + "@yandex.com"] = password

    with open('emails.json', 'w') as f:
        json.dump(emails, f)
