from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import numpy as np
import re
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)
driver.get('https://www.cars24.com/buy-used-car/')


XPath_to_model_list = '/html/body/div[1]/div[1]/div[2]/div/div/div[1]/div/div[1]/div[3]/ul'


def load_till_last():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.80);")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(3)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    driver.execute_script("window.scrollTo(0, 100);")
    return None



def create_dictionary():
    return {
        'Year':[],
        'Company':[],
        'Model':[],
        'Transmission':[],
        'Engine_Type':[],
        'Kms_Driven':[],
        'ownership':[],
        'Fuel_Type':[],
        'Passing':[],
        'Area':[],
        'Price':[],
    }
    
    

def SplitEngineDetail(html_list):
    transmission = html_list[2].text
    engine_type = html_list[0].text
    return engine_type, transmission


def SplitCarDetails(html_list):
    kms_driven = html_list[0].text
    owner_type = html_list[1].text
    fuel_type = html_list[2].text
    passing = html_list[3].text
    return kms_driven, owner_type, fuel_type, passing



def SplitTitle(text):
    title_list = text.split(' ')
    year = title_list[0]
    model = ' '.join(title_list[2:])
    cmpny = title_list[1]
    return year, cmpny, model


def get_car_details(dictionary, soup):
    year, cmpny, model = SplitTitle(soup.find('h2', {'class':'_2lmIw'}).text)
    engine_type, transmission = SplitEngineDetail(soup.find('ul',{'class':'_1hOnS'}).findChildren())
    kms_driven, owner_type, fuel_type, passing = SplitCarDetails(soup.find('ul',{'class':'_13yb6'}).findChildren())
    price = soup.find('div',{'class':'_18ToE'}).findChildren()[0].text[1:]
    area = soup.find('span',{'class':'_3DYbK'}).text.split(',')[-1]
    dictionary['Year'].append(year)
    dictionary['Company'].append(cmpny)
    dictionary['Model'].append(model)
    dictionary['Transmission'].append(transmission)
    dictionary['Engine_Type'].append(engine_type)
    dictionary['Kms_Driven'].append(kms_driven)
    dictionary['ownership'].append(owner_type)
    dictionary['Fuel_Type'].append(fuel_type)
    dictionary['Passing'].append(passing)
    dictionary['Area'].append(area.replace('\n', ''))
    dictionary['Price'].append(price)
    return dictionary       
    
    
    
def get_current__page_data():
    dictionary = create_dictionary()
    for car_element in driver.find_elements(By.CLASS_NAME, '_2kfVy'):
        html_cntnt = car_element.get_attribute('outerHTML')
        soup = BeautifulSoup(html_cntnt, 'html.parser')
        dictionary = get_car_details(dictionary, soup)

    return pd.DataFrame(dictionary)



def traverse_through_cmpny(car_cmpny_list):
    num = 2
    try:
        df = pd.read_csv('Scraper/Cars_Scrape/Cars_24/Cars_24.csv')
    except:
        df = pd.DataFrame(create_dictionary())
    
    for cmpny in car_cmpny_list[num-2:]:
        # select cmpny 
        sleep(2)
        driver.find_element(By.XPATH,f"{XPath_to_model_list}[{num}]/li/div/div/div/div").click()
        load_till_last()
        df = pd.concat([df, get_current__page_data()])
        
        # deselect cmpny
        sleep(2)
        driver.find_element(By.XPATH,f"{XPath_to_model_list}[{num}]/li/div/div/div/div").click()
        num+=1
        df.to_csv('Scraper/Cars_Scrape/Cars_24/Cars_24.csv', index=None)
        print(cmpny)
        
    

def scrape_data():
    car_cmpny_list = [i.text for i in driver.find_elements(By.XPATH, XPath_to_model_list)[1:] if '(0)' not in i.text]
    return traverse_through_cmpny(car_cmpny_list)

scrape_data()
# print(create_dictionary())