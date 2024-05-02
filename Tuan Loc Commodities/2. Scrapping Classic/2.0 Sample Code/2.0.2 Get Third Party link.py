import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import FirefoxOptions
import requests
from bs4 import BeautifulSoup

# Thiết lập cookies và headers
cookies = {
    '_classic_frontend_key': 'SFMyNTY.g3QAAAAGbQAAAAtfY3NyZl90b2tlbm0AAAAYZGYyUjVZN2phSmRCQ2lVWDZvaWp6OG9xbQAAAAphdXRoX3N0YXRldAAAAAV3B3ZlcnNpb253A25pbHcKX19zdHJ1Y3RfX3cQRWxipeGlyLkF1dGhTdGF0ZXcFdG9rZW53A25pbHcQaXNfYXV0aGVudGljYXRlZHcFZmFsc2V3B3VzZXJfaWR3A25pbG0AAAAOY3BfYXR0cmlidXRpb250AAAAA20AAAALY3BfY2FtcGFpZ253A25pbG0AAAAJY3BfbWVkaXVtdwNuaWxtAAAACWNwX3NvdXJjZXcDbmlsbQAAAAxjdXJyZW50X3VzZXJ3A25pbG0AAAALdW5pcXVlX3VzZXJtAAAAEFZjN3A5ZjVDenlnWStQNi9tAAAAD3V0bV9hdHRyaWJ1dGlvbnQAAAACbQAAAAx1dG1fY2FtcGFpZ253A25pbG0AAAALdXRmX2NvbnRlbnR3A25pbA.1sedtPPdlEj9QascBe88DmfC7dZ81_-YUjqh6ULBNE4',
    'AWSALB': 'fXzNQCcMNMry3HnHQpbET95mFi1jRTm/Ksz8pL7Yrl0r3/W71ZGhbWn9IISqAtddrpi7thkMwd9hfNqLsOshzF2oSApSnALwegyENwsGXkaPtrsFXw5CmragWse1',
    'AWSALBCORS': 'fXzNQCcMNMry3HnHQpbET95mFi1jRTm/Ksz8pL7Yrl0r3/W71ZGhbWn9IISqAtddrpi7thkMwd9hfNqLsOshzF2oSApSnALwegyENwsGXkaPtrsFXw5CmragWse1',
}
'''
Cookies
Cookies là những dữ liệu nhỏ được máy chủ web gửi đến trình duyệt của người dùng, và sau đó trình duyệt sẽ gửi lại những cookies này tới máy chủ trong mỗi yêu cầu HTTP tiếp theo. Cookies thường được sử dụng để lưu trữ thông tin về phiên làm việc của người dùng, sở thích, và các hoạt động trước đó trên trang web. Trong scraping, cookies có thể cần thiết để duy trì trạng thái đăng nhập, tùy chọn ngôn ngữ, hoặc các tùy chọn khác đã được thiết lập trong các lần truy cập trước đó.
'''

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
}

'''

'''

file_path = r"D:\GitHub\Work-Experiences\Tuan Loc Commodities\2. Scrapping\2.1 My Own Scrapping Code\page_links.txt"
results = []

with open(file_path, 'r') as file:
    arr_urls = file.read().splitlines()

for original_url in arr_urls:
    print(original_url)
    response = requests.get(original_url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    parent_elements = soup.find_all(class_='group')  # Adjust class name to actual HTML structure
    
    for element in parent_elements:
        child_one = element.find(class_='waves-effect waves-light relative btn-flat btn- flex items-center justify-center mt-2 md:m-0')
        child_two = element.find(class_='text-xl leading-5 font-medium table:text-secondary table:text-base flex-1')

        href = child_one.get('href') if child_one and child_one.has_attr('href') else "No href"
        text = child_two.text.strip() if child_two else "No text"
        
        if child_one and href != "No href":
            results.append({'original_link': original_url, 'link_view_listing': href, 'name': text})

df_result = pd.DataFrame(results)
df_result.to_csv('result.csv', index=False)