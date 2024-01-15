import pandas as pd
import sys
sys.path.append('./')
from app.Loan.computation.helpers.scheduler import ensure_list_type, kwargs_detection
from app.Loan.computation.helpers.prepay import _time_, _amount_
from app.Loan.computation.methods import _EPP_arr_, _ETP_arr_
from app.Loan.computation.categories import amortization as amortization_methods
from dateutil.relativedelta import relativedelta
import datetime
from itertools import product
import asyncio
default_kwargs = {
    'interest_arr': {'interest': [1.94], 'time': []},
    'total_amount': 10_000_000,
    'down_payment_rate': 20,
    'tenure': 30,
    'grace_period': 0,
    'start_date': None,
    'method': [
        'EQUAL_TOTAL', 
        'EQUAL_PRINCIPAL'
    ],
    'prepay_arr': {
        'amount': [],
        'time': []
    },
    'subsidy_arr': {
        'interest_arr': {'interest': [0], 'time': []},
        'start': 0,
        'amount': 0,
        'tenure': 0,
        'grace_period': 0,
        'prepay_arr': {'amount': [], 'time': []},
            'method': [
                'EQUAL_TOTAL', 
                'EQUAL_PRINCIPAL'
            ]
    },
}

example_for_subsidy_arr= {
    'interest_arr': {'interest': [1, 1.33], 'time': [10]},
    'start': 2,
    'amount': 15_00_000,
    'tenure': 20,
    'grace_period': 0,
    'prepay_arr': {'amount': [], 'time': []},
    'method': ['EQUAL_TOTAL', 'EQUAL_PRINCIPAL'],
}

class df_schema:
    class level_0:
        ORIGINAL = '原始貸款'
        SUBSIDY = '房貸補貼'
        TOTAL = '總計'

    class level_1:
        ETP = '本息攤還法'  # Equal Total Payment
        EPP = '本金攤還法'  # Equal Principal Payment

    class level_2:
        PRINCIPAL = '攤還本金'  # Principal
        INTEREST = '應付利息'  # Interest
        PAYMENT = '償還總額'  # Payment
        RESIDUAL = '剩餘貸款'  # Residual


def calculator(
    interest_arr: dict,
    total_amount: int,
    tenure: int,
    down_payment_rate: int = 20,
    grace_period: int = 0,
    method: list[str] = [*amortization_methods.keys()], # ['EQUAL_TOTAL', 'EQUAL_PRINCIPAL']
    thousand_sep= True,
    start_date= None,
    result_type= 'dict', # 'dict' or 'df'
    **kwargs: dict
    ):
    """
    Arguments:
    1. interest_arr(dict): The arrangement of the amortization_methods interest which includes:  
      (1) interest(List): the interest rate(s) applied to specific period(s) of the loan.

      (2) time(List)(Optional): The timepoints at which the loan interest rates change.

    2. total_amount(int): The total amount of the loan.

    3. tenure(int): The loan period of the loan. 

    4. down_payment_rate(float): The down payment rate of the loan. The default value is 20.

    5. grace_period(int): The grace period of the loan. The default value is 0.

    6. method(list): The payment method applied to the ordinary loan installment. The default options include [Eqaul Total] and [Equal Principal] which stand for eqaul total payment and equal principal payment respectively.

    7. subsidy_arr(dict): The arrangement of the subsidy loan, which includes:

        (1) interest_arr(dict): The arrangement of the amortization_methods interest of subsidy loan which includes:  
            i. The interest rate(s) applied to specific period(s) of the loan.
            
            ii. time(List)(Optional): The timepoints at which the subsidy loan interest rates change. 

        (3) start(int): The timepoint at which the subsidy loan is applied.

        (4) grace_period(int): The grace period of the subsidy loan.

        (5) amount(int): The amount of the subsidy loan.

        (6) tenure(int): The tenure of the subsidy loan.

        (7) method(dict): The payment method applied to the subsidy loan installment. The default options include [Eqaul Total] and [Equal Principal] which stand for eqaul total payment and equal principal payment respectively.

        (8) prepay_arr(dict)(Optional): The arrangement of the prepayment of the subsidy loan, which includes:

            i. amount(List): Prepaid amount(s) applied to specific period(s) of the loan.

            ii. time(List)(Optional): The according period(s) of the prepayment.

    8. prepay_arr: The arrangement of the prepayment of the loan, which includes:

        (1) amount(List): Prepaid amount(s) applied to specific period(s) of the loan. 

        (2) time(List)(Optional): The according period(s) of the prepayment. 
            (Note that there is a slight difference in the time specification between prepayment and loan/subsidy loan. 
            The time for prepayment represents the collection of timepoints for the amounts being prepaid, while the time for loan/subsidy loan refers to the collection of timepoints at which the interest rates change.)
    """

    if grace_period > 5:
        raise ValueError('寬限期不可超過5年')

    # To identify whether the types of the passed keywords are fitted.
    kws_dict = {
        'subsidy_arr':
        {
            'interest_arr': {
                'interest': list, 
                'time': list
            },
            'start': int,
            'grace_period': int,
            'amount': int,
            'tenure': int,
            'method': list,
            'prepay_arr': dict
        },
        'prepay_arr':
        {
            'time': list,
            'amount': list,
        },
    }

    kwargs_detection(kws_spec=kws_dict, **kwargs)

    method_applied_to_subsidy_loan = kwargs.get(
        'subsidy_arr', {}).get('method', amortization_methods.keys())
    loan_amount = round(total_amount * (1 - (down_payment_rate / 100)))
    subsidy_time = kwargs.get('subsidy_arr', {}).get('start', 0)
    subsidy_amount = kwargs.get('subsidy_arr', {}).get('amount', 0)

    prepay_time = _time_#(
    prepay_time.subsidy_time= subsidy_time
    prepay_time.prepay_time= kwargs.get('prepay_arr', {}).get('time', [0])
        # subsidy_time=subsidy_time,
        # tenure=tenure,
        # prepay_arr={
            # 'time': kwargs.get('prepay_arr', {}).get('time', 0)}
    # )

    prepay_amount = _amount_(
        # tenure=tenure,
        subsidy_time=subsidy_time,
        subsidy_amount= subsidy_amount,  # type: ignore
        prepay_arr={
            'time': kwargs.get('prepay_arr', {}).get('time', 0),
            'amount': ensure_list_type(kwargs.get('prepay_arr', {}).get('amount', 0))
        }
    )
    def _df_(data,
             index_range=[0, tenure * 12 + 1],
             name=None,
             date= start_date,
             **kwargs,
             ):
        suffix = kwargs.get('suffix', "")
        suffix = ("_" + suffix if len(suffix) > 0 else suffix)
        dic= {
             'index': ([v for v in range(index_range[0], index_range[1])] if not date else [datetime.datetime.strptime(date, '%Y-%m-%d').date() + relativedelta(months=n) for n in range(index_range[0], index_range[1])]),
             'columns': [f'攤還本金{suffix}', f'應付利息{suffix}', f'償還總額{suffix}', f'剩餘貸款{suffix}'],
             'data': [*map(list, zip(*data))],
             'index_names': [None],
             'column_names': [None] + [None] * (len([name]) if name else 0),
         }
        if name:
            dic_columns= dic['columns'].copy()
            dic['columns'] = [col for col in product(name, dic_columns)]
        return dic

    method_applied = [v for v in method if v in amortization_methods.keys()]
    if method_applied:
        kwargs_for_loan = {
            'tenure': tenure,
            'loan_amount': loan_amount,
            'grace_period': grace_period,
            'interest_arr': interest_arr,
            'prepay_arr': {
                'time': prepay_time,
                'amount': prepay_amount,
            },
        }
        df= _df_(
            data= [_ETP_arr_(**kwargs_for_loan) if 'EQUAL_TOTAL' in method else ()][0] + [_EPP_arr_(**kwargs_for_loan) if 'EQUAL_PRINCIPAL' in method else ()][0],
            name= [amortization_methods[method_key] for method_key in method],
            index_range=[0, tenure * 12 + 1],
            date= start_date,
        )    
        # if subsidy_arr is specified
        if subsidy_amount > 0:
            DL = 24  # The deadline of applying for preferential loan
            if subsidy_time > DL:
                raise ValueError(f'超過申請購屋補貼期限(不可晚於購房後{DL/12}年)')
            subsidy_tenure = kwargs.get('subsidy_arr', {}).get(
                'tenure', 0)  # period of the subsidy loan
            subsidy_grace_period = kwargs.get(
                'subsidy_arr', {}).get('grace_period', 0)
            subsidy_subsidy_time = kwargs.get(
                'subsidy_arr', {}).get('subsidy', {}).get('time', 0)
            subsidy_subsidy_amount = kwargs.get(
                'subsidy_arr', {}).get('subsidy', {}).get('amount', 0)
            
            subsidy_prepay_time = _time_#(
            subsidy_prepay_time.subsidy_time= subsidy_subsidy_time
            subsidy_prepay_time.prepay_time= kwargs.get('subsidy_arr', {}).get('prepay_arr', {}).get('time', [0])
                # subsidy_time=subsidy_subsidy_time,
                # tenure=tenure,
                # prepay_arr={'time': kwargs.get('subsidy_arr', {}).get('prepay_arr', {}).get('time', 0)})

            subsidy_prepay_amount = _amount_(
                subsidy_time=subsidy_subsidy_time,
                # tenure=tenure,
                subsidy_amount=subsidy_subsidy_amount,  # type: ignore
                prepay_arr={
                    'amount': kwargs.get('subsidy_arr', {}).get('prepay_arr', {}).get('amount', 0),
                    'time': kwargs.get('subsidy_arr', {}).get('prepay_arr', {}).get('time', 0)}
            )
            subsidy_interest_arr = {
                'interest': kwargs.get('subsidy_arr', {}).get('interest_arr', {}).get('interest', [0]),
                'time': kwargs.get('subsidy_arr', {}).get('interest_arr', {}).get('time', [])
            }
            
            kwargs_for_subsidy = {
                "tenure": subsidy_tenure,
                "loan_amount": subsidy_amount,
                "interest_arr": subsidy_interest_arr,
                "grace_period": subsidy_grace_period,
                "prepay_arr": {
                    "time": subsidy_prepay_time,
                    "amount": subsidy_prepay_amount
                },
            }

            df_subsidy= _df_(
                data= [_ETP_arr_(**kwargs_for_subsidy) if 'EQUAL_TOTAL' in method_applied_to_subsidy_loan else ()][0] + [_EPP_arr_(**kwargs_for_subsidy) if 'EQUAL_PRINCIPAL' in method_applied_to_subsidy_loan else ()][0],
                name= [amortization_methods[method] for method in method_applied_to_subsidy_loan],
            )
            # Padding the data of subsidy loan to fit the length of the original loan.
            padding_from_the_begining = [[0] * len(df_subsidy['data'][0])] * (subsidy_time)
            padding_to_the_end = [[0] * len(df_subsidy['data'][0])] * (tenure * 12 - (subsidy_time + subsidy_tenure * 12))
            df_subsidy['data']= padding_from_the_begining + df_subsidy['data'] + padding_to_the_end

            # Add the level_0 header to df if subsidy_arr is given.
            df['columns']= [tuple([df_schema.level_0.ORIGINAL] + list(col)) for col in df['columns']]
            df_subsidy['columns']= [tuple([df_schema.level_0.SUBSIDY] + list(col)) for col in df_subsidy['columns']]

            # Concatenate the dictionaries
            df= {
                'index': [*df['index']],
                'columns': [*df['columns'], *df_subsidy['columns']],
                'data': [*map(lambda x, y: x+y, df['data'], df_subsidy['data'])],
                'index_names': [None],
                'column_names': [None] * len(df['columns'][0]),
            }

        # 加總原始貸款與補貼貸款並新增償還總額欄位
            # 將原始貸款選定的還款方式對應到房貸補貼對應的還款方式進行配對，以便篩出欄位加總
            idx = [
                [args, args_subsidy]
                for args in df['columns'] if args[0] == df_schema.level_0.ORIGINAL and args[2] == df_schema.level_2.PAYMENT
                for args_subsidy in df_subsidy['columns'] if args_subsidy[0] == df_schema.level_0.SUBSIDY and args_subsidy[2] == df_schema.level_2.PAYMENT
            ]
            
            # 欄位加總
            for id in idx:
                df['columns'].append((df_schema.level_0.TOTAL, id[0][1] + "(" + df_schema.level_0.ORIGINAL + ")", id[1][1] + "(" + df_schema.level_0.SUBSIDY + ")"))
                df['data']= [*map(lambda x: x + [sum([x[n] for (n, i) in enumerate(df['columns']) if (i in id)])], df['data'])]
 
            # 計算各期清償總和，並扣除重複計算的租金補貼貸款
            df['index'].append('Sum')
            df['data'].append([sum([*map(lambda x: x[i], df['data'])]) for i in range(len(df['data'][0]))])
            df['data'][-1]= [(data if n2 not in [n1 for (n1, (l0, l1, l2)) in enumerate(df['columns']) if l2 == df_schema.level_2.RESIDUAL] else df['data'][-2][n2]) for (n2, data) in enumerate(df['data'][-1])]
            df['data'][-1] = [data - df['data'][-2][n2] if n2 in [n1 for (n1, (l0, l1, l2)) in enumerate(df['columns']) if l2 == df_schema.level_2.RESIDUAL] else data for (n2, data) in enumerate(df['data'][-1])]
# 
        else:
            df['index'].append('Sum')
            # summation of each order of the list in data in dictionary named df above by list comprehension
            df['data'].append([sum([*map(lambda x: x[i], df['data'])]) for i in range(len(df['data'][0]))])
            df['data'][-1]= [(data if n2 not in [n1 for (n1, (l0, l1)) in enumerate(df['columns']) if l1 == '剩餘貸款'] else df['data'][-2][n2]) for (n2, data) in enumerate(df['data'][-1])]

        # Adjustment for the thousands digit. Note the output would be a string.
        if df['data'] and thousand_sep == True:
            df['data']= [[f"{round(x):,}" for x in data] for data in df['data']]
        if result_type == 'df':
            df = pd.DataFrame.from_dict(df, orient='tight')
    else: # when no method is specified
        df= {
             'index': ([v for v in range(0, 1)] if not start_date else [datetime.datetime.strptime(start_date, '%Y-%m-%d').date() + relativedelta(months=n) for n in range(0, 1)]),
             'columns': [('', '攤還本金'), ('', '應付利息'), ('', '償還總額'), ('', '剩餘貸款')],
             'data': [[0]* 4],
             'index_names': [None],
             'column_names': [None]*1,
         }
    return df


def async_calculator( # slower at most of the time.
    interest_arr: dict,
    total_amount: int,
    tenure: int,
    down_payment_rate: int = 20,
    grace_period: int = 0,
    method: list[str] = [*amortization_methods.keys()], # ['EQUAL_TOTAL', 'EQUAL_PRINCIPAL']
    thousand_sep= True,
    start_date= None,
    result_type= 'dict', # 'dict' or 'df'
    **kwargs: dict
    ):
    if grace_period > 5:
        raise ValueError('寬限期不可超過5年')

    # To identify whether the types of the passed keywords are fitted.
    kws_dict = {
        'subsidy_arr':
        {
            'interest_arr': {
                'interest': list, 
                'time': list
            },
            'start': int,
            'grace_period': int,
            'amount': int,
            'tenure': int,
            'method': list,
            'prepay_arr': dict
        },
        'prepay_arr':
        {
            'time': list,
            'amount': list,
        },
    }
    kwargs_detection(kws_spec=kws_dict, **kwargs)
    
    async def wrapper():
        method_applied_to_subsidy_loan = kwargs.get(
            'subsidy_arr', {}).get('method', amortization_methods.keys())
        loan_amount = round(total_amount * (1 - (down_payment_rate / 100)))
        subsidy_time = kwargs.get('subsidy_arr', {}).get('start', 0)
        subsidy_amount = kwargs.get('subsidy_arr', {}).get('amount', 0)
        prepay_time = _time_#(
        prepay_time.subsidy_time= subsidy_time
        prepay_time.prepay_time= ensure_list_type(kwargs.get('prepay_arr', {}).get('time', [0]))
            # subsidy_time=subsidy_time,
            # tenure=tenure,
            # prepay_arr={
                # 'time': kwargs.get('prepay_arr', {}).get('time', 0)}
        # )
        prepay_amount = _amount_(
            # tenure=tenure,
            subsidy_time=subsidy_time,
            subsidy_amount=subsidy_amount,  # type: ignore
            prepay_arr={
                'time': kwargs.get('prepay_arr', {}).get('time', 0),
                'amount': ensure_list_type(kwargs.get('prepay_arr', {}).get('amount', 0))
            }
        )
        async def _df_(
                data,
                index_range=[0, tenure * 12 + 1],
                name=None,
                date= start_date,
                **kwargs,
                ):
            suffix = kwargs.get('suffix', "")
            suffix = ("_" + suffix if len(suffix) > 0 else suffix)
            dic= {
                 'index': ([v for v in range(index_range[0], index_range[1])] if not date else [datetime.datetime.strptime(date, '%Y-%m-%d').date() + relativedelta(months=n) for n in range(index_range[0], index_range[1])]),
                 'columns': [f'攤還本金{suffix}', f'應付利息{suffix}', f'償還總額{suffix}', f'剩餘貸款{suffix}'],
                 'data': [*map(list, zip(*data))],
                 'index_names': [None],
                 'column_names': [None] + [None] * (len([name]) if name else 0),
            }
            if name:
                dic_columns= dic['columns'].copy()
                dic['columns'] = [col for col in product(name, dic_columns)]
            return dic
        
        
        method_applied= [v for v in method if v in amortization_methods.keys()]    
        
        kwargs_for_loan = {
                        'tenure': tenure,
                        'loan_amount': loan_amount,
                        'grace_period': grace_period,
                        'interest_arr': interest_arr,
                        'prepay_arr': {
                            'time': prepay_time,
                            'amount': prepay_amount,
                        },
                    }

        if method_applied and subsidy_amount == 0:
            task1 = asyncio.create_task(_df_(
                    data= [_ETP_arr_(**kwargs_for_loan) if 'EQUAL_TOTAL' in method else ()][0] + [_EPP_arr_(**kwargs_for_loan) if 'EQUAL_PRINCIPAL' in method else ()][0],
                    name= [amortization_methods[method_key] for method_key in method],
                    index_range=[0, tenure * 12 + 1],
                    date=start_date,
                    )
            )

            df= await task1

            df['index'].append('Sum')
            # summation of each order of the list in data in dictionary named df above by list comprehension
            df['data'].append([sum([*map(lambda x: x[i], df['data'])]) for i in range(len(df['data'][0]))])
            df['data'][-1]= [(data if n2 not in [n1 for (n1, (l0, l1)) in enumerate(df['columns']) if l1 == '剩餘貸款'] else df['data'][-2][n2]) for (n2, data) in enumerate(df['data'][-1])]
    
        elif method_applied and subsidy_amount > 0:
            # if subsidy_arr is specified
            DL = 24  # The deadline of applying for preferential loan
            if subsidy_time > DL:
                raise ValueError(f'超過申請購屋補貼期限(不可晚於購房後{DL/12}年)')
            subsidy_tenure = kwargs.get('subsidy_arr', {}).get(
                'tenure', 0)  # period of the subsidy loan
            subsidy_grace_period = kwargs.get(
                'subsidy_arr', {}).get('grace_period', 0)
            subsidy_subsidy_time = kwargs.get(
                'subsidy_arr', {}).get('subsidy', {}).get('time', 0)
            subsidy_subsidy_amount = kwargs.get(
                'subsidy_arr', {}).get('subsidy', {}).get('amount', 0)
            subsidy_prepay_time = _time_#(
            subsidy_prepay_time.subsidy_time= subsidy_subsidy_time
            subsidy_prepay_time.prepay_time= ensure_list_type(kwargs.get('subsidy_arr', {}).get('prepay_arr', {}).get('time', [0]))
                # subsidy_time=subsidy_subsidy_time,
                # tenure=tenure,
                # prepay_arr={'time': kwargs.get('subsidy_arr', {}).get('prepay_arr', {}).get('time', 0)})
            
            subsidy_prepay_amount = _amount_(
                subsidy_time=subsidy_subsidy_time,
                # tenure=tenure,
                subsidy_amount=subsidy_subsidy_amount,  # type: ignore
                prepay_arr={
                    'amount': kwargs.get('subsidy_arr', {}).get('prepay_arr', {}).get('amount', 0),
                    'time': kwargs.get('subsidy_arr', {}).get('prepay_arr', {}).get('time', 0)}
            )
            subsidy_interest_arr = {
                'interest': kwargs.get('subsidy_arr', {}).get('interest_arr', {}).get('interest', [0]),
                'time': kwargs.get('subsidy_arr', {}).get('interest_arr', {}).get('time', [])
            }
            method_applied_to_subsidy=[v for v in method_applied_to_subsidy_loan if v in amortization_methods.keys()],
            kwargs_for_subsidy = {
                "tenure": subsidy_tenure,
                "loan_amount": subsidy_amount,
                "interest_arr": subsidy_interest_arr,
                "grace_period": subsidy_grace_period,
                "prepay_arr": {
                    "time": subsidy_prepay_time,
                    "amount": subsidy_prepay_amount
                },
            }
            
            task1 = asyncio.create_task(_df_(
                data= [_ETP_arr_(**kwargs_for_loan) if 'EQUAL_TOTAL' in method else ()][0] + [_EPP_arr_(**kwargs_for_loan) if 'EQUAL_PRINCIPAL' in method else ()][0],
                name= [amortization_methods[method_key] for method_key in method],
                index_range=[0, tenure * 12 + 1],
                date=start_date,
                )
            )
            
            task2 = asyncio.create_task(_df_(
                    data=[_ETP_arr_(**kwargs_for_subsidy) if 'EQUAL_TOTAL' in method_applied_to_subsidy_loan else ()][0] + [_EPP_arr_(**kwargs_for_subsidy) if 'EQUAL_PRINCIPAL' in method_applied_to_subsidy_loan else ()][0],
                    name=[amortization_methods[method] for method in method_applied_to_subsidy_loan],
                )
            )
            
            df= await task1
            df_subsidy= await task2

            # Padding the data of subsidy loan to fit the length of the original loan.
            padding_from_the_begining = [[0] * len(df_subsidy['data'][0])] * (subsidy_time)
            padding_to_the_end = [[0] * len(df_subsidy['data'][0])] * (
                        tenure * 12 - (subsidy_time + subsidy_tenure * 12))
            df_subsidy['data'] = padding_from_the_begining + df_subsidy['data'] + padding_to_the_end
            
            # Add the level_0 header to df if subsidy_arr is given.
            df['columns'] = [tuple([df_schema.level_0.ORIGINAL] + list(col)) for col in df['columns']]
            df_subsidy['columns'] = [tuple([df_schema.level_0.SUBSIDY] + list(col)) for col in df_subsidy['columns']]
            # Concatenate the dictionaries
            
            df= {
                'index': [*df['index']],
                'columns': [*df['columns'], *df_subsidy['columns']],
                'data': [*map(lambda x, y: x+y, df['data'], df_subsidy['data'])],
                'index_names': [None],
                'column_names': [None] * len(df['columns'][0]),
            }
            
            idx = [
                [args, args_subsidy]
                for args in df['columns'] if args[0] == df_schema.level_0.ORIGINAL and args[2] == df_schema.level_2.PAYMENT
                for args_subsidy in df_subsidy['columns'] if args_subsidy[0] == df_schema.level_0.SUBSIDY and args_subsidy[2] == df_schema.level_2.PAYMENT
            ]

            for id in idx:
                df['columns'].append((df_schema.level_0.TOTAL, id[0][1] + "(" + df_schema.level_0.ORIGINAL + ")", id[1][1] + "(" + df_schema.level_0.SUBSIDY + ")"))
                df['data']= [*map(lambda x: x + [sum([x[n] for (n, i) in enumerate(df['columns']) if (i in id)])], df['data'])] 
            
            # 計算各期清償總和，並扣除重複計算的租金補貼貸款
            df['index'].append('Sum')
            df['data'].append([sum([*map(lambda x: x[i], df['data'])]) for i in range(len(df['data'][0]))])
            df['data'][-1]= [(data if n2 not in [n1 for (n1, (l0, l1, l2)) in enumerate(df['columns']) if l2 == df_schema.level_2.RESIDUAL] else df['data'][-2][n2]) for (n2, data) in enumerate(df['data'][-1])]
            df['data'][-1] = [data - df['data'][-2][n2] if n2 in [n1 for (n1, (l0, l1, l2)) in enumerate(df['columns']) if l2 == df_schema.level_2.RESIDUAL] else data for (n2, data) in enumerate(df['data'][-1])]
        

        # Adjustment for the thousands digit. Note the output would be a string.   
        else:
            df= {
                 'index': ([v for v in range(0, 1)] if not start_date else [datetime.datetime.strptime(start_date, '%Y-%m-%d').date() + relativedelta(months=n) for n in range(0, 1)]),
                 'columns': ['攤還本金', '應付利息', '償還總額', '剩餘貸款'],
                 'data': [[0]* 4],
                 'index_names': [None],
                 'column_names': [None]*1,
             }
        if df['data'] and thousand_sep == True:
            df['data']= [[f"{round(x):,}" for x in data] for data in df['data']]
        if result_type == 'df':
            df = pd.DataFrame.from_dict(df, orient='tight')
        return df
    
    res = asyncio.run(wrapper())

    return res


# python app/Loan/main.py
# py -m app.Loan.main
if __name__ == "__main__":
    import time
    # default_kwargs['subsidy_arr']= example_for_subsidy_arr
    # default_kwargs['method'] = []
    # default_kwargs['start_date']= '2021-01-01'
    # default_kwargs['result_type']= 'df'
    t0 = time.time()
    result = calculator(**default_kwargs, thousand_sep= False)
    print(
        result
    )
    sync_operating_time= time.time()-t0

    t_0_async= time.time()
    result_async = async_calculator(**default_kwargs)
    print(
        result_async
    )
    print('TIME COMPARISON: ', 
          '\n', 'Sync:', sync_operating_time, 
          '\n', 'Async:', time.time()-t_0_async
          )