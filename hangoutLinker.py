    # -*- coding: utf-8 -*-

import re
import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#credentials
email = os.getenv('TELEHANGBOT_GOOGLE_EMAIL')
password = os.getenv('TELEHANGBOT_GOOGLE_PASSWD')

debug = bool(os.getenv('TELEHANGBOT_TELEGRAM_DEBUG') or "False")

timeout_str = os.getenv('TELEHANGBOT_TIMEOUT') or "5"
timeout = int(timeout_str)

selenium_server_address = 'http://localhost:4444/wd/hub'

cookies_file = "cookies.pkl"
driver = None
loggedIn = False
links = 0

def saveCookies():
    print("saveCookies")
    # driver.get("https://google.com")
    # waitForUrl('https://www.google(.+)')
    # pickle.dump(driver.get_cookies(), open(cookies_file,"wb"))

def loadCookies():
    print("loadCookies")
    # try:
    #     driver.get("https://google.com")
    #     waitForUrl('https://www.google(.+)')
    #     if os.path.isfile(cookies_file):
    #         cookies = pickle.load(open(cookies_file, "rb"))
    #         for cookie in cookies:
    #             driver.add_cookie(cookie)
    # except:
    #     pass

def setUpDriver():
    """
    init driver and set chrome options
    """
    print("setUpDriver")
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
    print("checkLoggedIn")
    global driver
    global loggedIn
    try:
        driver.get("https://accounts.google.com")
        waitForUrl('https://accounts.google.com(.+)')

        elem = driver.find_element_by_name("identifier")
        loggedIn = False
    except:
        loggedIn = True
        pass

def login():
    """
    login into google account
    """
    print("login")
    global loggedIn
    
    loggedIn = False
    
    global driver
    global loggedIn

    loadCookies()
    checkLoggedIn()

    if loggedIn:
        return

    #login into google account
    driver.get("https://accounts.google.com")
    
    #enter email
    setValueAndGo("identifier", email)
    
    #enter password
    setValueAndGo("password", password)
    # if all is ok should be redirect to myaccount
    waitForUrl('https://myaccount.google.com(.+)')
    if 'myaccount.google.com' in driver.current_url: 
        loggedIn = True
    else:
        #set location if ip was changed and google asks for location
        setValueAndGo("answer", "Perm")
        checkLoggedIn()

    saveCookies()

def setValueAndGo(name, value):
    """
    set input value by name and press enter
    """
    print("setValueAndGo")
    global driver
    elem = driver.find_element_by_name(name)
    elem.send_keys(value)
    elem.send_keys(Keys.RETURN)

    # if debug:
    #     driver.save_screenshot('/shared/screen.png')

def waitForUrl(url):
    """
    wait while url loaded
    """
    print("waitForUrl")
    global driver
    regex = re.compile(url)
    for _ in range(10):
        print(driver.current_url)
        if regex.match(driver.current_url):
            return True
        time.sleep(0.5)

    return False

def tryGetLink():
    """
    try to get hangouts link
    """
    print("tryGetLink")
    global driver
    global loggedIn

    link = "error"
    try:
        if loggedIn:
            driver.get('https://hangouts.google.com/start')
            if waitForUrl('https://hangouts.google.com/(hangouts/_|call|calls)/(.+)'):
                link = driver.current_url
                #leave hangout's page
                driver.get('https://google.com')
    except Exception as e:
        if debug:
            link = link + ': ' + str(e)
        pass

    return link

def getlink():
    """
    authorize and get link
    """
    print("getlink")
    global links
    global loggedIn
    global driver

    links = links + 1
    link = tryGetLink()

    if 'error' in link:
        sepUpAndLogin()
        link = getlink()
    #restart chrome
    elif links > 100 or loggedIn == False:
        links = 0
        sepUpAndLogin()

    return link

def sepUpAndLogin():
    setUpDriver()
    login()
