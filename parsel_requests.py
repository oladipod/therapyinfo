import scrapy
import csv
import time
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
import json
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




class macro(scrapy.Spider):
    name= 'macro'
    custom_settings = {
       'CONCURRENT_REQUESTS': 1,}

    
    def __init__(self):
        self.count=0
        try:
            self.last_memory= json.load(open('last.json','a+'))
            if isinstance(len(self.last_memory),dict):
                
                self.last = self.last_memory['href']
                self.next= self.last_memory['next']
        except:
            self.last_memory={0,0}



        # with open ('AllProfileLinksss.csv', 'w+', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(('s/n', 'Therapists ProfileLink'))
        driver.get('https://www.psychologytoday.com/gb/counselling/isle-of-man')
        driver_cookies = driver.get_cookies()
        user_agent = driver.execute_script("return navigator.userAgent;")
        self.cookies={}
        
        self.headers = {
			'User-Agent': user_agent}
        for cookie in driver_cookies:
            self.cookies[cookie['name']]= cookie['value']
    def start_requests(self):
        # state_urls = ['https://www.psychologytoday.com/gb/counselling/channel-islands', 'https://www.psychologytoday.com/gb/counselling/england', 'https://www.psychologytoday.com/gb/counselling/isle-of-man', 'https://www.psychologytoday.com/gb/counselling/northern-ireland', 
        # 'https://www.psychologytoday.com/gb/counselling/scotland', 'https://www.psychologytoday.com/gb/counselling/wales', 'https://www.psychologytoday.com/en-at/therapists/burgenland', 'https://www.psychologytoday.com/en-at/therapists/carinthia', 'https://www.psychologytoday.com/en-at/therapists/lower-austria', 
        # 'https://www.psychologytoday.com/en-at/therapists/salzburg', 'https://www.psychologytoday.com/en-at/therapists/styria', 'https://www.psychologytoday.com/en-at/therapists/tyrol', 'https://www.psychologytoday.com/en-at/therapists/upper-austria', 'https://www.psychologytoday.com/en-at/therapists/vienna', 'https://www.psychologytoday.com/en-at/therapists/vorarlberg', 
        # 'https://www.psychologytoday.com/en-be/therapists/brussels', 'https://www.psychologytoday.com/en-be/therapists/flanders', 'https://www.psychologytoday.com/en-be/therapists/walloon-region', 'https://www.psychologytoday.com/en-dk/therapists/capital-region-of-denmark', 
        # 'https://www.psychologytoday.com/en-dk/therapists/central-denmark-region', 'https://www.psychologytoday.com/en-dk/therapists/north-denmark-region', 'https://www.psychologytoday.com/en-dk/therapists/region-of-southern-denmark', 'https://www.psychologytoday.com/en-dk/therapists/zealand', 
        # 'https://www.psychologytoday.com/ie/counselling/connacht', 'https://www.psychologytoday.com/ie/counselling/leinster', 'https://www.psychologytoday.com/ie/counselling/munster', 'https://www.psychologytoday.com/ie/counselling/ulster', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/andalucia', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/aragon', 
        # 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/principado-de-asturias', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/islas-baleares', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/pais-vasco', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/islas-canarias', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/cantabria', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/castilla-y-leon', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/castilla-la-mancha', 
        # 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/cataluna', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/ceuta', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/comunidad-de-madrid', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/extremadura', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/galicia', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/la-rioja', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/melilla', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/comunidad-foral-de-navarra', 
        # 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/region-de-murcia', 'https://www.psychologytoday.com/es/psicologos-psicoterapeutas/comunidad-valenciana', 'https://www.psychologytoday.com/en-se/therapists/blekinge-county', 'https://www.psychologytoday.com/en-se/therapists/dalarna-county', 'https://www.psychologytoday.com/en-se/therapists/gavleborg-county', 'https://www.psychologytoday.com/en-se/therapists/gotland', 'https://www.psychologytoday.com/en-se/therapists/halland-county', 'https://www.psychologytoday.com/en-se/therapists/jamtland-county', 'https://www.psychologytoday.com/en-se/therapists/jonkoping-county', 
        # 'https://www.psychologytoday.com/en-se/therapists/kalmar-county', 'https://www.psychologytoday.com/en-se/therapists/kronoberg-county', 'https://www.psychologytoday.com/en-se/therapists/norrbotten-county', 'https://www.psychologytoday.com/en-se/therapists/orebro', 'https://www.psychologytoday.com/en-se/therapists/ostergotland', 'https://www.psychologytoday.com/en-se/therapists/skane', 'https://www.psychologytoday.com/en-se/therapists/sodermanland', 'https://www.psychologytoday.com/en-se/therapists/stockholm-county', 'https://www.psychologytoday.com/en-se/therapists/uppsala-county', 'https://www.psychologytoday.com/en-se/therapists/varmland-county', 
        # 'https://www.psychologytoday.com/en-se/therapists/vasterbotten', 'https://www.psychologytoday.com/en-se/therapists/vasternorrland', 'https://www.psychologytoday.com/en-se/therapists/vastmanland', 'https://www.psychologytoday.com/en-se/therapists/vastra-gotaland', 'https://www.psychologytoday.com/en-ch/therapists/aargau', 'https://www.psychologytoday.com/en-ch/therapists/appenzell-ausserrhoden', 'https://www.psychologytoday.com/en-ch/therapists/appenzell-innerrhoden', 'https://www.psychologytoday.com/en-ch/therapists/basel-city', 'https://www.psychologytoday.com/en-ch/therapists/basel-landschaft', 'https://www.psychologytoday.com/en-ch/therapists/bern', 'https://www.psychologytoday.com/en-ch/therapists/geneva', 'https://www.psychologytoday.com/en-ch/therapists/glarus', 'https://www.psychologytoday.com/en-ch/therapists/grisons', 'https://www.psychologytoday.com/en-ch/therapists/jura', 'https://www.psychologytoday.com/en-ch/therapists/la-sarine', 'https://www.psychologytoday.com/en-ch/therapists/lucerne-district', 
        # 'https://www.psychologytoday.com/en-ch/therapists/neuenburg', 'https://www.psychologytoday.com/en-ch/therapists/nidwalden', 'https://www.psychologytoday.com/en-ch/therapists/obwalden', 'https://www.psychologytoday.com/en-ch/therapists/schaffhausen', 'https://www.psychologytoday.com/en-ch/therapists/schwyz-district', 'https://www.psychologytoday.com/en-ch/therapists/solothurn', 'https://www.psychologytoday.com/en-ch/therapists/st-gallen', 'https://www.psychologytoday.com/en-ch/therapists/thurgau', 'https://www.psychologytoday.com/en-ch/therapists/ticino', 'https://www.psychologytoday.com/en-ch/therapists/uri', 'https://www.psychologytoday.com/en-ch/therapists/valais', 'https://www.psychologytoday.com/en-ch/therapists/vaud', 'https://www.psychologytoday.com/en-ch/therapists/zug', 'https://www.psychologytoday.com/en-ch/therapists/zurich', 'https://www.psychologytoday.com/au/counselling/australian-capital-territory', 'https://www.psychologytoday.com/au/counselling/new-south-wales', 'https://www.psychologytoday.com/au/counselling/northern-territory', 
        # 'https://www.psychologytoday.com/au/counselling/queensland', 'https://www.psychologytoday.com/au/counselling/south-australia', 'https://www.psychologytoday.com/au/counselling/tasmania', 'https://www.psychologytoday.com/au/counselling/victoria', 'https://www.psychologytoday.com/au/counselling/western-australia', 'https://www.psychologytoday.com/hk/counselling/hong-kong', 'https://www.psychologytoday.com/hk/counselling/kowloon', 'https://www.psychologytoday.com/hk/counselling/new-territories', 'https://www.psychologytoday.com/nz/counselling/auckland', 'https://www.psychologytoday.com/nz/counselling/bay-of-plenty', 'https://www.psychologytoday.com/nz/counselling/canterbury', 'https://www.psychologytoday.com/nz/counselling/gisborne', 'https://www.psychologytoday.com/nz/counselling/hawke-s-bay', 'https://www.psychologytoday.com/nz/counselling/manawatu-wanganui', 'https://www.psychologytoday.com/nz/counselling/marlborough', 'https://www.psychologytoday.com/nz/counselling/nelson', 'https://www.psychologytoday.com/nz/counselling/northland', 'https://www.psychologytoday.com/nz/counselling/otago', 'https://www.psychologytoday.com/nz/counselling/southland', 'https://www.psychologytoday.com/nz/counselling/taranaki', 'https://www.psychologytoday.com/nz/counselling/tasman', 'https://www.psychologytoday.com/nz/counselling/waikato', 'https://www.psychologytoday.com/nz/counselling/wellington', 'https://www.psychologytoday.com/nz/counselling/west-coast', 'https://www.psychologytoday.com/cl/psicologos/antofagasta', 'https://www.psychologytoday.com/cl/psicologos/arica-y-parinacota', 'https://www.psychologytoday.com/cl/psicologos/atacama', 'https://www.psychologytoday.com/cl/psicologos/aysen-del-general-carlos-ibanez-del-campo', 'https://www.psychologytoday.com/cl/psicologos/bio-bio', 'https://www.psychologytoday.com/cl/psicologos/coquimbo', 'https://www.psychologytoday.com/cl/psicologos/la-araucania', 'https://www.psychologytoday.com/cl/psicologos/los-lagos', 
        # 'https://www.psychologytoday.com/cl/psicologos/los-rios', 'https://www.psychologytoday.com/cl/psicologos/magallanes-y-de-la-antartica-chilena', 'https://www.psychologytoday.com/cl/psicologos/maule', 'https://www.psychologytoday.com/cl/psicologos/libertador-general-bernardo-ohiggins', 'https://www.psychologytoday.com/cl/psicologos/region-metropolitana-de-santiago', 'https://www.psychologytoday.com/cl/psicologos/tarapaca', 'https://www.psychologytoday.com/cl/psicologos/valparaiso', 'https://www.psychologytoday.com/sg/counselling/sg/singapore', 'https://www.psychologytoday.com/za/counselling/eastern-cape', 'https://www.psychologytoday.com/za/counselling/free-state', 'https://www.psychologytoday.com/za/counselling/gauteng', 'https://www.psychologytoday.com/za/counselling/kwazulu-natal', 'https://www.psychologytoday.com/za/counselling/limpopo', 'https://www.psychologytoday.com/za/counselling/mpumalanga', 'https://www.psychologytoday.com/za/counselling/north-west', 'https://www.psychologytoday.com/za/counselling/northern-cape', 'https://www.psychologytoday.com/za/counselling/western-cape', 'https://www.psychologytoday.com/us/therapists/alabama', 'https://www.psychologytoday.com/us/therapists/alaska', 'https://www.psychologytoday.com/us/therapists/arizona', 'https://www.psychologytoday.com/us/therapists/arkansas', 'https://www.psychologytoday.com/us/therapists/california', 'https://www.psychologytoday.com/us/therapists/colorado', 'https://www.psychologytoday.com/us/therapists/connecticut', 'https://www.psychologytoday.com/us/therapists/delaware', 'https://www.psychologytoday.com/us/therapists/district-of-columbia', 'https://www.psychologytoday.com/us/therapists/florida', 'https://www.psychologytoday.com/us/therapists/georgia', 'https://www.psychologytoday.com/us/therapists/guam', 'https://www.psychologytoday.com/us/therapists/hawaii', 'https://www.psychologytoday.com/us/therapists/idaho', 'https://www.psychologytoday.com/us/therapists/illinois', 'https://www.psychologytoday.com/us/therapists/indiana', 'https://www.psychologytoday.com/us/therapists/iowa', 'https://www.psychologytoday.com/us/therapists/kansas', 'https://www.psychologytoday.com/us/therapists/kentucky', 'https://www.psychologytoday.com/us/therapists/louisiana', 'https://www.psychologytoday.com/us/therapists/maine', 'https://www.psychologytoday.com/us/therapists/maryland', 'https://www.psychologytoday.com/us/therapists/massachusetts', 'https://www.psychologytoday.com/us/therapists/michigan', 'https://www.psychologytoday.com/us/therapists/minnesota', 'https://www.psychologytoday.com/us/therapists/mississippi', 'https://www.psychologytoday.com/us/therapists/missouri', 'https://www.psychologytoday.com/us/therapists/montana', 'https://www.psychologytoday.com/us/therapists/nebraska',
        # 'https://www.psychologytoday.com/us/therapists/nevada', 'https://www.psychologytoday.com/us/therapists/new-hampshire', 'https://www.psychologytoday.com/us/therapists/new-jersey', 'https://www.psychologytoday.com/us/therapists/new-mexico', 
        # 'https://www.psychologytoday.com/us/therapists/new-york', 'https://www.psychologytoday.com/us/therapists/north-carolina', 'https://www.psychologytoday.com/us/therapists/north-dakota', 'https://www.psychologytoday.com/us/therapists/ohio', 'https://www.psychologytoday.com/us/therapists/oklahoma', 'https://www.psychologytoday.com/us/therapists/oregon', 'https://www.psychologytoday.com/us/therapists/pennsylvania', 'https://www.psychologytoday.com/us/therapists/puerto-rico', 'https://www.psychologytoday.com/us/therapists/rhode-island', 'https://www.psychologytoday.com/us/therapists/south-carolina', 'https://www.psychologytoday.com/us/therapists/south-dakota', 'https://www.psychologytoday.com/us/therapists/tennessee', 'https://www.psychologytoday.com/us/therapists/texas', 'https://www.psychologytoday.com/us/therapists/utah', 'https://www.psychologytoday.com/us/therapists/vermont', 'https://www.psychologytoday.com/us/therapists/virgin-islands', 'https://www.psychologytoday.com/us/therapists/virginia', 'https://www.psychologytoday.com/us/therapists/washington', 'https://www.psychologytoday.com/us/therapists/west-virginia', 'https://www.psychologytoday.com/us/therapists/wisconsin', 'https://www.psychologytoday.com/us/therapists/wyoming', 'https://www.psychologytoday.com/ca/therapists/alberta', 'https://www.psychologytoday.com/ca/therapists/british-columbia', 'https://www.psychologytoday.com/ca/therapists/manitoba', 'https://www.psychologytoday.com/ca/therapists/new-brunswick', 'https://www.psychologytoday.com/ca/therapists/newfoundland-and-labrador', 'https://www.psychologytoday.com/ca/therapists/nova-scotia', 'https://www.psychologytoday.com/ca/therapists/ontario', 'https://www.psychologytoday.com/ca/therapists/prince-edward-island', 'https://www.psychologytoday.com/ca/therapists/quebec', 'https://www.psychologytoday.com/ca/therapists/saskatchewan', 'https://www.psychologytoday.com/ca/therapists/yukon', 'https://www.psychologytoday.com/mx/psicologos/aguascalientes', 'https://www.psychologytoday.com/mx/psicologos/baja-california', 'https://www.psychologytoday.com/mx/psicologos/baja-california-sur', 'https://www.psychologytoday.com/mx/psicologos/campeche', 'https://www.psychologytoday.com/mx/psicologos/chiapas', 'https://www.psychologytoday.com/mx/psicologos/chihuahua', 'https://www.psychologytoday.com/mx/psicologos/ciudad-de-mexico', 'https://www.psychologytoday.com/mx/psicologos/coahuila-de-zaragoza', 'https://www.psychologytoday.com/mx/psicologos/colima', 'https://www.psychologytoday.com/mx/psicologos/durango', 'https://www.psychologytoday.com/mx/psicologos/guanajuato', 'https://www.psychologytoday.com/mx/psicologos/guerrero', 'https://www.psychologytoday.com/mx/psicologos/hidalgo', 'https://www.psychologytoday.com/mx/psicologos/jalisco', 
        # 'https://www.psychologytoday.com/mx/psicologos/mexico', 'https://www.psychologytoday.com/mx/psicologos/michoacan-de-ocampo', 'https://www.psychologytoday.com/mx/psicologos/morelos', 'https://www.psychologytoday.com/mx/psicologos/nayarit', 'https://www.psychologytoday.com/mx/psicologos/nuevo-leon', 'https://www.psychologytoday.com/mx/psicologos/oaxaca', 'https://www.psychologytoday.com/mx/psicologos/puebla', 'https://www.psychologytoday.com/mx/psicologos/queretaro', 'https://www.psychologytoday.com/mx/psicologos/quintana-roo', 'https://www.psychologytoday.com/mx/psicologos/san-luis-potosi', 'https://www.psychologytoday.com/mx/psicologos/sinaloa', 'https://www.psychologytoday.com/mx/psicologos/sonora', 'https://www.psychologytoday.com/mx/psicologos/tabasco', 'https://www.psychologytoday.com/mx/psicologos/tamaulipas', 'https://www.psychologytoday.com/mx/psicologos/tlaxcala', 'https://www.psychologytoday.com/mx/psicologos/veracruz-de-ignacio-de-la-llave', 'https://www.psychologytoday.com/mx/psicologos/yucatan', 'https://www.psychologytoday.com/mx/psicologos/zacatecas'
        # ]
        
        all__=['https://www.psychologytoday.com/mx/psicologos/mexico/764862?sid=5ee60d983968b&ref=2&rec_next=21&tr=ResultsName'
            ,'https://www.psychologytoday.com/mx/psicologos/mexico/736038?sid=5ee60d983968b&ref=6&rec_next=21&tr=ResultsName']
        
        # total= len(state_urls)
        # try:
        #     yield scrapy.Request(url=self.last, cookies=self.cookies, headers=self.headers,callback=self.parse,cb_kwargs=dict(count=self.next))
        #     for count, url in enumerate(state_urls[self.next:]):
        #         time.sleep(0.5)
        #         count+=self.next
        #         count+=1
        #         yield scrapy.Request(url=url, cookies=self.cookies, headers=self.headers,callback=self.parse, cb_kwargs=dict(count=count))
        # except:
        for count, url in enumerate(all__[:]):
            # time.sleep(0.5)
            # count+=1
            yield scrapy.Request(url=url, cookies=self.cookies, headers=self.headers,callback=self.parse,cb_kwargs=dict(count=0))

    def parse(self,response,count):
        website = response.xpath('//*[@data-event-label= "website"]/@href').get()
        website_= requests.get(website,cookies =self.cookies, headers=self.headers)
        #website link
        website_link= website_.url
        #profile link
        profile_link= response.request.url
        #name
        try:
            name= response.xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[1]/h1').get()  #no /text()
        except:
            name =''

        #profile photo link
        try:
            profile_photolink = response.xpath('//*[@id="profilePhoto"]/img/@src').get()
        except:
            profile_photolink =''


        #title
        try:
            title = response.xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[1]/div/text()').get()
        except:
            title=''

        #phone
        try:
            phone = response.xpath('//*[@id="profileContainer"]/div[2]/div[2]/div[1]/div[2]/div/span/a/text()').get()
        except:
            phone=''

        #spec_top
    
        try:
            spec_top_element = response.xpath('//*[@class="specialties-list]').xpath('//*[@class="highlight]/text()').extract()
            # spec_top_list = []
            spec_top = ', '.join(spec_top_element)
        except Exception as error:
            spec_top = ''



        #spec_issues

        try:
            spec_issues_element = response.xpath('//*[@id="profile-content"]/div/div[2]/div[2]/div[2]/div').xpath('li/text()').extract()
            # spec_issues_list = []
            spec_issues = ', '.join(spec_issues_element)
        except Exception as error:
            spec_issues = ''



        #spec_mental

        try:
            spec_mental_element = response.xpath('//*[@id="profile-content"]/div/div[2]/div[2]/div[3]/div').xpath('li/text()')
            spec_mental = ', '.join(spec_mental_element)
        except Exception as error:
            spec_mental = ''


        #spec_sex

        try:
            spec_sex_element = response.xpath('//*[@class="attributes-sexuality"]').xpath('li/text()')
            spec_sex = ', '.join(spec_sex_element)
        except Exception as error:
                spec_sex = ''


        #clientfocus_ethnic

        try:
            clientfocus_ethnic_element = response.xpath('//*[@class="attributes-ethnicity-focus"]').xpath('span/text()').extract()[1:]
            clientfocus_ethnic = ', '.join(clientfocus_ethnic_element)
        except Exception as error:
            clientfocus_ethnic = ''


    
        #clientfocus_speak
        try:
            clientfocus_speak_element = response.xpath('//*[@class="attributes-language"]').xpath('span/text()').extract()[1:]
            clientfocus_speak = ', '.join(clientfocus_speak_element)
        except Exception as error:
            clientfocus_speak = ''
    


        #clientfocus_faith
        try:
            clientfocus_faith_element = response.xpath('//*[@class="attributes-religion"]').xpath('span/text()').extract()[1:]
            
            clientfocus_faith = ', '.join(clientfocus_faith_element)
        except Exception as error:
            clientfocus_faith = ''


        #clientfocus_age
        try:
            clientfocus_age_element = response.xpath('//*[@class="attributes-age-focus"]').xpath('li/text()').extract()
            clientfocus_age = ', '.join(clientfocus_age_element)
        except Exception as error:
            clientfocus_age = ''


        #clientfocus_community
        try:
            clientfocus_community_element = response.xpath('//*[@class="attributes-categories"]').xpath('li/text()').extract()
            
            clientfocus_community = ', '.join(clientfocus_community_element)
        except Exception as error:
            clientfocus_community = ''

        
        #treatapproach_typestherapy
        try:
            treatapproach_therapy_element =response.xpath('//*[@class="attributes-treatment-orientation"]').xpath('span/text()').extract()
            treatapproach_typestherapy = ', '.join(treatapproach_therapy_element)

        except Exception as error:
            treatapproach_typestherapy = ''



        #treatapproach_modality

        try:
            treatapproach_modality_element = response.xpath('//*[@class="attributes-modality"]').xpath('li/text()').extract()
            treatapproach_modality = ', '.join(treatapproach_modality_element)
        except Exception as error:
            treatapproach_modality = ''



        #about

        try:
            about_element = response.xpath('//*[@class="profile-personalstatement"]').xpath('//*[@class="statementPara"]/text()').extract()
            about = ' '.join(about_element)
        except Exception as error:
            about = ''

    
        #fo_cps
        #fo_cps , fo_slidingsccale
        try:
            unspecified_fo_element1 = response.xpath('//*[@id="tabs-finances-office"]').xpath('li/text()').extract()
            if len(unspecified_fo_element1) == 2:
                fo_cps = unspecified_fo_element1[0][17:]
                fo_slidingscale = unspecified_fo_element1[1][14:]
            else:
                fo_cps = unspecified_fo_element1[0][17:] 
                fo_slidingscale = ''

        except Exception as error:
            fo_cps = ''
            fo_slidingscale = ''

        #fo_payby
        try:
            unspecified_fo_element2 = response.xpath('//*[@class="attributes-payment-method"]').xpath('span/text()').extract()
            fo_payby = ' '.join(unspecified_fo_element2[1:])

        except Exception as error:
            fo_payby = ''


        #fo_insurance
        try:
            unspecified_fo_element3 = response.xpath('//*[@class="attributes-insurance"]').xpath('li/text()').extract()
            fo_insurance = ','.join(unspecified_fo_element3)

        except Exception as error:
            fo_insurance = ''

        #to click on teletherapy button options
        try:
            teletherapy = response.xpath('//*[@id="select-finances-online"]').click()
            time.sleep(5)

            #ft_sessionfee, ft_couplefee
            ft_sessionfee_element = response.xpath('//*[@id="tabs-finances-online"]').xpath('li/text()').extract()
            ft_sessionfee = ft_sessionfee_element[0][12:]
            ft_couplefee = ft_sessionfee_element[1][20:]

            #ft_payby
            try:
                ft_element = response.xpath('//*[@class="finances-online"]').xpath('span/text').extract()
                ft_payby = ' '.join(ft_element[1:])

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

        qual_element = response.xpath('//*[@class="profile-qualifications"]').xpath('//*[@tag="ul"]').xpath('li/text()').extract()
        qual_textlist_string = ' +++ '.join(qual_element)

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
        addcred_element = response.xpath('//*[@class="profile-additional-credentials"]').xpath('li/text()').extract()
        addcred_textlist_string = ' +++ '.join(addcred_element)
        


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
        verification_element = response.xpath('//*[@class="prof-verified-text"]')
        verification = 'YES'
    except Exception as error:
        verification = 'NO'

    
    #PROFESSIONAL CONNECTIONS
    try:
        pro_connect_element = response.xpath('//*[@id="tabs-connections"]').xpath('a/text()').extract()
        pro_connect = ','.join(pro_connect_element)
    except Exception as error:
        pro_connect = ''

    
    #THERAPIST groupss
    try:
        groupss_element =response.xpath('//*[@class="group-small"]').xpath('h5/text()').extract() 
        groupss = ';'.join(groupss_element)

    except Exception as error:
        groupss = ''


    #ADDRESS 1 and 2

    address1 = ''
    address2 = ''

    try:
        addresses =response.xpath('//*[@class="location-address-phone"]')
                            
        if len(addresses) == 2 or len(addresses) == 4:
            address = addresses[0].xpath('span/@textContent').extract()
            address1 = ','.join(address)
                

        if len(addresses) == 4:
            address = addresses[1].xpath('span/@textContent').extract()
            address2 = ','.join(address)

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


        
        
        
        
        
        
        # time.sleep(0.1)
        # print(response.status)
        # print(type(response.status))
        
        #toget the profile link of each therapist on the list pge
        # profiles= response.xpath('//*[@class ="result-name"]/@href').extract()
        # self.count+=len(profiles)
        # time.sleep(0.5)
        # with open ('AllProfileLinksss.csv', 'a+', newline='') as f:
        #     writer = csv.writer(f)
        #     for link in profiles:
        #         writer.writerow([link])
        #     with open('last.json','w') as f:
        # #         json.dump({"next":count,'href':response.request.url},f)
        # if response.xpath('//*[@class= "btn btn-default btn-next"]'):
        #     # print('\n\nnext page found')
        #     next_page= response.xpath('//*[@class= "btn btn-default btn-next"]/@href').get()
        #     yield scrapy.Request(url=next_page, cookies=self.cookies, headers=self.headers,callback=self.parse,cb_kwargs=dict(count=count))
        # print(f'Total count == {self.count}')




