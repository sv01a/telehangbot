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

debug = bool(os.getenv('TELEHANGBOT_TELEGRAM_TOKEN') or "False")

timeout_str = os.getenv('TELEHANGBOT_TIMEOUT') or "5"
timeout = int(timeout_str)

selenium_server_address = 'http://localhost:4444/wd/hub'
commands = [u'/потрындеть',u'/перетереть',u'/takeacall',u'/tac',u'/попиздеть',u'/поговорить',u'/беседа',u'/переговоры']

driver = None
loggedIn = False
links = 0

def setUpDriver():
    """
    init driver and set chrome options
    """
    global driver
    try:
        driver.close()
    except:
        pass

    #disable mic access request
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-user-media-security=true")
    options.add_argument("--use-fake-ui-for-media-stream")

    driver = webdriver.Remote(selenium_server_address, options.to_capabilities())
    #set timeout
    driver.implicitly_wait(timeout)

def checkLoggedIn():
    """
    check on logged in 
    """
    global driver
    try:
        driver.get("https://myaccount.google.com")
        waitForUrl('https://myaccount.google.com(.+)')

        if 'https://myaccount.google.com/intro' == driver.current_url:
            loggedIn = False
        else: 
            loggedIn = True
            loginTries = 0
    except:
        pass

def login():
    """
    login into google account
    """
    global driver
    global loggedIn
    #login into google account
    driver.get("https://accounts.google.com")
    
    #enter email
    setValueAndGo("Email", email)
    
    #enter password
    setValueAndGo("Passwd", password)
    # if all is ok should be redirect to myaccount
    waitForUrl('https://myaccount.google.com(.+)')
    if 'myaccount.google.com' in driver.current_url: 
        loggedIn = True
    else:
        #set location if ip was changed and google asks for location
        setValueAndGo("answer", "Perm")
        checkLoggedIn()

def setValueAndGo(id, value):
    """
    set input value by id and press enter
    """
    global driver
    elem = driver.find_element_by_id(id)
    elem.send_keys(value)
    elem.send_keys(Keys.RETURN)

def waitForUrl(url):
    """
    wait while url loaded
    """
    global driver
    regex = re.compile(url)
    for _ in range(20):
        if regex.match(driver.current_url):
            return True
        time.sleep(0.5)

    return False

def tryGetLink():
    """
    try to get hangouts link
    """
    global driver
    driver.get('https://hangouts.google.com/start')
    if waitForUrl('https://hangouts.google.com/hangouts/_/(.+)'):
        link = driver.current_url
        #leave hangout's page
        driver.get('https://google.com')
        return link
    else:
        return "error"

def getlink():
    """
    authorize and get link
    """
    global links
    global loggedIn

    links = links + 1
    link = 'error'

    try:
        checkLoggedIn()

        if loggedIn == True:
            link = tryGetLink()

    except Exception as e:
        if debug == True:
            link = str(e)
        pass
    
    #restart chrome
    if links > 100 or loggedIn == False:
        links = 0
        sepUpAndLogin()

    return link

def sepUpAndLogin():
    setUpDriver()
    login()

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

#main
#take some time to start selenium server
time.sleep(30)

sepUpAndLogin()

bot = telepot.Bot(token)
bot.message_loop(handle)

print('bot started')
#keep running
while 1:
	time.sleep(10)
