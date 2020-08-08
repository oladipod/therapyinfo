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

import pymysql
import urllib.request

import os

from datetime import datetime
import csv
import re
import time
from bs4 import BeautifulSoup as bsp
import requests

from webdriver_manager.chrome import ChromeDriverManager


chrome_options = Options()
chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument('--start-maximized--')


driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# driver = webdriver.Chrome(executable_path = 'chromedriver', options=chrome_options)
action = ActionChains(driver)
#driver.maximize_window()



# CREATE CONNETION TO DATABASE AND CREATE A TABLE
# conn = pymysql.connect(database = 'mysql', user = 'root', passwd ='90RrgyX0Nx9wCxWtE1Sc', host = '167.99.98.149:22' )

"""
conn = pymysql.connect(host='167.99.98.149',user='remoteroot',passwd='9ZLkPeH4VZ!!p7t+nyE',port=3306)

cur = conn.cursor()
print(conn)
"""


# cur.execute("CREATE DATABASE psychtoday")
# conn.commit

# query1 = "CREATE TABLE psychtoday.psychologytoday(therapist_id INT AUTO_INCREMENT PRIMARY KEY, profile_link VARCHAR(500), profile_photolink VARCHAR(500), name VARCHAR(500), title VARCHAR(500), phone VARCHAR(500), spec_top VARCHAR(500), spec_issues VARCHAR(500), spec_mental VARCHAR(500), spec_sex VARCHAR(500), clientfocus_ethnic VARCHAR(500), clientfocus_speak VARCHAR(500), clientfocus_faith VARCHAR(500), clientfocus_age VARCHAR(500), clientfocus_community VARCHAR(500), treatapproach_typestherapy VARCHAR(500), treatapproach_modality VARCHAR(500), about TEXT(1000), fo_cps VARCHAR(500), fo_slidingscale VARCHAR(500), fo_payby VARCHAR(500), fo_insurance VARCHAR(500), ft_sessionfee VARCHAR(500), ft_couplefee VARCHAR(500), ft_payby VARCHAR(500), qual_practice VARCHAR(500), qual_school VARCHAR(500), qual_gradyear VARCHAR(500), qual_licensestate VARCHAR(500), qual_licenseprovince VARCHAR(500), qual_supervisor VARCHAR(500), qual_supervisorlicense VARCHAR(500), qual_membership VARCHAR(500), qual_training VARCHAR(500), qual_degdiploma VARCHAR(500), addcred_certificate1 VARCHAR(500), addcred_certificate2 VARCHAR(500), addcred_certificate_date1 VARCHAR(500), addcred_certificate_date2 VARCHAR(500), addcred_membership VARCHAR(500), addcred_degdiploma1 VARCHAR(500), addcred_degdiploma2 VARCHAR(500),  verification VARCHAR(500), pro_connect VARCHAR(500), groupss VARCHAR(500), address1 VARCHAR(500), address2 VARCHAR(500), website_url VARCHAR(500), profile_pix BLOB)"
# cur.execute(query1)
# conn.commit()

# SAVE TO CSV FILE
# with open ('AllProfileLinks.csv', 'w+', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(('s/n', 'Therapists ProfileLink'))

# with open ('AllProfileLinks.csv', 'a+', newline='') as f:
#     writer = csv.writer(f)


main_urls = ['https://www.psychologytoday.com/gb/counselling', 'https://www.psychologytoday.com/en-at/therapists', 'https://www.psychologytoday.com/en-be/therapists',
'https://www.psychologytoday.com/en-dk/therapists', 'https://www.psychologytoday.com/ie/counselling',
'https://www.psychologytoday.com/es/psicologos-psicoterapeutas', 'https://www.psychologytoday.com/en-se/therapists',
'https://www.psychologytoday.com/en-ch/therapists', 'https://www.psychologytoday.com/au/counselling',
'https://www.psychologytoday.com/hk/counselling', 'https://www.psychologytoday.com/nz/counselling', 
'https://www.psychologytoday.com/cl/psicologos', 'https://www.psychologytoday.com/sg/counselling',
'https://www.psychologytoday.com/za/counselling', 'https://www.psychologytoday.com/us/therapists', 
'https://www.psychologytoday.com/ca/therapists', 'https://www.psychologytoday.com/mx/psicologos'
]

# profile_link_list = []
navlinks = [] 
counterr = 0
for main_url in main_urls:
    driver.get(main_url)
    driver.implicitly_wait(0.3)
    time.sleep(3)

        #links of the states in each country
    try:  
        statelinks_obj = driver.find_elements_by_class_name('listItems')[0].find_elements_by_tag_name('a')     
        print('total no of state in', main_url, 'is', len(statelinks_obj) )      
        for i in statelinks_obj:    
            navlinks.append(i.get_property('href'))
        
    except Exception as error:
        print(main_url, 'GAVE SOME ERROR, MANUAL')


all_state  = "', '".join(navlinks)
print(all_state)   