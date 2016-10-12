# -*- coding: utf-8 -*-

import re
import os
import time
import telepot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#credentials
token = os.getenv('TELEHANGBOT_TELEGRAM_TOKEN')
email = os.getenv('TELEHANGBOT_GOOGLE_EMAIL')
password = os.getenv('TELEHANGBOT_GOOGLE_PASSWD')

timeout_str = os.getenv('TELEHANGBOT_TIMEOUT') or "5"
timeout = int(timeout_str)

selenium_server_address = 'http://localhost:4444/wd/hub'
commands = [u'/потрындеть',u'/перетереть',u'/takeacall',u'/tac',u'/попиздеть',u'/поговорить',u'/беседа']


def handle(msg):
    """
    handle chat messages
    """
    chat_id = msg['chat']['id']
    command = msg['text']
    
    try:
        print('Got command: %s' % command.encode('ascii', 'ignore').decode('ascii', 'ignore'))
    except Exception: 
        pass
    
    if command in commands:
        bot.sendMessage(chat_id, getlink())

def setValueAndGo(driver, id, value):
    """
    set input value by id and press enter
    """
    elem = driver.find_element_by_id(id)
    elem.send_keys(value)
    elem.send_keys(Keys.RETURN)

def waitForUrl(driver, url):
    """
    wait while url loaded
    """
    regex = re.compile(url)
    for _ in range(20):
        if regex.match(driver.current_url):
            break
        time.sleep(1)

def tryGetLink(driver):
    """
    try to get hangouts link
    """
    if 'myaccount.google.com' in driver.current_url: 
        #start hangout
        elem = driver.get('https://hangouts.google.com/start')

        #wait until redirect and take a url
        waitForUrl(driver, 'https://hangouts.google.com/hangouts/_/(.+)')
        return driver.current_url
    else:
        return "error"

def getlink():
    """
    authorize and get link
    """
    link = ''

    #disable mic access request
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-user-media-security=true")
    options.add_argument("--use-fake-ui-for-media-stream")

    driver = webdriver.Remote(selenium_server_address, options.to_capabilities())
    #set timeout
    driver.implicitly_wait(timeout)

    #login into google account
    driver.get("https://accounts.google.com")
    
    #enter email
    setValueAndGo(driver, "Email", email)
    
    #enter password
    setValueAndGo(driver, "Passwd", password)

    waitForUrl(driver, 'https://myaccount.google.com(.+)')

    link = tryGetLink(driver)

    if link == "error":
        #enter city
        setValueAndGo(driver, "answer", "Perm")
        link = tryGetLink(driver)

    driver.close()
    return link

#main
bot = telepot.Bot(token)
bot.message_loop(handle)

print('bot started')
#keep running
while 1:
	time.sleep(10)
