import os
import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def download_history_car(arr_urls, dest_path):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": dest_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    all_data = []

    for url in arr_urls:
        driver.get(url)
        driver.maximize_window()
        print('Starting to requests %s' %url)
        wait = WebDriverWait(driver, 2)
        time.sleep(5)
        try:
            history_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@data-tab='history']"))
            )
            history_tab.click()
        except Exception:
            continue
        time.sleep(5)

        blocks = driver.find_elements_by_xpath("//div[@class='history-item']")

        for block in blocks:
            data = {'URL': url}

            try:
                date_element = block.find_element(By.XPATH, ".//span[contains(@class, 'typography-body2 typography-primary-color typography-sm- typography-md- typography-lg- text-gray-600 mb-1')]")
                date = date_element.text.strip()
                data['Date'] = date
            except Exception:
                pass

            status = ''
            try:
                # Locate the status text using XPath
                status_element = driver.find_element(By.XPATH, "//div[@class='flex justify-start items-center mb-1 flex-wrap']//span[contains(@class, 'typography-body2') and contains(text(), 'Sold at')]")

                # Extract the status text
                status = status_element.text.strip()
            except Exception:
                pass
            data['Status'] = status

            details = ''
            try:
                details_element = driver.find_element(By.XPATH, "//div[@class='flex flex-wrap space-x-1']")
                details = details_element.text.strip()
            except Exception:
                pass
            data['Details'] = details

            all_data.append(data)

    df = pd.DataFrame(all_data)
    df.to_csv(os.path.join(dest_path, 'output_data.csv'), index=False)
    driver.quit()

if __name__ == '__main__':
    file_path = r"D:\GitHub\Work-Experiences\Tuan Loc Commodities\2. Scrapping Classic\2.1 My Own Scrapping Code\2.1.2 Scraping Vehicle History\found links.txt"

    with open(file_path, 'r') as file:
        arr_urls = file.read().splitlines()

    dest_path = r'D:\GitHub\Work-Experiences\Tuan Loc Commodities\2. Scrapping Classic\2.0 Sample Code\data_source\car_test'

    download_history_car(arr_urls, dest_path)
