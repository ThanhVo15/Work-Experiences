import os
import traceback
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import re

# Define destination path
dest_path = os.path.dirname(os.path.realpath(__file__)) + '/data_source/car_test/'

# Ensure the directory exists
if not os.path.exists(dest_path):
    os.makedirs(dest_path)

arr_url = ['https://www.classic.com/m/porsche/911/964/carrera-2/coupe-automatic/']

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": dest_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})


def extract_event_data(data_list):
    extracted_data = []
    i = 0
    while i < len(data_list):
        if re.match(r'\\ue[0-9a-fA-F]{3}', repr(data_list[i])):
            try:
                date = data_list[i + 1]
                event = ' '.join(data_list[i + 2: i + 6]).replace('  ', ' ')
                details = data_list[i + 6] + ' ' + data_list[i + 7]
                extracted_data.append({
                    'Date': date,
                    'Event': event,
                    'Details': details
                })
                i += 8
            except IndexError:
                i += 1
        else:
            i += 1
    return extracted_data 


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

for url in arr_url:
    driver.get(url)
    driver.maximize_window()
    print('Starting to request %s' % url)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Locate elements containing car information
        child = driver.find_elements(By.XPATH, "//*[@class= 'text-xl leading-5 font-medium table:text-secondary table:text-base flex-1']")
        arr_car = []
        df_5 = pd.DataFrame()

        # Extract hrefs of car listings
        for i in range(len(child)):
            href = child[i].get_attribute("href")
            arr_car.append(href)

        # Loop through each car listing
        for car_url in arr_car:
            driver.get(car_url)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='vehicle-tabs']")))
            element = driver.find_elements(By.XPATH, "//*[@id='vehicle-tabs']")

            # Extract the text content and split it by new lines
            arr_temp = element[0].text.split('\n')
            print(arr_temp)
            
            event_data = extract_event_data(arr_temp)
            for event in event_data:
                df_event = pd.DataFrame([{
                        'Date': event['Date'],
                        'Event': event['Event'],
                        'Details': event['Details']
                    }])
                df_5 = pd.concat([df_5, df_event])
            print(df_5)
    except:
        print(traceback.format_exc())

driver.quit()
