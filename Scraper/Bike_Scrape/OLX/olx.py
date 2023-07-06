from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options


from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import numpy as np


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)
driver.get("https://www.olx.in/bikes_c2198/")
sleep(10)


# Loading the data
while True:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    try:
        wait.until(lambda driver: driver.find_element(By.CLASS_NAME, '_38O09'))
    except:
        sleep(10)
        break
    driver.find_element(By.CLASS_NAME, '_38O09').click()
    sleep(2)
    
    

'''
driver.get("https://www.olx.in/")
sleep(10)



# Goint to Bike page
search_element =  driver.find_element(By.CLASS_NAME, '_1044D')
search_element.find_element(By.TAG_NAME, 'input').send_keys('bike')
driver.find_element(By.CLASS_NAME, '_3jHVg').click()

sleep(5)


# Loading the data
# while True:
#     driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#     try:
#         wait.until(lambda driver: driver.find_element(By.CLASS_NAME, '_38O09'))
#     except:
#         sleep(10)
#         break
#     driver.find_element(By.CLASS_NAME, '_38O09').click()
#     sleep(2)


links = [i.get_attribute('href') for i in driver.find_elements(By.CSS_SELECTOR, "li[class='_1DNjI']>a")]
for i in links:
    driver.execute_script("window.open('');")
    
    # Switch to the new window and open new URL
    driver.switch_to.window(driver.window_handles[1])
    driver.get(i)
    sleep(3)
    
    # Closing new_url tab
    driver.close()
    
    # Switching to old tab
    driver.switch_to.window(driver.window_handles[0])

    # driver.execute_script(f"window.open('{i}');")


sleep(5)
# for i in driver.find_elements(By.CLASS_NAME, '_38O09'):
#     print(i.click())
#     sleep(5)
'''

driver.get('https://www.olx.in/item/claccic-bullet-iid-1736031979')
price = driver.find_element(By.CLASS_NAME, 'T8y-z').text

Kms_Driven = driver.find_element(By.CLASS_NAME, 'dBLgK').text

for i in driver.find_elements(By.CLASS_NAME, '_1O2tT'):
    index = i.find_element(By.CLASS_NAME, '_3V4pD').text
    value = i.find_element(By.CLASS_NAME, 'B6X7c').text
    dict1 = {
        index:value
    }
    print(dict1)
    
    #SelectCity > div > div > div > div > div.ReactTypeahead.inputfield.gs_ta.active > div > div > ul > li:nth-child(10)