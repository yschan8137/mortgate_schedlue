import requests
from bs4 import BeautifulSoup

url = 'https://www.example.com/mortgage'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有房貸方案的區塊
plans = soup.find_all('div', class_='mortgage-plan')

# 逐一解析每個方案的資訊
for plan in plans:
    name = plan.find('h2', class_='plan-name').text
    interest_rate = plan.find('div', class_='interest-rate').text
    loan_amount = plan.find('div', class_='loan-amount').text
    # ... 其他資訊的解析 ...

    # 儲存資訊到檔案或資料庫中
    # ...
