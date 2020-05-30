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

#driver.get('https://www.psychologytoday.com/us/therapists/alabama/444145?sid=5ec54f52dfbcd&ref=1&tr=ResultsName')
#driver.get('https://www.psychologytoday.com/es/psicologos-psicoterapeutas/comunidad-valenciana/726849?sid=5ecfe3fe4e2f5&ref=7&tr=ResultsName')
#driver.get('file:///C:/Users/Samuel%20Ladipo/Documents/GitHub/therapyinfo/Dr.%20Dr.%20Terra%20Griffin,%20Ed.%20D.,%20LPC-S,%20NCC,%20Counselor,%20Hoover,%20AL,%2035226%20_%20Psychology%20Today.html')
# driver.get('file:///C:/Users/Samuel%20Ladipo/Documents/GitHub/therapyinfo/Empower%20Counseling%20&%20Coaching,%20Counselor,%20Birmingham,%20AL,%2035223%20_%20Psychology%20Today.html')
driver.get('file:///C:/Users/Samuel%20Ladipo/Documents/GitHub/therapyinfo/Kobus%20Fourie,%20Counsellor,%20Faerie%20Glen,%200081%20_%20Psychology%20Today.html')
# 'file:///C:/Users/Samuel%20Ladipo/Documents/GitHub/therapyinfo/Lena%20Santhirasegaram,%20Registered%20Psychotherapist,%20Toronto,%20ON,%20M4N%20_%20Psychology%20Today.html'
#driver.get('file:///C:/Users/Samuel%20Ladipo/Documents/GitHub/therapyinfo/Online%20services%20during%20coronavirus,%20Juneau,%20AK,%2099801%20_%20Psychology%20Today.html')
#driver.get('file:///C:/Users/Samuel%20Ladipo/Documents/GitHub/therapyinfo/Shenetra%20Alexander,%20Licensed%20Professional%20Counselor,%20Birmingham,%20AL,%2035218%20_%20Psychology%20Today.html')
#driver.get('file:///C:/Users/Samuel%20Ladipo/Documents/GitHub/therapyinfo/Shenetra%20Alexander,%20Licensed%20Professional%20Counselor,%20Birmingham,%20AL,%2035218%20_%20Psychology%20Today.html')
#     phone = driver.find_element_by_xpath('//*[@id="profile-content"]/div/div[2]/div[1]/div/div/div[1]').get_attribute('addressLocality').text()
# except Exception as error:
#     phone = 'null'
time.sleep(4)
# 


# try:
#     qual_practice_element = driver.find_element_by_class_name('profile-personalstatement').find_elements_by_class_name('statementPara')
#     qual_practice_list = []
#     for i in qual_practice_element:
#         qual_practice_list.append(i.text) 
#         qual_practice = ' '.join(qual_practice_list)
# except Exception as error:
#     qual_practice = 'null'


#def qualification_test()
try:
    qual_element = driver.find_element_by_class_name('profile-qualifications').find_element_by_tag_name('ul').find_elements_by_tag_name('li')
    
    for i in qual_element:
        qual_text = i.text
        try:
            if 'Years in Practice:' in qual_text:
                qual_practice = qual_text[18:]
                
            
            elif 'Year Graduated:' in qual_text:
                qual_gradyear = qual_text[15:]

            elif 'School:' in qual_text:
                qual_school = qual_text[7:]   

            elif 'License and State:' in qual_text:
                qual_licencestate = qual_text[21:]
                
            
            elif 'Licence and Province:' in qual_text:
                qual_licenceprovince = qual_text[21:]
                
            
            elif 'Supervisor:' in qual_text:
                qual_supervisor = qual_text[11:]
                
            
            elif 'Supervisor License:' in qual_text:
                qual_supervisorlicence = qual_text[19:]
                

            elif 'Membership:' in qual_text:
                qual_membership = qual_text[11:]
                
            
            elif 'Training:' in qual_text:
                qual_training = qual_text[8:]
                

            elif 'Degree / Diploma:' in qual_text:
                qual_degdiploma = qual_text[8:]

        except Exception as error:
            print ('QUALIFICATION NOT FOUND')
           

except Exception as error:
    qual_practice = 'Null'
    qual_school = 'Null'
    qual_gradyear = 'Null'
    qual_licencestate = 'Null'
    qual_licenceprovince = 'Null'
    qual_supervisor = 'Null'
    qual_supervisorlicence = 'Null'
    qual_membership = 'Null'
    qual_training = 'Null'
    qual_degdiploma = 'Null'

print(qual_practice)
print(qual_school)
print(qual_membership) 
print(qual_licencestate)
   

