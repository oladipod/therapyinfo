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

driver = webdriver.Chrome(ChromeDriverManager().install())




# CREATE CONNETION TO DATABASE AND CREATE A TABLE
# conn = pymysql.connect(database = 'mysql', user = 'root', passwd ='90RrgyX0Nx9wCxWtE1Sc', host = '167.99.98.149:22' )
conn = pymysql.connect(host='167.99.98.149',user='remoteroot',passwd='9ZLkPeH4VZ!!p7t+nyE',port=3306)

cur = conn.cursor()
print(conn)

# cur.execute("CREATE DATABASE psychtoday")
# conn.commit

# query1 = "CREATE TABLE psychtoday.psychologytoday(therapist_id INT AUTO_INCREMENT PRIMARY KEY, profile_link VARCHAR(500), profile_photolink VARCHAR(500), name VARCHAR(500), title VARCHAR(500), phone VARCHAR(500), spec_top VARCHAR(500), spec_issues VARCHAR(500), spec_mental VARCHAR(500), spec_sex VARCHAR(500), clientfocus_ethnic VARCHAR(500), clientfocus_speak VARCHAR(500), clientfocus_faith VARCHAR(500), clientfocus_age VARCHAR(500), clientfocus_community VARCHAR(500), treatapproach_typestherapy VARCHAR(500), treatapproach_modality VARCHAR(500), about TEXT(1000), fo_cps VARCHAR(500), fo_slidingscale VARCHAR(500), fo_payby VARCHAR(500), fo_insurance VARCHAR(500), ft_sessionfee VARCHAR(500), ft_couplefee VARCHAR(500), ft_payby VARCHAR(500), qual_practice VARCHAR(500), qual_school VARCHAR(500), qual_gradyear VARCHAR(500), qual_licensestate VARCHAR(500), qual_licenseprovince VARCHAR(500), qual_supervisor VARCHAR(500), qual_supervisorlicense VARCHAR(500), qual_membership VARCHAR(500), qual_training VARCHAR(500), qual_degdiploma VARCHAR(500), addcred_certificate1 VARCHAR(500), addcred_certificate2 VARCHAR(500), addcred_certificate_date1 VARCHAR(500), addcred_certificate_date2 VARCHAR(500), addcred_membership VARCHAR(500), addcred_degdiploma1 VARCHAR(500), addcred_degdiploma2 VARCHAR(500),  verification VARCHAR(500), pro_connect VARCHAR(500), groupss VARCHAR(500), address1 VARCHAR(500), address2 VARCHAR(500), website_url VARCHAR(500), profile_pix BLOB)"
# cur.execute(query1)
# conn.commit()


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument('--start-maximized--')


# driver = webdriver.Chrome(executable_path = 'chromedriver', options=chrome_options)
action = ActionChains(driver)
#driver.maximize_window()

main_urls = [ 'https://www.psychologytoday.com/nz/counselling', 'https://www.psychologytoday.com/cl/psicologos']


profile_link_list = []
navlinks = [] 
for main_url in main_urls:
        driver.get(main_url)
        driver.implicitly_wait(3)

        #links of the states in each country  
        statelinks_obj = driver.find_elements_by_class_name('listItems')[0].find_elements_by_tag_name('a')     
         
        for i in statelinks_obj[:3]:    
            navlinks.append(i.get_property('href'))
            
        #to get the webpage of each links of state, 
        for j in navlinks:
            driver.get(j)
            print('NOW PROCEEDING TO', j )
            #time.sleep(5)
            
            #toget the profile link of each therapist on the list pge
            condition = True
            while condition:  
                therapist_link = driver.find_elements_by_class_name('result-name')
                for k in therapist_link[:3]:  
                    profile_link_list.append(k.get_attribute('href'))
                    
                #pagenation- click the next button till you reach the last page
                try:
                    #perform actions by using javascript statement
                    javaScript = "document.getElementsByClassName('icon-chevron-right')[0].click();"
                    driver.execute_script(javaScript)
                    time.sleep(5)

                    ## next_button = driver.find_elements_by_class_name('icon-chevron-right')[0]
                    ## driver.execute_script(("arguments[0].click();", next_button)
                except Exception as error:
                    condition = False

            print(len(profile_link_list))


rowcounter = 1
#get all therapist links
for link in profile_link_list[:8]:
    profile_page = driver.get(link)
    driver.wait = WebDriverWait(driver, 2)


    #TO START GETTING ALL REQUIRED FIELDS ON EACH PAGE

    #profile_link
    profile_link = link
    print(profile_link)

    #name
    try:
        name = str(driver.find_element_by_xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[1]/h1').text)
    except Exception as error:
        name = ''

    print(name)

    #profile_photolink
    try:
        profile_photolink = driver.find_element_by_xpath('//*[@id="profilePhoto"]/img').get_attribute('src')
    except Exception as error:
        profile_photolink = ''
    print(profile_photolink)

    #title
    try:
        title = driver.find_element_by_xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[1]/div').text
    except Exception as error:
        title = ''
    print(title)

    #phone
    try:
        phone = driver.find_element_by_xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[2]/div/span/a').text
    except Exception as error:
        phone = ''
    print(phone)
    
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
    print(spec_top)


    #spec_issues

    try:
        spec_issues_element = driver.find_element_by_xpath('//*[@id="profile-content"]/div/div[2]/div[2]/div[2]/div').find_elements_by_tag_name('li')
        spec_issues_list = []
        for i in spec_issues_element:
            spec_issues_list.append(i.text) 
        spec_issues = ', '.join(spec_issues_list)
    except Exception as error:
        spec_issues = ''
    print(spec_issues)


    #spec_mental

    try:
        spec_mental_element = driver.find_element_by_xpath('//*[@id="profile-content"]/div/div[2]/div[2]/div[3]/div').find_elements_by_tag_name('li')
        spec_mental_list = []
        for i in spec_mental_element:
            spec_mental_list.append(i.text) 
        spec_mental = ', '.join(spec_mental_list)
    except Exception as error:
        spec_mental = ''
    print(spec_mental)


    #spec_sex

    try:
        spec_sex_element = driver.find_element_by_class_name('attributes-sexuality').find_elements_by_tag_name('li')
        spec_sex_list = []
        for i in spec_sex_element:
            spec_sex_list.append(i.text)
        spec_sex = ', '.join(spec_sex_list)
    except Exception as error:
            spec_sex = ''
    print(spec_sex)

    #clientfocus_ethnic

    try:
        clientfocus_ethnic_element = driver.find_element_by_class_name('attributes-ethnicity-focus').find_elements_by_tag_name('span')[1:]
        clientfocus_ethnic_list = []
        for i in clientfocus_ethnic_element:
            clientfocus_ethnic_list.append(i.text) 
        clientfocus_ethnic = ', '.join(clientfocus_ethnic_list)
    except Exception as error:
        clientfocus_ethnic = ''
    print(clientfocus_ethnic)

    
    #clientfocus_speak
    try:
        clientfocus_speak_element = driver.find_element_by_class_name('attributes-language').find_elements_by_tag_name('span')[1:]
        clientfocus_speak_list = []
        for i in clientfocus_speak_element:
            clientfocus_speak_list.append(i.text) 
        clientfocus_speak = ', '.join(clientfocus_speak_list)
    except Exception as error:
        clientfocus_speak = ''
    print(clientfocus_speak)


    #clientfocus_faith
    try:
        clientfocus_faith_element = driver.find_element_by_class_name('attributes-religion').find_elements_by_tag_name('span')[1:]
        clientfocus_faith_list = []
        for i in clientfocus_faith_element:
            clientfocus_faith_list.append(i.text) 
        clientfocus_faith = ', '.join(clientfocus_faith_list)
    except Exception as error:
        clientfocus_faith = ''
    print(clientfocus_faith)


    #clientfocus_age
    try:
        clientfocus_age_element = driver.find_element_by_class_name('attributes-age-focus').find_elements_by_tag_name('li')
        clientfocus_age_list = []
        for i in clientfocus_age_element:
            clientfocus_age_list.append(i.text) 
        clientfocus_age = ', '.join(clientfocus_age_list)
    except Exception as error:
        clientfocus_age = ''
    print(clientfocus_age)


    #clientfocus_community
    try:
        clientfocus_community_element = driver.find_element_by_class_name('attributes-categories').find_elements_by_tag_name('li')
        clientfocus_community_list = []
        for i in clientfocus_community_element:
            clientfocus_community_list.append(i.text) 
        clientfocus_community = ', '.join(clientfocus_community_list)
    except Exception as error:
        clientfocus_community = ''
    print(clientfocus_community)
    
    #treatapproach_typestherapy
    try:
        treatapproach_therapy_element = driver.find_element_by_class_name('attributes-treatment-orientation').find_elements_by_tag_name('span')
        treatapproach_therapy_list = []
        for i in treatapproach_therapy_element:
            treatapproach_therapy_list.append(i.text)
        treatapproach_typestherapy = ', '.join(treatapproach_therapy_list)

    except Exception as error:
        treatapproach_typestherapy = ''

    print(treatapproach_typestherapy)

    #treatapproach_modality

    try:
        treatapproach_modality_element = driver.find_element_by_class_name('attributes-modality').find_elements_by_tag_name('li')
        treatapproach_modality_list = []
        for i in treatapproach_modality_element:
            treatapproach_modality_list.append(i.text) 
        treatapproach_modality = ', '.join(treatapproach_modality_list)
    except Exception as error:
        treatapproach_modality = ''
    print(treatapproach_modality)


    #about

    try:
        about_element = driver.find_element_by_class_name('profile-personalstatement').find_elements_by_class_name('statementPara')
        about_list = []
        for i in about_element:
            about_list.append(i.text) 
            about = ' '.join(about_list)
    except Exception as error:
        about = ''
    print(about)
    
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
    print(fo_cps, fo_slidingscale)


    #fo_payby
    try:
        unspecified_fo_element2 = driver.find_element_by_class_name('attributes-payment-method').find_elements_by_tag_name('span')
        fo_payby_list = []
        for i in unspecified_fo_element2:
            fo_payby_list.append(i.text)
        fo_payby = ' '.join(fo_payby_list[1:])

    except Exception as error:
        fo_payby = ''

    print(fo_payby)


    #fo_insurance
    try:
        unspecified_fo_element3 = driver.find_element_by_class_name('attributes-insurance').find_elements_by_tag_name('li')
        fo_insurance_list = []
        for i in unspecified_fo_element3:
            fo_insurance_list.append(i.text)
        fo_insurance = ','.join(fo_insurance_list)

    except Exception as error:
        fo_insurance = ''
    print(fo_insurance)
    

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

    print(ft_couplefee, ft_sessionfee, ft_payby)

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

    print(qual_degdiploma)
    print(qual_gradyear)
    print(qual_membership)
    print(qual_practice, qual_school, qual_gradyear, qual_licensestate) 
    print(qual_licenseprovince, qual_supervisor, qual_supervisorlicense, qual_training)

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

    print(addcred_certificate1)
    print(addcred_certificate2)
    print(addcred_certificate_date1)
    print(addcred_certificate_date2)
    print(addcred_membership)
    print(addcred_degdiploma1)




    
    #VERIFICATION
    try:
        verification_element = driver.find_element_by_class_name('prof-verified-text')
        verification = 'YES'
    except Exception as error:
        verification = 'NO'

    print(verification)

    
    #PROFESSIONAL CONNECTIONS
    try:
        pro_connect_element = driver.find_element_by_id('tabs-connections').find_elements_by_tag_name('a')
        pro_connect_list = []
        for i in pro_connect_element:
            pro_connect_list.append(i.text)
        pro_connect = ','.join(pro_connect_list)
    except Exception as error:
        pro_connect = ''
    print(pro_connect)
    
    #THERAPIST groupss
    try:
        groupss_element = driver.find_element_by_class_name('group-small').find_elements_by_tag_name('h5')
        groupss_list = []
        for i in groupss_element:
            groupss_list.append(i.text)
        groupss = ';'.join(groupss_list)

    except Exception as error:
        groupss = ''
    print(groupss)

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

    print(address1)
    print(address2)


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

    print(profile_pix)

    # WEBSITE URL
    try:
        website_element = driver.find_element_by_xpath('//*[@id="profileContainer"]/div[2]/div[1]/div/div[2]/div/a[2]').click()
        time.sleep(5)
        
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

    print(website_url)

    
    
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
#     print(profile_link, profile_photolink, name, title, phone, spec_top, spec_issues, spec_mental, spec_sex,clientfocus_ethnic,
# clientfocus_speak, clientfocus_faith, clientfocus_age, clientfocus_community, treatapproach_typestherapy,
# treatapproach_modality, about, fo_cps, fo_slidingscale, fo_payby, fo_insurance, ft_sessionfee, ft_couplefee,
# ft_payby, qual_practice, qual_school, qual_gradyear, qual_licensestate, qual_licenseprovince, qual_supervisor,  
# qual_supervisorlicense, qual_membership, qual_training, qual_degdiploma, addcred_certificate1, addcred_certificate2, 
# addcred_certificate_date1, addcred_certificate_date2, addcred_membership, addcred_degdiploma1, addcred_degdiploma2,  
# verification, pro_connect, groupss, website_url, address1, address2)



    print("PROCEEDING TO NEXT THERAPIST")
    print("PROCEEDING TO NEXT THERAPIST")
    

driver.quit()

    

cur.close()
conn.close()








