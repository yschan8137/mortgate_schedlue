import pandas as pd
import requests


#查詢貸款利率
def query(
    loan_period: int,
    total_amount: int, 
    first_purchase: bool = 1, 
    down_payment_rate: float = 0.2,
    ):
    rs = requests.session()
    src = f'https://mortgage.591.com.tw/search/?first_purchase={first_purchase}&price={total_amount}&purchase={int(down_payment_rate * total_amount)}&mortgage_ratio={int(down_payment_rate * 100)}&mortgage_time={loan_period}&target_user=0&bank_id=&order_field=&firstRow=0'
    rs.headers.update(
      {
       "Content-Type": "application/json",
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
       }
       )
    res = rs.get(url = src)
    df = pd.concat(
        [
            pd.DataFrame(
                {**{k: v for (k, v) in dfs.items() if k != 'apr_remark'}, 
                **{v.split('：')[0]: v.split('：')[1] for v in dfs['apr_remark'].split('\n') 
                if v != '總費用年百分率試算範例'}}, index= [i+1]) 
                for (i, dfs) in enumerate(res.json()['data']['data'])
                ],
                )
    return df