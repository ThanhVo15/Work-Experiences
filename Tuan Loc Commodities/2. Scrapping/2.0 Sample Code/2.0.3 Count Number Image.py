# Code mẫu đếm số lượng hình ảnh có trong 1 trang web của bên thứ 3


import requests
from bs4 import BeautifulSoup

def count_images(response):
    # Tạo đối tượng BeautifulSoup để phân tích cú pháp HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    content = soup.select_one("#content > div:nth-of-type(2) > div > div:nth-of-type(1) > div:nth-of-type(2)")
    
    # Nếu phần tử tồn tại, tìm tất cả các thẻ <img> trong nó
    if content:
        images = content.find_all('img')
        return len(images)
    else:
        return 0

import requests

cookies = {
    '_dealer_marketing_session': 'K0wrQS9TUXhXbXVIYkNFYWZIWTZHSEJjTWFGNHZtbWpmdy8xUkJRa013YWkvMmtwNXVPT2xscjlrdVpHZW5PWWJPTFZRRUV3bXdqTitiMzBFY3NYK0tNaXhQdFJJV1paaEpwcWlKN3hmMzNHbWlnUVFxeFIxcVRyVUVEajYwT0s1Rk12eGxFNmNZSEdjYXRGVVJhQ21Zd3RUejBuQmdWaVZORlVucXVvNDVqQTg4UXEyZCswNm4wT2hhYmNoeFU2LS1XcTh1Q2VGS1ZoVGhRbmk4N3lBS2JnPT0%3D--5cc8cbe2d4715adccfee3c7dc09404e3b9ab6cf5',
    'OptanonAlertBoxClosed': '2024-04-25T08:59:49.585Z',
    'OptanonConsent': 'isIABGlobal=false&datestamp=Thu+Apr+25+2024+15%3A59%3A49+GMT%2B0700+(Indochina+Time)&version=6.10.0&hosts=&consentId=dbb5cc2e-60e9-4e39-aa4a-d863c93d35d8&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0001%3A1',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': '_dealer_marketing_session=K0wrQS9TUXhXbXVIYkNFYWZIWTZHSEJjTWFGNHZtbWpmdy8xUkJRa013YWkvMmtwNXVPT2xscjlrdVpHZW5PWWJPTFZRRUV3bXdqTitiMzBFY3NYK0tNaXhQdFJJV1paaEpwcWlKN3hmMzNHbWlnUVFxeFIxcVRyVUVEajYwT0s1Rk12eGxFNmNZSEdjYXRGVVJhQ21Zd3RUejBuQmdWaVZORlVucXVvNDVqQTg4UXEyZCswNm4wT2hhYmNoeFU2LS1XcTh1Q2VGS1ZoVGhRbmk4N3lBS2JnPT0%3D--5cc8cbe2d4715adccfee3c7dc09404e3b9ab6cf5; OptanonAlertBoxClosed=2024-04-25T08:59:49.585Z; OptanonConsent=isIABGlobal=false&datestamp=Thu+Apr+25+2024+15%3A59%3A49+GMT%2B0700+(Indochina+Time)&version=6.10.0&hosts=&consentId=dbb5cc2e-60e9-4e39-aa4a-d863c93d35d8&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0001%3A1',
    'DNT': '1',
    'If-None-Match': 'W/"74931eb518da4a7e6509c6b4f0c9d510"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get(
    'https://www.gaaclassiccars.com/vehicles/39961/2015-ferrari-458-italia',
    cookies=cookies,
    headers=headers,
)
print("Số hình ảnh trên trang:", count_images(response))
