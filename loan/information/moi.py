import asyncio
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1111107 filter out the ',' in 貸款額度-新北市
#查詢自購住宅補貼上限
def concessional_loan(url: str = 'https://www.gov.tw/News_Content.aspx?n=37&s=561179&sms=9100', table_num= 4):
  async def get_from_web(url):
    res = requests.get(url)
    return res

  async def to_soup(res):
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

  async def soup_to_dataframe(soup, table_num):
    table = soup.find_all('table')[table_num]
    res = pd.read_html(
      str(table), 
      encoding= 'utf-8',
      index_col=[0,1], 
      header= [0]
      )[0]
    return res

  async def fr(df):
   res =  {
  level_0: {level_1: {
      '利率': [float(match.group(1)) for match in re.finditer(pattern = r"目前為(\d+.*?)%", string = str(df.xs((level_0, level_1)).to_dict()))][0],
      '適用對象': [match.group(1) if match.group(1) != None else match.group(2) for match in re.finditer(pattern = r"(\d{1,2}\.\s\S*)(?:。)|(非屬.*)(?:，)", string = str(df.xs((level_0, level_1)).to_dict()))]
      
  }
   for level_1 in df.xs(level_0).index}
   if level_0 in ['優惠利率']
   else [
       [
        {match.group(1): int(match.group(2))}  
           for match in re.finditer(
               pattern= r"([^，]{3,4})最高為新臺幣(\d+)萬元", 
               string= level_1
               )
           ] + [{'不申請': '0'}]
         if level_0 == '貸款額度'
         else {
             '貸款年限': int(re.findall(pattern= r"^最長(.*?)年",string= level_1)[0]),
             '寬限期': int(re.findall(pattern= r"寬限期最長(.*?)年",string= level_1)[0])}
         for level_1 in df.xs(level_0).index
        ][0]
   for level_0 in df.index.levels[0]
   }
   return res

  async def task(url):
    res = await get_from_web(url)
    soup = await to_soup(res)
    df = await soup_to_dataframe(soup, table_num)
    table = await fr(df)
    return table

  res = asyncio.run(task(url))
  return res