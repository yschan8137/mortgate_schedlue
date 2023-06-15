import numpy as np
import pandas as pd

from .computation.helpers.scheduler import ensure_list_type, kwargs_detection, scheduler
from .computation.helpers.prepay import _time_, _amount_
from .computation.methods import _EPP_arr_, _ETP_arr_
from .computation.categoties import amortization as amortization_methods


class df_schema:
    class level_0:
        ORIGINAL = '原始貸款'
        SUBSIDY = '房貸補貼'
        TOTAL = '償還總額'

    class level_1:
        ETP = '本息攤還法' #Equal Total Payment
        EPP = '本金攤還法' #Equal Principal Payment

    class level_2:
        PRINCIPAL = '攤還本金' #Principal
        INTEREST = '利息'   #Interest
        PAYMENT = '每期貸款'    #Payment
        RESIDUAL = '剩餘貸款'   #Residual


def calculator(
    interest_arr: dict,
    total_amount: int,
    tenure: int,
    down_payment_rate: int = 20,
    grace_period: int = 0,
    method: list[str] = [*amortization_methods.keys()], # ['EQUAL_TOTAL', 'EQUAL_PRINCIPAL']
    **kwargs: dict
) -> pd.DataFrame:
    """
    Arguments:
    1. interest_arr(dict): The arrangement of the amortization_methods interest which includes:  
      (1) interest(List): the interest rate(s) applied to specific period(s) of the loan.

      (2) multi_arr(List)(Optional): The timepoints at which the loan interest rates change.

    2. total_amount(int): The total amount of the loan.

    3. tenure(int): The loan period of the loan. 

    4. down_payment_rate(float): The down payment rate of the loan. The default value is 20.

    5. grace_period(int): The grace period of the loan. The default value is 0.

    6. method(list): The payment method applied to the ordinary loan installment. The default options include [Eqaul Total] and [Equal Principal] which stand for eqaul total payment and equal principal payment respectively.

    7. subsidy_arr(dict): The arrangement of the subsidy loan, which includes:

        (1) interest(List): The interest rate(s) applied to specific period(s) of the loan.

        (2) multi_arr(List)(Optional): The timepoints at which the subsidy loan interest rates change. 

        (3) time(int): The timepoint at which the subsidy loan is applied.

        (4) grace_period(int): The grace period of the subsidy loan.

        (5) amount(int): The amount of the subsidy loan.

        (6) tenure(int): The tenure of the subsidy loan.

        (7) method(dict): The payment method applied to the subsidy loan installment. The default options include [Eqaul Total] and [Equal Principal] which stand for eqaul total payment and equal principal payment respectively.
    
        (8) prepay_arr(dict)(Optional): The arrangement of the prepayment of the subsidy loan, which includes:
    
            i. amount(List): Prepaid amount(s) applied to specific period(s) of the loan.
            
            ii. multi_arr(List)(Optional): The according period(s) of the prepayment.
    
    8. prepay_arr: The arrangement of the prepayment of the loan, which includes:

        (1) amount(List): Prepaid amount(s) applied to specific period(s) of the loan. 

        (2) multi_arr(List)(Optional): The according period(s) of the prepayment. 
            (Note that there is a slight difference in the multi_arr specification between prepayment and loan/subsidy loan. 
            The multi_arr for prepayment represents the collection of timepoints for the amounts being prepaid, while the multi_arr for loan/subsidy loan refers to the collection of timepoints at which the interest rates change.)
    """

    if grace_period > 5:
        raise ValueError('寬限期不可超過5年')

    # To identify whether the types of the passed keywords are fitted.
    kws_dict = {
        'subsidy_arr':
        {
            'interest': list,
            'multi_arr': list,
            'time': int,
            'grace_period': int,
            'amount': int,
            'tenure': int,
            'method': list,
            'prepay_arr': dict
        },
        'prepay_arr':
        {
            'multi_arr': list,
            'amount': list,
        },
    }

    kwargs_detection(kws_spec=kws_dict, **kwargs)

    method_applied_to_subsidy_loan = kwargs.get(
        'subsidy_arr', {}).get('method', amortization_methods.keys())
    loan_amount = round(total_amount * (1 - (down_payment_rate / 100)))
    subsidy_time = kwargs.get('subsidy_arr', {}).get('time', 0)
    subsidy_amount = kwargs.get('subsidy_arr', {}).get('amount', 0)

    prepay_time = _time_(
        subsidy_time=subsidy_time,
        tenure= tenure,
        prepay_arr={
            'multi_arr': kwargs.get('prepay_arr', {}).get('multi_arr', 0)}
    )

    prepay_amount = _amount_(
        prepay_time=prepay_time,
        tenure=tenure,
        subsidy_time=subsidy_time,
        subsidy_amount=subsidy_amount,  # type: ignore
        prepay_arr={
            'multi_arr': kwargs.get('prepay_arr', {}).get('multi_arr', 0),
            'amount': ensure_list_type(kwargs.get('prepay_arr', {}).get('amount', 0))
        }
    )

    def _df_(objs,
             name=None,
             index_range=[0, tenure * 12 + 1],
             **kwargs):
        suffix = kwargs.get('suffix', "")
        suffix = ("_" + suffix if len(suffix) > 0 else suffix)
        df = pd.DataFrame(
            {
                f'攤還本金{suffix}': objs[0],
                f'利息{suffix}': objs[1],
                f'每期貸款{suffix}': objs[2],
                f'剩餘貸款{suffix}': objs[3]
            },
            index=[v for v in range(index_range[0], index_range[1])]
        )
        if name:
            df.columns = pd.MultiIndex.from_product([[name], df.columns])
        return df

    method_applied = [v for v in method if v in amortization_methods.keys()]
    # Collection of the dataframes of applied amortization_methods method.
    dfs_ordinry = {}
    if 'EQUAL_TOTAL' in method_applied:
        res_etp = _ETP_arr_(
            tenure= tenure,
            loan_amount=loan_amount,
            grace_period=grace_period,
            interest_arr=interest_arr,
            prepay_time=prepay_time,
            prepay_amount=prepay_amount,
        )
        df_etp = _df_(res_etp)
        dfs_ordinry[amortization_methods['EQUAL_TOTAL']] = df_etp
    if 'EQUAL_PRINCIPAL' in method_applied:
        res_epp = _EPP_arr_(
            tenure=tenure,
            loan_amount=loan_amount,
            grace_period=grace_period,
            interest_arr=interest_arr,
            prepay_time=prepay_time,
            prepay_amount=prepay_amount,
        )
        df_epp = _df_(res_epp)
        dfs_ordinry[amortization_methods['EQUAL_PRINCIPAL']] = df_epp

    if dfs_ordinry != {}:
        # raise ValueError('The method(s) of amortization are not specified.')
        df = pd.concat(
            objs=[*dfs_ordinry.values()],
            keys=[*dfs_ordinry.keys()],
            axis=1
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
            subsidy_prepay_time = _time_(
                subsidy_time=subsidy_subsidy_time,
                tenure=tenure,
                prepay_arr={'multi_arr': kwargs.get('subsidy_arr', {}).get('prepay_arr', {}).get('time', 0)})
            subsidy_prepay_amount = _amount_(
                prepay_time=subsidy_prepay_time,
                subsidy_time=subsidy_subsidy_time,
                tenure=tenure,
                subsidy_amount=subsidy_subsidy_amount,  # type: ignore
                prepay_arr={
                    'amount': kwargs.get('subsidy_arr', {}).get('prepay_arr', {}).get('amount', 0),
                    'multi_arr': kwargs.get('subsidy_arr', {}).get('prepay_arr', {}).get('time', 0)}
            )
            subsidy_interest_arr = {
                'interest': kwargs.get('subsidy_arr', {}).get('interest', 0),
                'multi_arr': kwargs.get('subsidy_arr', {}).get('multi_arr', [])
            }
            method_applied_to_subsidy = [v for v in method_applied_to_subsidy_loan if v in amortization_methods.keys()]
            kwargs_subsidy = {
                "tenure": subsidy_tenure,
                "loan_amount": subsidy_amount,
                "interest_arr": subsidy_interest_arr,
                "prepay_time": subsidy_prepay_time,
                "prepay_amount": subsidy_prepay_amount,
                "grace_period": subsidy_grace_period,
            }

            dfs_subsidy = {}
            if 'EQUAL_TOTAL' in method_applied_to_subsidy:
                res_ETP_subsidy = _ETP_arr_(**kwargs_subsidy)
                df_etp_subsidy = _df_(res_ETP_subsidy, index_range=[subsidy_time, subsidy_time + subsidy_tenure * 12 + 1])
                dfs_subsidy[amortization_methods['EQUAL_TOTAL']] = df_etp_subsidy
            if 'EQUAL_PRINCIPAL' in method_applied_to_subsidy:
                res_EPP_subsidy = _EPP_arr_(**kwargs_subsidy)
                df_epp_subsidy = _df_(res_EPP_subsidy, index_range=[subsidy_time, subsidy_time + subsidy_tenure * 12 + 1])
                dfs_subsidy[amortization_methods['EQUAL_PRINCIPAL']] = df_epp_subsidy

            multi_index_subsidy = pd.MultiIndex.from_product(
                iterables=[[df_schema.level_0.SUBSIDY], amortization_methods.values()])
            
            # if dfs_subsidy != {}:
            df_subsidy = pd.concat(
                objs=[*dfs_subsidy.values()],
                keys=multi_index_subsidy, # type: ignore
                axis=1
            )

            # Add the level_0 header if subsidy_arr is given.
            df.columns = pd.MultiIndex.from_tuples(
                [('原始貸款', k, v) for (k, v) in df.columns]
            )

                # dataframe of the orinary loan df if the subsidy_arr is specified.
            df = pd.concat(
                objs=[df, df_subsidy],
                axis=1
                ).fillna(0)

        # 加總原始貸款與補貼貸款並新增償還總額欄位
            # 將原始貸款選定的還款方式對應到房貸補貼對應的還款方式進行配對，以便篩出欄位加總
            idx = [
                [args, args_subsidy]
                for args in df.columns if args[0] == df_schema.level_0.ORIGINAL and args[2] == df_schema.level_2.PAYMENT
                for args_subsidy in df.columns if args_subsidy[0] == df_schema.level_0.SUBSIDY and args_subsidy[2] == df_schema.level_2.PAYMENT
            ]

            # 欄位加總
            for id in idx:
                df.loc[:, (df_schema.level_0.TOTAL, id[0][1] + "(" + df_schema.level_0.ORIGINAL + ")", id[1][1] + "(" +
                           df_schema.level_0.SUBSIDY + ")")] = df.loc[:, id].apply(lambda x: round(x)).sum(axis=1, numeric_only=True) # type: ignore

            # 計算各期清償總和
            df.loc['Sum'] = df[1:].sum().groupby(axis=0, level=[0, 1, 2]  # type: ignore
                                                 ).transform('sum')
            df.loc['Sum', [(l0, l1, l2) for (l0, l1, l2) in df.columns if l2 == '剩餘貸款']] = df.loc[len(
                df) - 2, [(l0, l1, l2) for (l0, l1, l2) in df.columns if l2 == '剩餘貸款']].apply(lambda x: round(x))
            
            # 租金補貼貸款會重覆計算，須扣除
            df.loc['Sum', [(l0, l1, l2) for (l0, l1, l2) in df.columns if l0 == df_schema.level_0.TOTAL]] -= subsidy_amount
        
        else:
            df.loc['Sum'] = df[1:].sum().groupby(
                axis=0, level=[0, 1]).transform('sum')  # type: ignore
            df.loc['Sum', [(l0, l1) for (l0, l1) in df.columns if l1 == '剩餘貸款']] = df.loc[len(
                df) - 2, [(l0, l1) for (l0, l1) in df.columns if l1 == '剩餘貸款']]

        # Adjustment for the thousands digit.
        df = df.applymap(lambda x: f"{round(x):,}")
    else:
        dfs_ordinry['None'] = _df_([0]*4, index_range=[0, 1])
        df = pd.concat(
            objs=[*dfs_ordinry.values()],
            keys=[*dfs_ordinry.keys()],
            axis=1
        )   
    return df


# py -m Amort.loan.main
if __name__ == "__main__":
    print(
        calculator(
            interest_arr={'interest': [1.38], 'multi_arr': []},
            total_amount=10_000_000,
            down_payment_rate= 20,
            tenure=40,
            grace_period=0,
            prepay_arr={
                'multi_arr': [120, 160],
                'amount': [2_000_000, 200_0000]
            },
            subsidy_arr={
                'interest': [1.01],
                'multi_arr': [],
                'time': 24,
                'amount': 2_300_000,
                'tenure': 20,
                'grace_period': 0,
                'prepay_arr': {'amount': [], 'multi_arr': []},
                'method': [
                    'EQUAL_TOTAL', 
                    'EQUAL_PRINCIPAL'
                ]
            },
            method=[
                'EQUAL_TOTAL', 
                'EQUAL_PRINCIPAL'
                ]
        )
    )