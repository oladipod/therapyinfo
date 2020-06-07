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

import os

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

import pymysql
conn = pymysql.connect(database = 'mysql', user = 'root@167.99.98.149:22', password ='90RrgyX0Nx9wCxWtE1Sc', host = '127.0.0.1', )
cur = conn.cursor()
print(conn)

fields = ['profile_link', 'profile_photolink', 'name', 'title', 'phone', 'website_link', 'hospital_centre', 'address1', 'city1', 
'state1', 'zipcode1',
'address2', 'spec_top', 'spec_issues', 'spec_mental', 'spec_sex', 'clientfocus_ethnic', 'clientfocus_speak',	'clientfocus_faith', 
'clientfocus_age',	'clientfocus_community', 'treatapproach_typestherapy', 'treatapproach_modality', 'about', 'fo_cps', 
'fo_slidingscale', 'fo_payby', 'fo_insurance', 'ft_sessionfee', 'ft_couplefee', 'ft_payby', 'qual_practice', 'qual_school', 
'qual_gradyear', 'qual_licensestate', 'qual_supervisor', 'qual_supervisorlicense', 
'qual_membership', 'qual_training', 'qual_degdiploma', 'adcred_cert1', 'addcred_date1', 
'addcred_cert2', 'addcred_date2', 'addcred_member', 'addcred_degdiploma', 'verification', 'pro_connects', 'groups'
]
    