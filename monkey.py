import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support.select.Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
from tqdm import tqdm
from selenium.webdriver.common.action_chains import ActionChains

#import psycopg2
import os

#conn = psycopg2.connect(database = 'postgres', user = 'devtotti', host = '127.0.0.1', port = '5432')
#cur = conn.cursor()

from datetime import datetime
import csv
import re
import time
from bs4 import BeautifulSoup as bsp
import requests
import pdb


chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument('--start-maximized--')

driver = webdriver.Chrome(executable_path = 'chromedriver', options=chrome_options)
action = ActionChains(driver)

driver.get("https://www.psychologytoday.com/en-be/therapists/an/antwerp/488551?sid=5ec6f553f05d9&ref=1&tr=ResultsName")
# try:
#     phone = driver.find_element_by_xpath('//*[@id="profile-content"]/div/div[2]/div[1]/div/div/div[1]').get_attribute('addressLocality').text()
# except Exception as error:
#     phone = 'null'
time.sleep(6)


print(spec_sex)



