from selenium import webdriver
import time
import json
import random

url = 'https://protonmail.com/signup'

names = []
surnames = []

with open('popularnames.json') as json_file:
    names = json.load(json_file)['names']
with open('popularsurnames.json') as json_file:
    surnames = json.load(json_file)['surnames']

emails = {}
emails['KristopherButler925@protonmail.com'] = "X#KristopherButler925"

def genPass(name):
    return "X#" + name


driver = webdriver.Chrome('J:/Python/Insta/chromedriver_win32/chromedriver')
# Go to the sign up page
driver.get(url)
time.sleep(2)
# Open the free plan
driver.find_element_by_class_name('panel-heading').click()
time.sleep(2)
# Click on the free plan
driver.find_element_by_id('freePlan').click()
time.sleep(2)

# Enter the account details
username = names[random.randint(0, len(names))] + surnames[random.randint(0, len(surnames))] + str(random.randint(100, 999))
print("Username: " + username)
driver.find_element_by_id('username').send_keys(username)
time.sleep(1)

password = genPass(username)
print("Password: " + password)
driver.find_element_by_id('password').send_keys(password)
time.sleep(1)

driver.find_element_by_id('passwordc').send_keys(password)
time.sleep(1)

# Click sign up button
driver.find_element_by_class_name('signUpProcess-btn-create').click()
time.sleep(1)
# Click on the warning
driver.find_element_by_id('confirmModalBtn').click()
time.sleep(3)

#Click on the verify by email button
driver.find_element_by_class_name('humanVerification-block-email').click()
time.sleep(1)
# Type in previous email with which this account is going to be verified
email = list(emails)[0]
driver.find_element_by_id('emailVerification').send_keys(email)
time.sleep(0.5)
# Send email
driver.find_element_by_xpath("//*[@class='pm_button primary codeVerificator-btn-send']").click()
time.sleep(0.5)

#Open a new tab
driver.execute_script("window.open('');")
time.sleep(2)
# Switch to the new window
driver.switch_to.window(driver.window_handles[1])
driver.get("https://mail.protonmail.com/login")
time.sleep(2)

# Enter details
driver.find_element_by_id('username').send_keys(email)
time.sleep(0.5)
password = emails[email]
driver.find_element_by_id('password').send_keys(password)
time.sleep(0.5)
driver.find_element_by_id('login_btn').click()
time.sleep(3)



with open('emails.json', 'w') as f:
    json.dump()
