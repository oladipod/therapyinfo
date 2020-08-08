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
with open ('AllProfileLinksss.csv', 'w+', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(('s/n', 'Therapists ProfileLink'))

with open ('AllProfileLinksss.csv', 'a+', newline='') as f:
    writer = csv.writer(f)

    state_urls = ['https://www.psychologytoday.com/gb/counselling/channel-islands', 'https://www.psychologytoday.com/gb/counselling/england', 'https://www.psychologytoday.com/gb/counselling/isle-of-man', 'https://www.psychologytoday.com/gb/counselling/northern-ireland', 
    'https://www.psychologytoday.com/gb/counselling/scotland', 'https://www.psychologytoday.com/gb/counselling/wales', 'https://www.psychologytoday.com/en-at/therapists/burgenland', 'https://www.psychologytoday.com/en-at/therapists/carinthia', 'https://www.psychologytoday.com/en-at/therapists/lower-austria', 
    'https://www.psychologytoday.com/en-at/therapists/salzburg', 'https://www.psychologytoday.com/en-at/therapists/styria', 'https://www.psychologytoday.com/en-at/therapists/tyrol', 'https://www.psychologytoday.com/en-at/therapists/upper-austria', 'https://www.psychologytoday.com/en-at/therapists/vienna', 'https://www.psychologytoday.com/en-at/therapists/vorarlberg', 
    'https://www.psychologytoday.com/en-be/therapists/brussels', 'https://www.psychologytoday.com/en-be/therapists/flanders', 'https://www.psychologytoday.com/en-be/therapists/walloon-region', 'https://www.psychologytoday.com/en-dk/therapists/capital-region-of-denmark', 
    'https://www.psychologytoday.com/en-dk/therapists/central-denmark-region', 'https://www.psychologytoday.com/en-dk/therapists/north-denmark-region', 'https://www.psychologytoday.com/en-dk/therapists/region-of-southern-denmark', 'https://www.psychologytoday.com/en-dk/therapists/zealand', 
    'https://www.psychologytoday.com/ie/counselling/connacht', 'https://www.psychologytoday.com/ie/counselling/leinster', 'https://www.psychologytoday.com/ie/counselling/munster', 'https://www.psychologytoday.com/ie/counselling/ulster', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/andalucia', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/aragon', 
    'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/principado-de-asturias', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/islas-baleares', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/pais-vasco', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/islas-canarias', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/cantabria', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/castilla-y-leon', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/castilla-la-mancha', 
    'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/cataluna', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/ceuta', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/comunidad-de-madrid', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/extremadura', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/galicia', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/la-rioja', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/melilla', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/comunidad-foral-de-navarra', 
    'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/region-de-murcia', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/comunidad-valenciana', 'https://www.psychologytoday.com/en-se/therapists/blekinge-county', 'https://www.psychologytoday.com/en-se/therapists/dalarna-county', 'https://www.psychologytoday.com/en-se/therapists/gavleborg-county', 'https://www.psychologytoday.com/en-se/therapists/gotland', 'https://www.psychologytoday.com/en-se/therapists/halland-county', 'https://www.psychologytoday.com/en-se/therapists/jamtland-county', 'https://www.psychologytoday.com/en-se/therapists/jonkoping-county', 
    'https://www.psychologytoday.com/en-se/therapists/kalmar-county', 'https://www.psychologytoday.com/en-se/therapists/kronoberg-county', 'https://www.psychologytoday.com/en-se/therapists/norrbotten-county', 'https://www.psychologytoday.com/en-se/therapists/orebro', 'https://www.psychologytoday.com/en-se/therapists/ostergotland', 'https://www.psychologytoday.com/en-se/therapists/skane', 'https://www.psychologytoday.com/en-se/therapists/sodermanland', 'https://www.psychologytoday.com/en-se/therapists/stockholm-county', 'https://www.psychologytoday.com/en-se/therapists/uppsala-county', 'https://www.psychologytoday.com/en-se/therapists/varmland-county', 
    'https://www.psychologytoday.com/en-se/therapists/vasterbotten', 'https://www.psychologytoday.com/en-se/therapists/vasternorrland', 'https://www.psychologytoday.com/en-se/therapists/vastmanland', 'https://www.psychologytoday.com/en-se/therapists/vastra-gotaland', 'https://www.psychologytoday.com/en-ch/therapists/aargau', 'https://www.psychologytoday.com/en-ch/therapists/appenzell-ausserrhoden', 'https://www.psychologytoday.com/en-ch/therapists/appenzell-innerrhoden', 'https://www.psychologytoday.com/en-ch/therapists/basel-city', 'https://www.psychologytoday.com/en-ch/therapists/basel-landschaft', 'https://www.psychologytoday.com/en-ch/therapists/bern', 'https://www.psychologytoday.com/en-ch/therapists/geneva', 'https://www.psychologytoday.com/en-ch/therapists/glarus', 'https://www.psychologytoday.com/en-ch/therapists/grisons', 'https://www.psychologytoday.com/en-ch/therapists/jura', 'https://www.psychologytoday.com/en-ch/therapists/la-sarine', 'https://www.psychologytoday.com/en-ch/therapists/lucerne-district', 
    'https://www.psychologytoday.com/en-ch/therapists/neuenburg', 'https://www.psychologytoday.com/en-ch/therapists/nidwalden', 'https://www.psychologytoday.com/en-ch/therapists/obwalden', 'https://www.psychologytoday.com/en-ch/therapists/schaffhausen', 'https://www.psychologytoday.com/en-ch/therapists/schwyz-district', 'https://www.psychologytoday.com/en-ch/therapists/solothurn', 'https://www.psychologytoday.com/en-ch/therapists/st-gallen', 'https://www.psychologytoday.com/en-ch/therapists/thurgau', 'https://www.psychologytoday.com/en-ch/therapists/ticino', 'https://www.psychologytoday.com/en-ch/therapists/uri', 'https://www.psychologytoday.com/en-ch/therapists/valais', 'https://www.psychologytoday.com/en-ch/therapists/vaud', 'https://www.psychologytoday.com/en-ch/therapists/zug', 'https://www.psychologytoday.com/en-ch/therapists/zurich', 'https://www.psychologytoday.com/au/counselling/australian-capital-territory', 'https://www.psychologytoday.com/au/counselling/new-south-wales', 'https://www.psychologytoday.com/au/counselling/northern-territory', 
    'https://www.psychologytoday.com/au/counselling/queensland', 'https://www.psychologytoday.com/au/counselling/south-australia', 'https://www.psychologytoday.com/au/counselling/tasmania', 'https://www.psychologytoday.com/au/counselling/victoria', 'https://www.psychologytoday.com/au/counselling/western-australia', 'https://www.psychologytoday.com/hk/counselling/hong-kong', 'https://www.psychologytoday.com/hk/counselling/kowloon', 'https://www.psychologytoday.com/hk/counselling/new-territories', 'https://www.psychologytoday.com/nz/counselling/auckland', 'https://www.psychologytoday.com/nz/counselling/bay-of-plenty', 'https://www.psychologytoday.com/nz/counselling/canterbury', 'https://www.psychologytoday.com/nz/counselling/gisborne', 'https://www.psychologytoday.com/nz/counselling/hawke-s-bay', 'https://www.psychologytoday.com/nz/counselling/manawatu-wanganui', 'https://www.psychologytoday.com/nz/counselling/marlborough', 'https://www.psychologytoday.com/nz/counselling/nelson', 'https://www.psychologytoday.com/nz/counselling/northland', 'https://www.psychologytoday.com/nz/counselling/otago', 'https://www.psychologytoday.com/nz/counselling/southland', 'https://www.psychologytoday.com/nz/counselling/taranaki', 'https://www.psychologytoday.com/nz/counselling/tasman', 'https://www.psychologytoday.com/nz/counselling/waikato', 'https://www.psychologytoday.com/nz/counselling/wellington', 'https://www.psychologytoday.com/nz/counselling/west-coast', 'https://www.psychologytoday.com/cl/psicologos/antofagasta', 'https://www.psychologytoday.com/cl/psicologos/arica-y-parinacota', 'https://www.psychologytoday.com/cl/psicologos/atacama', 'https://www.psychologytoday.com/cl/psicologos/aysen-del-general-carlos-ibanez-del-campo', 'https://www.psychologytoday.com/cl/psicologos/bio-bio', 'https://www.psychologytoday.com/cl/psicologos/coquimbo', 'https://www.psychologytoday.com/cl/psicologos/la-araucania', 'https://www.psychologytoday.com/cl/psicologos/los-lagos', 
    'https://www.psychologytoday.com/cl/psicologos/los-rios', 'https://www.psychologytoday.com/cl/psicologos/magallanes-y-de-la-antartica-chilena', 'https://www.psychologytoday.com/cl/psicologos/maule', 'https://www.psychologytoday.com/cl/psicologos/libertador-general-bernardo-ohiggins', 'https://www.psychologytoday.com/cl/psicologos/region-metropolitana-de-santiago', 'https://www.psychologytoday.com/cl/psicologos/tarapaca', 'https://www.psychologytoday.com/cl/psicologos/valparaiso', 'https://www.psychologytoday.com/sg/counselling/sg/singapore', 'https://www.psychologytoday.com/za/counselling/eastern-cape', 'https://www.psychologytoday.com/za/counselling/free-state', 'https://www.psychologytoday.com/za/counselling/gauteng', 'https://www.psychologytoday.com/za/counselling/kwazulu-natal', 'https://www.psychologytoday.com/za/counselling/limpopo', 'https://www.psychologytoday.com/za/counselling/mpumalanga', 'https://www.psychologytoday.com/za/counselling/north-west', 'https://www.psychologytoday.com/za/counselling/northern-cape', 'https://www.psychologytoday.com/za/counselling/western-cape', 'https://www.psychologytoday.com/us/therapists/alabama', 'https://www.psychologytoday.com/us/therapists/alaska', 'https://www.psychologytoday.com/us/therapists/arizona', 'https://www.psychologytoday.com/us/therapists/arkansas', 'https://www.psychologytoday.com/us/therapists/california', 'https://www.psychologytoday.com/us/therapists/colorado', 'https://www.psychologytoday.com/us/therapists/connecticut', 'https://www.psychologytoday.com/us/therapists/delaware', 'https://www.psychologytoday.com/us/therapists/district-of-columbia', 'https://www.psychologytoday.com/us/therapists/florida', 'https://www.psychologytoday.com/us/therapists/georgia', 'https://www.psychologytoday.com/us/therapists/guam', 'https://www.psychologytoday.com/us/therapists/hawaii', 'https://www.psychologytoday.com/us/therapists/idaho', 'https://www.psychologytoday.com/us/therapists/illinois', 'https://www.psychologytoday.com/us/therapists/indiana', 'https://www.psychologytoday.com/us/therapists/iowa', 'https://www.psychologytoday.com/us/therapists/kansas', 'https://www.psychologytoday.com/us/therapists/kentucky', 'https://www.psychologytoday.com/us/therapists/louisiana', 'https://www.psychologytoday.com/us/therapists/maine', 'https://www.psychologytoday.com/us/therapists/maryland', 'https://www.psychologytoday.com/us/therapists/massachusetts', 'https://www.psychologytoday.com/us/therapists/michigan', 'https://www.psychologytoday.com/us/therapists/minnesota', 'https://www.psychologytoday.com/us/therapists/mississippi', 'https://www.psychologytoday.com/us/therapists/missouri', 'https://www.psychologytoday.com/us/therapists/montana', 'https://www.psychologytoday.com/us/therapists/nebraska',
    'https://www.psychologytoday.com/us/therapists/nevada', 'https://www.psychologytoday.com/us/therapists/new-hampshire', 'https://www.psychologytoday.com/us/therapists/new-jersey', 'https://www.psychologytoday.com/us/therapists/new-mexico', 
    'https://www.psychologytoday.com/us/therapists/new-york', 'https://www.psychologytoday.com/us/therapists/north-carolina', 'https://www.psychologytoday.com/us/therapists/north-dakota', 'https://www.psychologytoday.com/us/therapists/ohio', 'https://www.psychologytoday.com/us/therapists/oklahoma', 'https://www.psychologytoday.com/us/therapists/oregon', 'https://www.psychologytoday.com/us/therapists/pennsylvania', 'https://www.psychologytoday.com/us/therapists/puerto-rico', 'https://www.psychologytoday.com/us/therapists/rhode-island', 'https://www.psychologytoday.com/us/therapists/south-carolina', 'https://www.psychologytoday.com/us/therapists/south-dakota', 'https://www.psychologytoday.com/us/therapists/tennessee', 'https://www.psychologytoday.com/us/therapists/texas', 'https://www.psychologytoday.com/us/therapists/utah', 'https://www.psychologytoday.com/us/therapists/vermont', 'https://www.psychologytoday.com/us/therapists/virgin-islands', 'https://www.psychologytoday.com/us/therapists/virginia', 'https://www.psychologytoday.com/us/therapists/washington', 'https://www.psychologytoday.com/us/therapists/west-virginia', 'https://www.psychologytoday.com/us/therapists/wisconsin', 'https://www.psychologytoday.com/us/therapists/wyoming', 'https://www.psychologytoday.com/ca/therapists/alberta', 'https://www.psychologytoday.com/ca/therapists/british-columbia', 'https://www.psychologytoday.com/ca/therapists/manitoba', 'https://www.psychologytoday.com/ca/therapists/new-brunswick', 'https://www.psychologytoday.com/ca/therapists/newfoundland-and-labrador', 'https://www.psychologytoday.com/ca/therapists/nova-scotia', 'https://www.psychologytoday.com/ca/therapists/ontario', 'https://www.psychologytoday.com/ca/therapists/prince-edward-island', 'https://www.psychologytoday.com/ca/therapists/quebec', 'https://www.psychologytoday.com/ca/therapists/saskatchewan', 'https://www.psychologytoday.com/ca/therapists/yukon', 'https://www.psychologytoday.com/mx/psicologos/aguascalientes', 'https://www.psychologytoday.com/mx/psicologos/baja-california', 'https://www.psychologytoday.com/mx/psicologos/baja-california-sur', 'https://www.psychologytoday.com/mx/psicologos/campeche', 'https://www.psychologytoday.com/mx/psicologos/chiapas', 'https://www.psychologytoday.com/mx/psicologos/chihuahua', 'https://www.psychologytoday.com/mx/psicologos/ciudad-de-mexico', 'https://www.psychologytoday.com/mx/psicologos/coahuila-de-zaragoza', 'https://www.psychologytoday.com/mx/psicologos/colima', 'https://www.psychologytoday.com/mx/psicologos/durango', 'https://www.psychologytoday.com/mx/psicologos/guanajuato', 'https://www.psychologytoday.com/mx/psicologos/guerrero', 'https://www.psychologytoday.com/mx/psicologos/hidalgo', 'https://www.psychologytoday.com/mx/psicologos/jalisco', 
    'https://www.psychologytoday.com/mx/psicologos/mexico', 'https://www.psychologytoday.com/mx/psicologos/michoacan-de-ocampo', 'https://www.psychologytoday.com/mx/psicologos/morelos', 'https://www.psychologytoday.com/mx/psicologos/nayarit', 'https://www.psychologytoday.com/mx/psicologos/nuevo-leon', 'https://www.psychologytoday.com/mx/psicologos/oaxaca', 'https://www.psychologytoday.com/mx/psicologos/puebla', 'https://www.psychologytoday.com/mx/psicologos/queretaro', 'https://www.psychologytoday.com/mx/psicologos/quintana-roo', 'https://www.psychologytoday.com/mx/psicologos/san-luis-potosi', 'https://www.psychologytoday.com/mx/psicologos/sinaloa', 'https://www.psychologytoday.com/mx/psicologos/sonora', 'https://www.psychologytoday.com/mx/psicologos/tabasco', 'https://www.psychologytoday.com/mx/psicologos/tamaulipas', 'https://www.psychologytoday.com/mx/psicologos/tlaxcala', 'https://www.psychologytoday.com/mx/psicologos/veracruz-de-ignacio-de-la-llave', 'https://www.psychologytoday.com/mx/psicologos/yucatan', 'https://www.psychologytoday.com/mx/psicologos/zacatecas'
    ]

    # profile_link_list = []
    counterr = 0



    #to get the webpage of each links of state, 
    for j in state_urls:
            driver.get(j)
            print('NOW PROCEEDING TO', j )
            driver.implicitly_wait(0.2)
            # time.sleep(0.1)
            
            #toget the profile link of each therapist on the list pge
            try:
                condition = True
                while condition:  
                    therapist_link = driver.find_elements_by_class_name('result-name')
                    print(len(therapist_link))
                    for k in therapist_link:  
                        prof_link = k.get_attribute('href')

                        writer.writerow((counterr, prof_link))
                        counterr += 1
                        print(prof_link)
                        


                    

                        # profile_link_list.append(prof_link)
                        
                    #pagenation- click the next button till you reach the last page
                    try:
                        #perform actions by using javascript statement
                        javaScript = "document.getElementsByClassName('icon-chevron-right')[0].click();"
                        driver.execute_script(javaScript)

                        ## next_button = driver.find_elements_by_class_name('icon-chevron-right')[0]
                        ## driver.execute_script(("arguments[0].click();", next_button)
                    except Exception as error:
                        condition = False

            except Exception as error:
                print('NO LIST ON THIS PAGE')

        # print(len(profile_link_list))






"""
# rowcounter = 1
#iterate over each therapist profiles
for link in profile_link_list:
    profile_page = driver.get(link)
    # driver.wait = WebDriverWait(driver, 3)
    profile_link = link
    writer.writerow(prof)





    #TO START GETTING ALL REQUIRED FIELDS ON EACH PAGE

    #profile_link
    profile_link = link
    
    #name
    try:
        name = str(driver.find_element_by_xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[1]/h1').text)
    except Exception as error:
        name = ''

    #profile_photolink
    try:
        profile_photolink = driver.find_element_by_xpath('//*[@id="profilePhoto"]/img').get_attribute('src')
    except Exception as error:
        profile_photolink = ''
    
    #title
    try:
        title = driver.find_element_by_xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[1]/div').text
    except Exception as error:
        title = ''
    
    #phone
    try:
        phone = driver.find_element_by_xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[2]/div/span/a').text
    except Exception as error:
        phone = ''

    
    # hospital_centre  ===unable to capture
    
    #spec_top
    
    try:
        spec_top_element = driver.find_element_by_class_name('specialties-list').find_elements_by_class_name('highlight')
        spec_top_list = []
        for i in spec_top_element:
            spec_top_list.append(i.text) 
        spec_top = ', '.join(spec_top_list)

    except Exception as error:
        spec_top = ''



    #spec_issues

    try:
        spec_issues_element = driver.find_element_by_xpath('//*[@id="profile-content"]/div/div[2]/div[2]/div[2]/div').find_elements_by_tag_name('li')
        spec_issues_list = []
        for i in spec_issues_element:
            spec_issues_list.append(i.text) 
        spec_issues = ', '.join(spec_issues_list)
    except Exception as error:
        spec_issues = ''



    #spec_mental

    try:
        spec_mental_element = driver.find_element_by_xpath('//*[@id="profile-content"]/div/div[2]/div[2]/div[3]/div').find_elements_by_tag_name('li')
        spec_mental_list = []
        for i in spec_mental_element:
            spec_mental_list.append(i.text) 
        spec_mental = ', '.join(spec_mental_list)
    except Exception as error:
        spec_mental = ''


    #spec_sex

    try:
        spec_sex_element = driver.find_element_by_class_name('attributes-sexuality').find_elements_by_tag_name('li')
        spec_sex_list = []
        for i in spec_sex_element:
            spec_sex_list.append(i.text)
        spec_sex = ', '.join(spec_sex_list)
    except Exception as error:
            spec_sex = ''


    #clientfocus_ethnic

    try:
        clientfocus_ethnic_element = driver.find_element_by_class_name('attributes-ethnicity-focus').find_elements_by_tag_name('span')[1:]
        clientfocus_ethnic_list = []
        for i in clientfocus_ethnic_element:
            clientfocus_ethnic_list.append(i.text) 
        clientfocus_ethnic = ', '.join(clientfocus_ethnic_list)
    except Exception as error:
        clientfocus_ethnic = ''


    
    #clientfocus_speak
    try:
        clientfocus_speak_element = driver.find_element_by_class_name('attributes-language').find_elements_by_tag_name('span')[1:]
        clientfocus_speak_list = []
        for i in clientfocus_speak_element:
            clientfocus_speak_list.append(i.text) 
        clientfocus_speak = ', '.join(clientfocus_speak_list)
    except Exception as error:
        clientfocus_speak = ''
    


    #clientfocus_faith
    try:
        clientfocus_faith_element = driver.find_element_by_class_name('attributes-religion').find_elements_by_tag_name('span')[1:]
        clientfocus_faith_list = []
        for i in clientfocus_faith_element:
            clientfocus_faith_list.append(i.text) 
        clientfocus_faith = ', '.join(clientfocus_faith_list)
    except Exception as error:
        clientfocus_faith = ''


    #clientfocus_age
    try:
        clientfocus_age_element = driver.find_element_by_class_name('attributes-age-focus').find_elements_by_tag_name('li')
        clientfocus_age_list = []
        for i in clientfocus_age_element:
            clientfocus_age_list.append(i.text) 
        clientfocus_age = ', '.join(clientfocus_age_list)
    except Exception as error:
        clientfocus_age = ''


    #clientfocus_community
    try:
        clientfocus_community_element = driver.find_element_by_class_name('attributes-categories').find_elements_by_tag_name('li')
        clientfocus_community_list = []
        for i in clientfocus_community_element:
            clientfocus_community_list.append(i.text) 
        clientfocus_community = ', '.join(clientfocus_community_list)
    except Exception as error:
        clientfocus_community = ''

    
    #treatapproach_typestherapy
    try:
        treatapproach_therapy_element = driver.find_element_by_class_name('attributes-treatment-orientation').find_elements_by_tag_name('span')
        treatapproach_therapy_list = []
        for i in treatapproach_therapy_element:
            treatapproach_therapy_list.append(i.text)
        treatapproach_typestherapy = ', '.join(treatapproach_therapy_list)

    except Exception as error:
        treatapproach_typestherapy = ''



    #treatapproach_modality

    try:
        treatapproach_modality_element = driver.find_element_by_class_name('attributes-modality').find_elements_by_tag_name('li')
        treatapproach_modality_list = []
        for i in treatapproach_modality_element:
            treatapproach_modality_list.append(i.text) 
        treatapproach_modality = ', '.join(treatapproach_modality_list)
    except Exception as error:
        treatapproach_modality = ''



    #about

    try:
        about_element = driver.find_element_by_class_name('profile-personalstatement').find_elements_by_class_name('statementPara')
        about_list = []
        for i in about_element:
            about_list.append(i.text) 
            about = ' '.join(about_list)
    except Exception as error:
        about = ''

    
    #fo_cps
    #fo_cps , fo_slidingsccale
    try:
        unspecified_fo_element1 = driver.find_element_by_id('tabs-finances-office').find_elements_by_tag_name('li')
        if len(unspecified_fo_element1) == 2:
            fo_cps = unspecified_fo_element1[0].text[17:]
            fo_slidingscale = unspecified_fo_element1[1].text[14:]
        else:
            fo_cps = unspecified_fo_element1[0].text[17:] 
            fo_slidingscale = ''

    except Exception as error:
        fo_cps = ''
        fo_slidingscale = ''

    #fo_payby
    try:
        unspecified_fo_element2 = driver.find_element_by_class_name('attributes-payment-method').find_elements_by_tag_name('span')
        fo_payby_list = []
        for i in unspecified_fo_element2:
            fo_payby_list.append(i.text)
        fo_payby = ' '.join(fo_payby_list[1:])

    except Exception as error:
        fo_payby = ''


    #fo_insurance
    try:
        unspecified_fo_element3 = driver.find_element_by_class_name('attributes-insurance').find_elements_by_tag_name('li')
        fo_insurance_list = []
        for i in unspecified_fo_element3:
            fo_insurance_list.append(i.text)
        fo_insurance = ','.join(fo_insurance_list)

    except Exception as error:
        fo_insurance = ''

    #to click on teletherapy button options
    try:
        teletherapy = driver.find_element_by_id('select-finances-online').click()
        time.sleep(5)

        #ft_sessionfee, ft_couplefee
        ft_sessionfee_element = driver.find_element_by_id('tabs-finances-online').find_elements_by_tag_name('li')
        ft_sessionfee_list = []
        for i in ft_sessionfee_element:
            ft_sessionfee_list.append(i.text)
        ft_sessionfee = ft_sessionfee_list[0][12:]
        ft_couplefee = ft_sessionfee_list[1][20:]

        #ft_payby
        try:
            ft_element = driver.find_element_by_class_name('finances-online').find_elements_by_tag_name('span')
            ft_payby_list = []
            for i in ft_element:
                ft_payby_list.append(i.text)
            ft_payby = ' '.join(ft_payby_list[1:])

        except Exception as error:
            ft_payby = ''  

    except Exception as error:
        print ('NO TELETHERAPY OPTION')
        ft_sessionfee = ''
        ft_couplefee = ''
        ft_payby = ''

    

    #QUALIFICATION
    qual_practice = ''
    qual_school = ''
    qual_gradyear = ''
    qual_licensestate = ''
    qual_licenseprovince = ''
    qual_supervisor = ''
    qual_supervisorlicense = ''
    qual_membership = ''
    qual_training = ''
    qual_degdiploma = ''


    try:

        qual_element = driver.find_element_by_class_name('profile-qualifications').find_element_by_tag_name('ul').find_elements_by_tag_name('li')

        qual_textlist = []
        for i in qual_element:
            qual_text = i.text
            qual_textlist.append(qual_text)
        qual_textlist_string = ' +++ '.join(qual_textlist)

        if 'Membership:' in qual_textlist_string:
            qual_membership = qual_textlist_string.split('Membership:')[1].split('+++')[0]
        elif 'Membresía:' in qual_textlist_string:
            qual_membership = qual_textlist_string.split('Membresía:')[1].split('+++')[0]
        else: 
            pass

        if 'Years in Practice:' in qual_textlist_string:
            qual_practice = qual_textlist_string.split('Years in Practice:')[1].split('+++')[0]
        elif 'Años de experiencia:' in qual_textlist_string:
            qual_practice = qual_textlist_string.split('Años de experiencia:')[1].split('+++')[0]
        else: 
            pass

        if 'School:' in qual_textlist_string:
            qual_school = qual_textlist_string.split('School:')[1].split('+++')[0]
        else: 
            pass

        if 'Year Graduated:' in qual_textlist_string:
            qual_gradyear = qual_textlist_string.split('Year Graduated:')[1].split('+++')[0]
        else: 
            pass

        if 'License and State:' in qual_textlist_string:
            qual_licensestate = qual_textlist_string.split('License and State:')[1].split('+++')[0]
        elif 'Licencia:' in qual_textlist_string:
            qual_licensestate = qual_textlist_string.split('Licencia:')[1].split('+++')[0]
        else: 
            pass

        if 'Licence and Province:' in qual_textlist_string:
            qual_licenseprovince = qual_textlist_string.split('Licence and Province:')[1].split('+++')[0]
        else: 
            pass

        if 'Supervisor:' in qual_textlist_string:
            qual_supervisor = qual_textlist_string.split('Supervisor:')[1].split('+++')[0]
        else: 
            pass

        if 'Supervisor License:' in qual_textlist_string:
            qual_supervisorlicense = qual_textlist_string.split('Supervisor License:')[1].split('+++')[0]
        else: 
            pass

        if 'Training:' in qual_textlist_string:
            qual_training = qual_textlist_string.split('Training:')[1].split('+++')[0]
        elif 'Formación:' in qual_textlist_string:
            qual_training= qual_textlist_string.split('Formación:')[1].split('+++')[0]
        else: 
            pass

        if 'Degree / Diploma:' in qual_textlist_string:
            qual_degdiploma = qual_textlist_string.split('Degree / Diploma:')[1].split('+++')[0]
        elif 'Título / Diploma:' in qual_textlist_string:
            qual_degdiploma = qual_textlist_string.split('Título / Diploma:')[1].split('+++')[0]
        else: 
            pass

    except Exception as error:
        qual_practice = ''
        qual_school = ''
        qual_gradyear = ''
        qual_licensestate = ''
        qual_licenseprovince = ''
        qual_supervisor = ''
        qual_supervisorlicense = ''
        qual_membership = ''
        qual_training = ''
        qual_degdiploma = ''



    # #ADDITIONAL CREDENTIALS
    addcred_certificate1 = ''
    addcred_certificate2 = ''
    addcred_certificate_date1 = ''
    addcred_certificate_date2 = ''
    addcred_membership = ''
    addcred_degdiploma1 = ''
    addcred_degdiploma2 = ''



    # ADDITIONAL CRED
    try:
        addcred_element = driver.find_element_by_class_name('profile-additional-credentials').find_elements_by_tag_name('li')
        addcred_textlist = []
        for i in addcred_element:
            addcred_text = i.text
            addcred_textlist.append(addcred_text)
        addcred_textlist_string = ' +++ '.join(addcred_textlist)
        


        #Certificates
        if 'Certificate:' in addcred_textlist_string:
            addcred_certificate = addcred_textlist_string.split('Certificate:')

            if len(addcred_certificate) > 2 and len(addcred_certificate) < 4:
                addcred_certificate1 = addcred_certificate[1].split('+++')[0]
                addcred_certificate2 = addcred_certificate[2].split('+++')[0]
            else:
                addcred_certificate1 = addcred_certificate[1].split('+++')[0]
                addcred_certificate2 = ''

        elif 'Certificado:' in addcred_textlist_string:
            addcred_certificate = addcred_textlist_string.split('Certificado:')

            if len(addcred_certificate) > 2 and len(addcred_certificate) < 4:
                addcred_certificate1 = addcred_certificate[1].split('+++')[0]
                addcred_certificate2 = addcred_certificate[2].split('+++')[0]
            else:
                addcred_certificate1 = addcred_certificate[1].split('+++')[0]
                addcred_certificate2 = ''


        else: 
            addcred_certificate1 = ''
            addcred_certificate2 = ''
        


        #Certificate dates
        if 'Certificate Date: ' in addcred_textlist_string:
            addcred_certificate_date = addcred_textlist_string.split('Certificate Date: ')

            if len(addcred_certificate_date) > 2 and len(addcred_certificate_date) < 4:
                addcred_certificate_date1 = addcred_certificate_date[1].split('+++')[0]
                addcred_certificate_date2 = addcred_certificate_date[2].split(' ')[0]
            else:
                addcred_certificate_date1 = addcred_certificate_date[1]
                addcred_certificate_date2 = ''

        else:
            addcred_certificate_date1 = ''
            addcred_certificate_date2 = ''

        
        #membership
        if 'Membership:' in addcred_textlist_string: 
            addcred_membership = addcred_textlist_string.split('Membership:')[1]

        elif 'Membresía:' in addcred_textlist_string: 
            addcred_membership = addcred_textlist_string.split('Membresía:')[1]
        else:
            addcred_membership = ''
        
        #degree diploma
        if 'Degree / Diploma:' in addcred_textlist_string: 
            addcred_degdiploma = addcred_textlist_string.split('Degree / Diploma:')
            if len(addcred_degdiploma) > 2 and len(addcred_degdiploma) < 4:
                addcred_degdiploma1 = addcred_degdiploma[1].split('+++')[0]
                addcred_degdiploma2= addcred_degdiploma[2].split('+++')[0]
            else:
                addcred_degdiploma1 = addcred_degdiploma[1].split('+++')[0]
                addcred_degdiploma2 = 'Null'

        elif 'Título / Diploma:' in addcred_textlist_string: 
            addcred_degdiploma = addcred_textlist_string.split('Título / Diploma:')
            if len(addcred_degdiploma) > 2 and len(addcred_degdiploma) < 4:
                addcred_degdiploma1 = addcred_degdiploma[1].split('+++')[0]
                addcred_degdiploma2= addcred_degdiploma[2].split('+++')[0]
            else:
                addcred_degdiploma1 = addcred_degdiploma[1].split('+++')[0]
                addcred_degdiploma2 = ''
        
        else:
            pass

    except Exception as error:
        addcred_certificate1 = ''
        addcred_certificate2 = ''
        addcred_certificate_date1 = ''
        addcred_certificate_date2 = ''
        addcred_membership = ''
        addcred_degdiploma1 = ''
        addcred_degdiploma2 = ''

                                                                    
    
    #VERIFICATION
    try:
        verification_element = driver.find_element_by_class_name('prof-verified-text')
        verification = 'YES'
    except Exception as error:
        verification = 'NO'

    
    #PROFESSIONAL CONNECTIONS
    try:
        pro_connect_element = driver.find_element_by_id('tabs-connections').find_elements_by_tag_name('a')
        pro_connect_list = []
        for i in pro_connect_element:
            pro_connect_list.append(i.text)
        pro_connect = ','.join(pro_connect_list)
    except Exception as error:
        pro_connect = ''

    
    #THERAPIST groupss
    try:
        groupss_element = driver.find_element_by_class_name('group-small').find_elements_by_tag_name('h5')
        groupss_list = []
        for i in groupss_element:
            groupss_list.append(i.text)
        groupss = ';'.join(groupss_list)

    except Exception as error:
        groupss = ''


    #ADDRESS 1 and 2

    address1 = ''
    address2 = ''

    try:
        addresses = driver.find_elements_by_class_name('location-address-phone')
                            
        if len(addresses) == 2 or len(addresses) == 4:
            address = addresses[0].find_elements_by_tag_name('span')
            address_list = []

            for i in address:
                address_list.append (i.get_attribute('textContent'))
                address1 = ','.join(address_list)
                

        if len(addresses) == 4:
            address = addresses[1].find_elements_by_tag_name('span')
            address_list2 = []
            for i in address:
                address_list2.append (i.get_attribute('textContent'))
                address2 = ','.join(address_list2)

    except Exception as error:
        address1 = ''
        address2 = ''


    # PROFILE_PIX
    try:
        if 'https://' in profile_photolink:
            photodata = requests.get(profile_photolink)
            profile_pix = photodata.content

        else:
            photodata = requests.get('https://' + profile_photolink)
            profile_pix = photodata.content
            
    except Exception as error:
        profile_pix = ''


    # WEBSITE URL
    try:
        website_element = driver.find_element_by_xpath('//*[@id="profileContainer"]/div[2]/div[1]/div/div[2]/div/a[2]').click()
        time.sleep(5)
        # to click on website link and return back to main window
        main_window_handle = None
        while not main_window_handle:
            driver.switch_to_window(driver.window_handles[1])
            website_url = driver.current_url
            driver.close()
            break
        driver.switch_to.window(driver.window_handles[0])

        # if len(driver.window_handles) > 1:
        #     driver.switch_to_window(driver.window_handles[1])
        #     website_url = driver.current_url

        # else:
        #     website_url = ''

    except Exception as error:
        website_url = 'NO WEBSITE'



    
    
    query2 = "INSERT INTO psychtoday.psychologytoday2 (profile_link, profile_photolink, name, title, phone, spec_top, spec_issues, spec_mental, spec_sex, clientfocus_ethnic, clientfocus_speak, clientfocus_faith, clientfocus_age, clientfocus_community, treatapproach_typestherapy, treatapproach_modality, about, fo_cps, fo_slidingscale, fo_payby, fo_insurance, ft_sessionfee, ft_couplefee, ft_payby, qual_practice, qual_school, qual_gradyear, qual_licensestate, qual_licenseprovince, qual_supervisor, qual_supervisorlicense, qual_membership, qual_training, qual_degdiploma, addcred_certificate1, addcred_certificate2, addcred_certificate_date1, addcred_certificate_date2, addcred_membership, addcred_degdiploma1, addcred_degdiploma2, verification, pro_connect, groupss, address1, address2, website_url, profile_pix)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
    args2 = (profile_link, profile_photolink, name, title, phone, spec_top, spec_issues, spec_mental, spec_sex,clientfocus_ethnic, clientfocus_speak, clientfocus_faith, clientfocus_age, clientfocus_community, treatapproach_typestherapy, treatapproach_modality, about, fo_cps, fo_slidingscale, fo_payby, fo_insurance, ft_sessionfee, ft_couplefee, ft_payby, qual_practice, qual_school, qual_gradyear, qual_licensestate, qual_licenseprovince, qual_supervisor, qual_supervisorlicense, qual_membership, qual_training, qual_degdiploma, addcred_certificate1, addcred_certificate2, addcred_certificate_date1, addcred_certificate_date2, addcred_membership, addcred_degdiploma1, addcred_degdiploma2, verification, pro_connect, groupss, address1, address2, website_url, profile_pix)
	
    try:
        cur.execute(query2, args2)
        conn.commit()
        print ("Data saved successfully!")

    except Exception as error:
        print("Error saving database with error: "+str(error))

    # cur.execute("SELECT * FROM psychtoday.psychologytoday2")
    # visualise = cur.fetchall()
    # for v in visualise:
    #     print(v[45:])


    rowcounter +=1
    if rowcounter % 10 is 0:
        print (rowcounter)
    else:
        pass
   





    #TO PRINT TO TERMINAL
    print(profile_link, profile_photolink, name, title, phone, spec_top, spec_issues, spec_mental, spec_sex,clientfocus_ethnic,
clientfocus_speak, clientfocus_faith, clientfocus_age, clientfocus_community, treatapproach_typestherapy,
treatapproach_modality, about, fo_cps, fo_slidingscale, fo_payby, fo_insurance, ft_sessionfee, ft_couplefee,
ft_payby, qual_practice, qual_school, qual_gradyear, qual_licensestate, qual_licenseprovince, qual_supervisor,  
qual_supervisorlicense, qual_membership, qual_training, qual_degdiploma, addcred_certificate1, addcred_certificate2, 
addcred_certificate_date1, addcred_certificate_date2, addcred_membership, addcred_degdiploma1, addcred_degdiploma2,  
verification, pro_connect, groupss, website_url, address1, address2)



    print("PROCEEDING TO NEXT THERAPIST")
    print("PROCEEDING TO NEXT THERAPIST")
    

driver.quit()

    

cur.close()
conn.close()


"""


