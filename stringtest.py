from selenium import webdriver
import time
import json
import random

string = "Your confirmation code is 821218. Please enter it in the text field." 
for s in string.split():
    s = s.replace('.', '')
    if(s.isdigit()):
        print(s)