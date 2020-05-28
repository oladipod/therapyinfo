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



fields = ['profile_link', 'profile_photolink', 'name', 'title', 'phone', 'website_link', 'hospital_centre', 'address1', 'city1', 'state1', 'zipcode1'
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
    


main_urls = ['https://www.psychologytoday.com/us/therapists']	
profile_link_list = []
navlinks = []  
driver = webdriver.Chrome(executable_path = 'chromedriver', options=chrome_options)
action = ActionChains(driver)
#driver.maximize_window()
for main_url in main_urls:
        driver.get(main_url)
        driver.implicitly_wait(10)
        statelinks_obj = driver.find_elements_by_class_name('listItems')[0].find_elements_by_tag_name('a')

        #links of the states in each country       
         
        for i in statelinks_obj[:2]:     #remove
            navlinks.append(i.get_property('href'))
        #to get the webpage of each links of state, remove the []pls
        for j in navlinks[:2]:
            driver.get(j)
            print('NOW PROCEEDING TO', j )
            #time.sleep(5)
            
            #toget the profile link of each therapist on the list pge
            i = 0
            while i < 2:
                therapist_link = driver.find_elements_by_class_name('result-name')
                for k in therapist_link[:2]:  #remove
                    profile_link_list.append(k.get_attribute('href'))
                    i = i+1
                    
                print(len(profile_link_list))
                #pagenation- click the next button till you reach the last page
                # try:
                #     #perform actions by using javascript statement
                #     javaScript = "document.getElementsByClassName('icon-chevron-right')[0].click();"
                #     driver.execute_script(javaScript)
                #     time.sleep(10)

                #     # next_button = driver.find_elements_by_class_name('icon-chevron-right')[0]
                #     # driver.execute_script(("arguments[0].click();", next_button)
                # except Exception as error:
                #     break
            #get all therapist links, replace 2 with nothing pls
            for link in profile_link_list[:2]:
                driver.get(link)
                #driver.wait = WebDriverWait(driver, 5)

                #name
                name = str(driver.find_element_by_xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[1]/h1').text)
                

                #profile_photolink
                try:
                    profile_photolink = driver.find_element_by_xpath('//*[@id="profilePhoto"]/img').get_attribute('src')
                except Exception as error:
                    profile_photolink = 'No image'
                
                #title
                try:
                    title = driver.find_element_by_xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[1]/div').text
                except Exception as error:
                    title = 'Title not found'
                
                #phone
                try:
                    phone = driver.find_element_by_xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[2]/div/span/a').text
                except Exception as error:
                    phone = 'Phone not found'

                
                #hospital_centre
                
                #spec_top
                
                try:
                    spec_top_element = driver.find_element_by_class_name('specialties-list').find_elements_by_class_name('highlight')
                    spec_top_list = []
                    for i in spec_top_element:
                        spec_top_list.append(i.text) 
                    spec_top = ', '.join(spec_top_list)

                except Exception as error:
                    spec_top = 'null'



                #spec_issues

                try:
                    spec_issues_element = driver.find_element_by_xpath('//*[@id="profile-content"]/div/div[2]/div[2]/div[2]/div').find_elements_by_tag_name('li')
                    spec_issues_list = []
                    for i in spec_issues_element:
                        spec_issues_list.append(i.text) 
                        spec_issues = ', '.join(spec_issues_list)
                except Exception as error:
                    spec_issues = 'null'



                #spec_mental

                try:
                    spec_mental_element = driver.find_element_by_xpath('//*[@id="profile-content"]/div/div[2]/div[2]/div[3]/div').find_elements_by_tag_name('li')
                    spec_mental_list = []
                    for i in spec_mental_element:
                        spec_mental_list.append(i.text) 
                        spec_mental = ', '.join(spec_mental_list)
                except Exception as error:
                    spec_mental = 'null'


                #spec_sex

                try:
                    spec_sex_element = driver.find_element_by_class_name('attributes-sexuality').find_elements_by_tag_name('li')
                    spec_sex_list = []
                    for i in spec_sex_element:
                        spec_sex_list.append(i.text) 
                        spec_sex = ', '.join(spec_sex_list)
                except Exception as error:
                        spec_sex = 'null'


                #clientfocus_ethnic






print(name)
print(title)
print(profile_photolink)
print(phone)
print(spec_top)
print(spec_issues)
print(spec_mental)
print(spec_sex)
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()

print(profile_photolink)


#fuvk off