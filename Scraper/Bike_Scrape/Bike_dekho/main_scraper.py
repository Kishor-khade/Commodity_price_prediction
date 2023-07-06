from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)
driver.get('https://www.bikedekho.com/used-cars+in+ahmedabad')


from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import numpy as np
import re

from places import places_list
all_places = places_list()
base_link = "https://www.bikedekho.com/used-cars+"

Xpath_to_engine_type = '//*[@id="rf01"]/div[1]/div/main/div[1]/div[2]/div/div[4]/div[6]/div/ul/'


def create_dict():
    return {
            'company':[], 
            'model': [],
            'year':[], 
            'kms_driven':[], 
            'cc_type':[],
            'fuel_type':[], 
            'place':[],
            'ownership':[], 
            'price':[],
        }
    

def load_till_last():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(2)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    driver.execute_script("window.scrollTo(0, 150);")
    return None


def split_title_line(text):
    list1 = text.split(' ')

    try:
        if (re.search(r'[1-2][0-9][0-9][0-9]', text).span()[0] == 0):
            year = list1[0]
            list1.pop(0)
        else:
            year=np.nan
    except:
        year=np.nan

    try:
        if (re.search(r'[a-zA-Z]', text).span()[0] == 5):
            company = list1[0]
            list1.pop(0)
        elif (re.search(r'[a-zA-Z]', text).span()[0] == 0):
            company = list1[0]
            list1.pop(0)
        else:
            company = 'others'
    except:
        company = 'others'
    try:
        if list1[0].lower() in ['enfield', 'davidson', 'honda',]:
            company+=' '+list1[0]
            list1.pop(0)
    except:
        pass
    model = ' '.join(list1)

    return year, company, model


def split_dot_list(span_list):
    i = 0
    if span_list[i].text.lstrip().rstrip().lower() not in ['petrol', 'electric', 'first', 'second']:
        kms_driven = span_list[i].text.lstrip().rstrip()
        i+=1
    else:
        kms_driven = np.nan
    if span_list[i].text.lstrip().rstrip()[3:].lower() in ['petrol', 'electric']:
        fuel_type = span_list[i].text.lstrip().rstrip()[3:]
        i+=1
        try:
            ownership = span_list[i].text.lstrip().rstrip()[3:]
        except:
            ownership = np.nan
    elif span_list[i].text.lstrip().rstrip()[3:].lower() in ['first', 'second']:
        fuel_type = np.nan
        ownership = span_list[i].text.lstrip().rstrip()[3:]
    else:
        fuel_type = np.nan
        ownership = np.nan
    # print(kms_driven, fuel_type, ownership)
    # ownership = span_list[i].text.lstrip().rstrip()[3:]
    return kms_driven, fuel_type, ownership


def get_price(price_element):
    price_element.find('sup').decompose()
    price_element.find('span', {'class':'icon-cd_R'}).decompose()
    return price_element.text.rstrip().lstrip()


def get_details(bike_element):
    html_cntnt = bike_element.get_attribute('outerHTML') 
    soup = BeautifulSoup(html_cntnt, 'html.parser')
    kms_driven, fuel_type, ownership = split_dot_list(
        soup.find(
            'div', 
            {'class':'dotlist'}
            ).findChildren()
        )
    price = get_price(
        soup.find(
            'div', 
            {'class':'price'})
        )
    year, company, model = split_title_line(
        soup.find(
            'div', 
            {'class':'title'}
            ).text.rstrip().lstrip()
        )

    return company, model,year,kms_driven,fuel_type,ownership,price


def get_through_cc(cc, cc_num, place, dictionary):
    try:
        if 'cc' in driver.find_element(By.XPATH, f'{Xpath_to_engine_type}li[{str(cc_num)}]/label').text:
            driver.find_element(By.XPATH, f'{Xpath_to_engine_type}li[{str(cc_num)}]/label').click()
        else:
            raise ModuleNotFoundError()
    except:
        try:    
            if 'cc' in driver.find_element(By.XPATH, f'//*[@id="rf01"]/div[1]/div/main/div[1]/div[2]/div/div[4]/div[5]/div/ul/li[{str(cc_num)}]/label').text:
                driver.find_element(By.XPATH, f'//*[@id="rf01"]/div[1]/div/main/div[1]/div[2]/div/div[4]/div[5]/div/ul/li[{str(cc_num)}]/label').click()
            else:
                raise ModuleNotFoundError()
        except:
            pass
    sleep(3)
    load_till_last()
    
    list_of_bikes_element = driver.find_elements(By.CLASS_NAME, 'reportAd')
    
    # print(len(list_of_bikes_element))
    # print(cc)
    for bike_element in list_of_bikes_element:
        company, model,year,kms_driven,fuel_type,ownership,price = get_details(bike_element)
        dictionary['company'].append(company)
        dictionary['model'].append(model)
        dictionary['year'].append(year)
        dictionary['kms_driven'].append(kms_driven)
        dictionary['fuel_type'].append(fuel_type)
        dictionary['ownership'].append(ownership)
        dictionary['price'].append(price)
        dictionary['cc_type'].append(cc)
        dictionary['place'].append(place)
        
    try:
        if 'cc' in driver.find_element(By.XPATH, f'{Xpath_to_engine_type}li[{str(cc_num)}]/label').text:
            driver.find_element(By.XPATH, f'{Xpath_to_engine_type}li[{str(cc_num)}]/label').click()
        else:
            raise ModuleNotFoundError()
    except:
        try:    
            if 'cc' in driver.find_element(By.XPATH, f'//*[@id="rf01"]/div[1]/div/main/div[1]/div[2]/div/div[4]/div[5]/div/ul/li[{str(cc_num)}]/label').text:
                driver.find_element(By.XPATH, f'//*[@id="rf01"]/div[1]/div/main/div[1]/div[2]/div/div[4]/div[5]/div/ul/li[{str(cc_num)}]/label').click()
            else:
                raise ModuleNotFoundError()
        except:
            pass
    return dictionary


def get_through_area(place):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    link = base_link+'in+'+place
    driver.get(link)
    sleep(3)
    
    df = pd.DataFrame(columns=['company', 'model', 'year', 'kms_driven', 'cc_type', 'fuel_type', 'place', 'ownership', 'price'], index=None)
    
    cc_types = [i.text for i in driver.find_elements(By.XPATH, f'{Xpath_to_engine_type}li')]
    num=1
    for cc in cc_types:
        dictionary = create_dict()
        dictionary = get_through_cc(
            cc, 
            num,
            place, 
            dictionary
            )
        num+=1
        df = pd.concat([df, pd.DataFrame(dictionary, index=None)])
        del dictionary
        sleep(3)
    
    # Switching to old tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return df



main_df = pd.read_csv('Scraper/Bike_Scrape/Bike_dekho/BikeDekho.csv')
# main_df = pd.DataFrame()
for place in all_places[:]:
    main_df = pd.concat(
        [
            main_df,
            get_through_area(place.replace(' ', '-').lower())
            ]
        )
    main_df.to_csv('Scraper/Bike_Scrape/Bike_dekho/BikeDekho.csv', index=None)
    print(place)