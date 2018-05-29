#!/usr/bin/python3
import os
import time
import requests
from selenium import webdriver


class SNKRS_LOGIN:
    def __init__(self):
        self.driver = webdriver.Chrome(f'{os.getcwd()}/chromedriver')
        self.cookies = None
        self.session = requests.session()

    def login(self, username_email, password, by_js=0):
        self.driver.get('https://www.nike.com/launch/')

        # TODO: figure out a less hack way to click button
        js_login_click = "document.getElementsByClassName('js-log-in small text-color-grey d-sm-ib va-sm-m mr4-sm')[0].click()"
        self.driver.execute_script(js_login_click)

        # Wait until modal visible
        time.sleep(1)

        if by_js:
            get_and_type_username_js = """var i=0;\
var login_modal=document.getElementsByClassName('nike-unite-text-input emailAddress nike-unite-component empty')[0].children;
for (i=0; i<login_modal.length; i++){{\
if (login_modal[i].tagName.toLowerCase() == 'input'){{\
login_modal[i].value = '{}'\
}};}}""".format(username_email)
            self.driver.execute_script(get_and_type_username_js)

            get_and_type_password_js = """var i=0;\
var login_modal=document.getElementsByClassName('nike-unite-text-input password nike-unite-password-input nike-unite-component empty')[0].children;
for (i=0; i<login_modal.length; i++){{\
if (login_modal[i].tagName.toLowerCase() == 'input'){{\
login_modal[i].value = '{}'\
}};}}""".format(password)
            self.driver.execute_script(get_and_type_password_js)
            time.sleep(1)

            get_and_click_login_button = """var i=0;\
var login_modal=document.getElementsByClassName('nike-unite-submit-button loginSubmit nike-unite-component')[0].children;
for (i=0; i<login_modal.length; i++){{\
if (login_modal[i].tagName.toLowerCase() == 'input'){{\
login_modal[i].click()\
}};}}"""
            self.driver.execute_script(get_and_click_login_button)
            time.sleep(10)

        else:
            email_field = self.driver.find_element_by_name('emailAddress')
            email_field.click()  # used to mitigate bot prevention handler (event listener)
            email_field.clear()
            email_field.send_keys(username_email)

            password_field = self.driver.find_element_by_name('password')
            password_field.click()  # used to mitigate bot prevention handler (event listener)
            password_field.clear()
            password_field.send_keys(password)

            get_and_click_login_button = """var i=0;\
var login_modal=document.getElementsByClassName('nike-unite-submit-button loginSubmit nike-unite-component')[0].children;
for (i=0; i<login_modal.length; i++){{\
if (login_modal[i].tagName.toLowerCase() == 'input'){{\
login_modal[i].click()\
}};}}"""
            self.driver.execute_script(get_and_click_login_button)
            time.sleep(5)

        self.cookies = self.driver.get_cookies()
        self.driver.close()

    def get_cookies(self):
        for cookie in self.cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])
        return self.session
