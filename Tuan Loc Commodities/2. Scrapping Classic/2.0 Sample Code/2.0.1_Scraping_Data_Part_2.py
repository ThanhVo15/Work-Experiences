import os
import csv
import shutil
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime


def download_car(dest_path):
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

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    # Khởi tạo trình duyệt Chrome
    
    for url in arr_url:
        driver.get(url)
        driver.maximize_window()
        print('Starting to requests %s' % url)
        wait = WebDriverWait(driver, 2)
        try:
            child = driver.find_elements_by_xpath ("//*[@class= 'text-xl leading-5 font-medium table:text-secondary table:text-base flex-1']")
            arr_car=[]
            df_5=pd.DataFrame()

            for i in range(len(child)):
                name=child[i].text
                href = child[i].get_attribute("href")
                arr_car.append(href)

            for i in range(len(arr_car)):

                driver.get(arr_car[i])
                WebDriverWait(driver, 5)
                driver.save_screenshot(dest_path+'screenshot_1.png')
                element = driver.find_elements_by_xpath ("//*[@id='vehicle-tabs']")
                print(element[1].text)
                arr_temp=element[0].text.split('\n')
                print(arr_temp)
                index_1=arr_temp.index('Year')
                index_2=arr_temp.index('Int. Color Group')

                arr_after=arr_temp[index_1:index_2+2]
                print(arr_after)
                # print(len(arr_after))
                df_temp=pd.DataFrame([{
                    'Manufacturer':arr_after[3],
                    'Model Family':arr_after[5],
                    'Model Generation':arr_after[7],
                    'Production year ':arr_after[1],
                    'VIN of the vehicle ':arr_after[23],
                    'Ext. Color Group':arr_after[-3],
                    'Int. Color Group':arr_after[-1],
                }])

                child_4 = driver.find_elements_by_xpath ("//*[@class='flex text-gray-500 pl-2 ml-auto ']")
                if len(child_4)>=2: 
                    df_temp['Date of sale/ending ']=datetime.strptime(child_4[1].text,'%b %d, %Y').date()
                    
                    child_1 = driver.find_elements_by_xpath ("//*[@class= 'flex md:inline-flex items-center justify-center px-5 py-2 uppercase font-medium tracking-wider whitespace-nowrap rounded transition duration-200 text-blue-500 border border-blue-500 hover:bg-blue-50 w-full h-full']")
                    if len(child_1)>0:
                        print(child_1[0].get_attribute("href"))
                        try:
                            driver.get(child_1[0].get_attribute("href"))
                            WebDriverWait(driver, 5)
                            driver.save_screenshot(dest_path+'screenshot_3.png')

                            child_2 = driver.find_elements_by_xpath ("//*[@class= 'col-sm-3 gallery__node gallery__thumb bottom_gallery_node ']")
                            df_temp['Number of pictures in listing']=len(child_2)
                            child_3 = driver.find_elements_by_xpath ("//*[@class= 'ytp-cued-thumbnail-overlay-image']")
                            df_temp['Number of videos in listing']=len(child_3)

                            element_with_text_bids =driver.find_elements_by_xpath ("//*[translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='bids']")
                            element_with_text_bids =driver.find_elements_by_xpath ("//*[@text='bids']")
                            if len(element_with_text_bids)>0:
                                parent_element = element_with_text_bids[0].find_element(By.XPATH, "..")
                                name_class=parent_element.get_attribute("class")
                                child_5 = driver.find_elements_by_xpath (f"//*[@class='{name_class}']")
                                if len(child_5)==3:
                                    df_temp['Total number of bids']=child_5[2].text
                                else:
                                    df_temp['Total number of bids']=child_5[0].text
                            else:
                                df_temp['Total number of bids']=None
                        except:
                            print(traceback.format_exc())
                            df_temp['Number of pictures in listing']=None
                            df_temp['Number of videos in listing']=None
                            df_temp['Total number of bids']=None
                    else:
                        df_temp['Number of pictures in listing']=None
                        df_temp['Number of videos in listing']=None
                        df_temp['Total number of bids']=None
                else:
                    df_temp['Date of sale/ending ']=None
                    df_temp['Number of pictures in listing']=None
                    df_temp['Number of videos in listing']=None
                    df_temp['Total number of bids']=None

                df_5=pd.concat([df_5, df_temp])

            print(df_5)
            df_5=df_5.reset_index(drop=True)
            df=pd.concat([df_1,df_2, df_3, df_4,df_5],axis=1)
            df['Interior material']=None
            print(df)
            df.to_csv(dest_path+url.replace('https://www.classic.com/m/','').replace('/','')+'.csv', index=False)

        except:
            print(traceback.format_exc())
    driver.quit()

if __name__ == '__main__':   
    dest_path = os.path.dirname(os.path.realpath(__file__)) + '/data_source/car_test/'
    print(dest_path)
    download_car(dest_path)
