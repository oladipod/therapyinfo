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
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')



fields = ['profile_link', 'profile_photolink', 'name', 'title', 'phone, website_href', 'hospital_centre', 'address1', 
'address2', 'spec_top', 'spec_issues', 'spec_mental', 'spec_sex', 'clientfocus_ethnic', 'clientfocus_speak',	'clientfocus_faith', 
'clientfocus_age',	'clientfocus_community', 'treatapproach_typestherapy', 'treatapproach_modality', 'about', 'fo_cps', 
'fo_slidingscale', 'fo_payby', 'fo_insurance', 'ft_sessionfee', 'ft_couplefee', 'ft_payby', 'qual_practice', 'qual_school', 
'qual_gradyear', 'qual_licensestate', 'qual_supervisor', 'qual_supervisorlicense', 
'qual_membership', 'qual_training', 'qual_degdiploma', 'adcred_cert1', 'addcred_date1', 
'addcred_cert2', 'addcred_date2', 'addcred_member', 'addcred_degdiploma', 'verification', 'pro_connects', 'groups'
]

#To store to csv
# def openFile():
#     csvFile = open("therapist.csv", 'w', newline='')
#     writer = csv.writer(csvFile)
#     writer.writerow(fields)
#     csvFile.close()
    


	
driver = webdriver.Chrome(executable_path = 'C/Users\Samuel Ladipo\Documents\GitHub\FINAL SCRAPE TOTTI\chromedriver',options=chrome_options)
main_url = 'https://www.psychologytoday.com/us/therapists'
    
    


driver.get('https://www.psychologytoday.com/us/therapists/alabama/444145?sid=5ec54f52dfbcd&ref=1&tr=ResultsName')
try:
    name = driver.find_element_by_xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[1]/h1').text
except Exception as error:
    name = 'Not found'

try:
    profile_photolink = driver.find_element_by_xpath('//*[@id="profilePhoto"]/img').get_attribute('src')
except Exception as error:
    profile_photolink = 'Null'

try:
    title = driver.find_elements_by_class_name('profile-title').find_elements_by_class_name('nowrap').text


