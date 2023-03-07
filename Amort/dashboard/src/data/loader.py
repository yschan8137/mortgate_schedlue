import pandas as pd

from typing import Callable

from ....loan import _591_, moi
from ....loan.computation.categoties import amortization

# 1111107 Entering Python Shell by typing 'python'
# leave python shell by typing ctrl + z or '^Z'

# reloan module in python shell: from importlib import reload, then type relaod([modeule])

# 1111109 Ipython kernel: Entering ipytohn in terminal
# enabling auto reload in ipython: Entering '%load_ext autoreload' and  '%autorelaod 2'.
Preprocessor= Callable[[pd.DataFrame], pd.DataFrame]

class DataSchema:
    BANK= 'bank_name'
    TITLE= 'title'
    INTEREST= {'MIN':'seg_min', 'TYPE': 'interest_type'}
    DURATION= 'mortgage_time'
    PAYMENT= 'perpay'
    TYPE= 'type'


def _moi_data():
    return moi.concessional_loan()

def _591_data(
    loan_period, 
    total_amount, 
    first_purchase= 1, 
    down_payment_rate= 0.2
    ):
    df = _591_.query(
        loan_period, 
        total_amount, 
        first_purchase, 
        down_payment_rate)
    filtered_df = df[df.columns[2:10]]
    return filtered_df
