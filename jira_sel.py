from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import configparser

Config = configparser.ConfigParser()
Config.read("./config.ini")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox') # Bypass OS security model
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=chrome_options)

def run(url):

    driver.get(url)
    reviewers = []
    try:
        elem = driver.find_element_by_id("login_field")
        elem.send_keys(Config['CREDENTIALS']["username"])
        time.sleep(2)
        passw = driver.find_element_by_id("password")
        passw.send_keys(Config['CREDENTIALS']["password"])
        log = driver.find_element_by_name("commit")
        log.send_keys(Keys.ENTER)
        time.sleep(3)
    except:
        pass
    re = driver.find_elements_by_class_name("assignee")
    for ass in re:
        reviewers.append(ass.text)
    return reviewers
