from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(executable_path=r'C:/Users/jsingh1/Downloads/chromedriver_win32/chromedriver.exe', options=chrome_options)

driver.get("https://github.secureserver.net/MCX/dotnet-api-packages/pull/207")

elem = driver.find_element_by_id("login_field")
elem.send_keys("jsingh1")
time.sleep(2)
passw = driver.find_element_by_id("password")
passw.send_keys("Sanjam@10")
log = driver.find_element_by_name("commit")
log.send_keys(Keys.ENTER)
time.sleep(3)
re = driver.find_elements_by_class_name("assignee")
for ass in re:
    print(ass.text)
