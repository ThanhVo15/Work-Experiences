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

def download_car(dest_path):
    arr_url = [
        'https://www.classic.com/m/porsche/911/964/carrera-2/coupe-automatic/',
        'https://www.classic.com/m/porsche/911/993/carrera/cabriolet-manual/',
        'https://www.classic.com/m/porsche/911/993/turbo/'
    ]

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": dest_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    for url in arr_url:
        driver.get(url)
        driver.maximize_window()
        print(f'Starting to request {url}')
        wait = WebDriverWait(driver, 10)

        try:
            driver.save_screenshot(os.path.join(dest_path, 'screenshot.png'))

            child = driver.find_elements(By.XPATH, "//*[@class='flex flex-wrap justify-between text-gray-500 table:justify-start table:space-x-3']")
            df_1 = pd.DataFrame()
            for element in child:
                arr = element.text.split('\n')
                df_temp = pd.DataFrame([{
                    'Mileage': arr[0],
                    'Transmission': arr[1],
                    'Drive Type': arr[2]
                }])
                df_1 = pd.concat([df_1, df_temp])
            df_1 = df_1.reset_index(drop=True)
            print(df_1)

            child = driver.find_elements(By.XPATH, "//*[@class='flex gap-2 items-center text-gray-500']")
            df_2 = pd.DataFrame()
            for element in child:
                df_temp = pd.DataFrame([{
                    'Selling location': element.text
                }])
                df_2 = pd.concat([df_2, df_temp])
            df_2 = df_2.reset_index(drop=True)

            child = driver.find_elements(By.XPATH, "//*[@class='debug:bg-emerald-100 w-1/2 table:flex-1 table:text-left table:space-y-1']")
            df_3 = pd.DataFrame()
            for element in child:
                arr = element.text.split('\n')
                price = arr[1] if len(arr) == 2 else None
                df_temp = pd.DataFrame([{
                    'Sold': arr[0],
                    'Selling price': price
                }])
                df_3 = pd.concat([df_3, df_temp])
            df_3 = df_3.reset_index(drop=True)

            child = driver.find_elements(By.XPATH, "//*[@class='debug:bg-violet-100 text-sm text-gray-500 text-right w-1/2 table:flex-1 table:order-last ']")
            df_4 = pd.DataFrame()
            for element in child:
                df_temp = pd.DataFrame([{
                    'Date of publication ': datetime.strptime(element.text.split('\n')[0], '%b %d, %Y').date(),
                }])
                df_4 = pd.concat([df_4, df_temp])
            df_4 = df_4.reset_index(drop=True)

            child = driver.find_elements(By.XPATH, "//*[@class='text-xl leading-5 font-medium table:text-secondary table:text-base flex-1']")
            arr_car = []
            df_5 = pd.DataFrame()
            for element in child:
                name = element.text
                href = element.get_attribute("href")
                arr_car.append(href)

            for car_url in arr_car:
                driver.get(car_url)
                WebDriverWait(driver, 5)
                driver.save_screenshot(os.path.join(dest_path, 'screenshot_1.png'))
                element = driver.find_element(By.XPATH, "//*[@id='vehicle-tabs']")
                arr_temp = element.text.split('\n')
                index_1 = arr_temp.index('Year')
                index_2 = arr_temp.index('Int. Color Group')
                arr_after = arr_temp[index_1:index_2 + 2]
                df_temp = pd.DataFrame([{
                    'Manufacturer': arr_after[3],
                    'Model Family': arr_after[5],
                    'Model Generation': arr_after[7],
                    'Production year': arr_after[1],
                    'VIN of the vehicle': arr_after[23],
                    'Ext. Color Group': arr_after[-3],
                    'Int. Color Group': arr_after[-1],
                }])

                child_4 = driver.find_elements(By.XPATH, "//*[@class='flex text-gray-500 pl-2 ml-auto ']")
                if len(child_4) >= 2:
                    df_temp['Date of sale/ending'] = datetime.strptime(child_4[1].text, '%b %d, %Y').date()
                    child_1 = driver.find_elements(By.XPATH, "//*[@class='flex md:inline-flex items-center justify-center px-5 py-2 uppercase font-medium tracking-wider whitespace-nowrap rounded transition duration-200 text-blue-500 border border-blue-500 hover:bg-blue-50 w-full h-full']")
                    if child_1:
                        try:
                            driver.get(child_1[0].get_attribute("href"))
                            WebDriverWait(driver, 5)
                            driver.save_screenshot(os.path.join(dest_path, 'screenshot_3.png'))

                            child_2 = driver.find_elements(By.XPATH, "//*[@class='col-sm-3 gallery__node gallery__thumb bottom_gallery_node ']")
                            df_temp['Number of pictures in listing'] = len(child_2)
                            child_3 = driver.find_elements(By.XPATH, "//*[@class='ytp-cued-thumbnail-overlay-image']")
                            df_temp['Number of videos in listing'] = len(child_3)

                            element_with_text_bids = driver.find_elements(By.XPATH, "//*[translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='bids']")
                            if element_with_text_bids:
                                parent_element = element_with_text_bids[0].find_element(By.XPATH, "..")
                                name_class = parent_element.get_attribute("class")
                                child_5 = driver.find_elements(By.XPATH, f"//*[@class='{name_class}']")
                                df_temp['Total number of bids'] = child_5[2].text if len(child_5) == 3 else child_5[0].text
                            else:
                                df_temp['Total number of bids'] = None
                        except:
                            print(traceback.format_exc())
                            df_temp['Number of pictures in listing'] = None
                            df_temp['Number of videos in listing'] = None
                            df_temp['Total number of bids'] = None
                    else:
                        df_temp['Number of pictures in listing'] = None
                        df_temp['Number of videos in listing'] = None
                        df_temp['Total number of bids'] = None
                else:
                    df_temp['Date of sale/ending'] = None
                    df_temp['Number of pictures in listing'] = None
                    df_temp['Number of videos in listing'] = None
                    df_temp['Total number of bids'] = None

                df_5 = pd.concat([df_5, df_temp])
            df_5 = df_5.reset_index(drop=True)
            df = pd.concat([df_1, df_2, df_3, df_4, df_5], axis=1)
            df['Interior material'] = None
            df.to_csv(os.path.join(dest_path, url.replace('https://www.classic.com/m/', '').replace('/', '') + '.csv'), index=False)

        except Exception as e:
            print(traceback.format_exc())

    driver.quit()

if __name__ == '__main__':
    dest_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data_source', 'car_test')
    os.makedirs(dest_path, exist_ok=True)
    print(dest_path)
    download_car(dest_path)
