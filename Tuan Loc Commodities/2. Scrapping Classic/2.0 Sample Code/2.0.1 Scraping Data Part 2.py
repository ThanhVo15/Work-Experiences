import os
import sys
import csv
import psycopg2
from dateutil.relativedelta import relativedelta
#from config import config
import requests, zipfile
from io import StringIO
import pandas as pd
import datetime
from datetime import *
from pandas import DataFrame
from datetime import datetime
import shutil
import traceback
from lxml import html
import ast
import json
from haralyzer import HarParser, HarPage

import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from shutil import copyfile, move

import datetime, calendar, dateparser
from datetime import *
from dateutil.relativedelta import relativedelta
import time
import xlrd
import tabula
#from tabula import read_pdf
import pandas as pd
import psycopg2
#from config import *
from selenium.webdriver.firefox.options import Options
import glob
#import camelot

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

#from simple_NER.rules.rx import RegexNER

#from googletrans import Translator
import numpy as np
import statistics
import shutil
from selenium.webdriver.common.action_chains import ActionChains


def download_car(dest_path):
    arr_url = ['https://www.classic.com/m/porsche/911/964/carrera-2/coupe-automatic/','https://www.classic.com/m/porsche/911/993/carrera/cabriolet-manual/','https://www.classic.com/m/porsche/911/993/turbo/']

    options = Options()
    options.headless = True
    firefox_profile = webdriver.FirefoxProfile()

    # Cấu hình các tùy chọn tải xuống từ firefox_profile
    firefox_profile.set_preference("browser.download.folderList", 2)
    firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
    firefox_profile.set_preference("browser.download.dir", dest_path)  
    firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                "application/octet-stream, text/csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/x-excel, application/x-msexcel, application/excel, application/vnd.ms-excel")  
    firefox_profile.set_preference("browser.helperApps.neverAsk.openFile", "application/octet-stream")

    # Truyền options vào WebDriver
    driver = webdriver.Firefox(firefox_profile=firefox_profile, options=options, executable_path=GeckoDriverManager().install())

    for url in arr_url:
        driver.get(url)
        driver.maximize_window()
        print('Starting to requests %s' %url)
        wait = WebDriverWait(driver, 2)
        try:
            driver.save_screenshot(dest_path+'screenshot.png')

            child = driver.find_elements_by_xpath ("//*[@class= 'flex flex-wrap justify-between text-gray-500 table:justify-start table:space-x-3']")
            df_1=pd.DataFrame()
            for i in range(len(child)):
                arr=child[i].text.split('\n')
                # print(arr)
                df_temp=pd.DataFrame([{
                'Mileage':arr[0],
                'Transmission': arr[1],
                'Drive Type': arr[2]
                }])
                df_1=pd.concat([df_1,df_temp])
            df_1=df_1.reset_index(drop=True)
            print(df_1)

            child = driver.find_elements_by_xpath ("//*[@class= 'flex gap-2 items-center text-gray-500']")
            df_2=pd.DataFrame()
            for i in range(len(child)):
                df_temp=pd.DataFrame([{
                'Selling location':child[i].text
                }])
                df_2=pd.concat([df_2,df_temp])
            df_2=df_2.reset_index(drop=True)

            child = driver.find_elements_by_xpath ("//*[@class= 'debug:bg-emerald-100 w-1/2 table:flex-1 table:text-left table:space-y-1']")
            df_3=pd.DataFrame()
            for i in range(len(child)):
                arr=child[i].text.split('\n')
                price=None

                if len(arr)==2:
                    price=arr[1]
                df_temp=pd.DataFrame([{
                'Sold':arr[0],
                'Selling price':price
                }])
                df_3=pd.concat([df_3,df_temp])
            df_3=df_3.reset_index(drop=True)

            child = driver.find_elements_by_xpath ("//*[@class= 'debug:bg-violet-100 text-sm text-gray-500 text-right w-1/2 table:flex-1 table:order-last ']")
            df_4=pd.DataFrame()
            for i in range(len(child)):
                df_temp=pd.DataFrame([{
                'Date of publication ':datetime.strptime(child[i].text.split('\n')[0],'%b %d, %Y').date(),
                }])
                df_4=pd.concat([df_4,df_temp])
            df_4=df_4.reset_index(drop=True)



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
                print(element[0].text)
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
                            # element_with_text_bids =driver.find_elements_by_xpath ("//*[@text='bids']")
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

                # break
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

    dest_path = os.path.dirname(os.path.realpath(__file__))  + '/data_source/car_test/'
    print(dest_path)
    download_car(dest_path)
