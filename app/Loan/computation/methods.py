import numpy as np
from app.Loan.computation.helpers.adjustments import ETR, Offsets
from app.Loan.computation.helpers.scheduler import ensure_list_type
from app.Loan.computation.helpers.prepay import _time_
import itertools

class _scheduler_:
    time_arr: list
    interest_arr: list
    end: int
    def __new__(cls, value):
        cls.res_items= {k: (v/100)/12 for (k, v) in zip([0, 1] + cls.time_arr, [0] + cls.interest_arr)}
        cls.__index__= max(k if k <= value else 0 for k in [0, 1] + cls.time_arr)
        cls.__end__ = min(k if k > value else cls.end for k  in [0, 1] + cls.time_arr)
        return cls.res_items[cls.__index__]
    
    @classmethod
    def interval_grouping(cls):
        return [[cls(k), [cls.__index__, cls.__end__]] for k in [0, 1] + cls.time_arr]

# 本金平均攤還法(Equal Principal Payment)
def _EPP_arr_(
    tenure: int,
    loan_amount: int,
    interest_arr: dict,
    grace_period: int = 0,
    **kwargs
) -> tuple[list, list, list, list]:
    # if isinstance(prepay_time := kwargs.get('prepay_arr', {}).get('time', []), int):
        # raise TypeError('The data type of the time in prepay_arr must be a list, which coveted from the _time_ function in the prepay module')
    if isinstance(prepay_amount := kwargs.get('prepay_arr', {}).get('amount', []), int):
        raise TypeError('The data type of the amount in prepay_arr must be a list, which coveted from the _amount_ function in the prepay module')
    _payments_ = []
    _residual_ = []
    _interest_ = []
    _total_ = []
    # 
    # _interest_arr_ = _scheduler_(
    #     tenure=tenure,
    #     interest_arr={
    #         'interest': ensure_list_type(interest_arr.get('interest', 0)),
    #         'time': ensure_list_type(interest_arr.get('time', []))
    #     }
    # )

    _interest_arr_= _scheduler_
    _interest_arr_.time_arr= ensure_list_type(interest_arr.get('time', []))
    _interest_arr_.interest_arr= ensure_list_type(interest_arr.get('interest', [0]))
    _interest_arr_.end= tenure * 12 + 1
    prepay_t= kwargs.get('prepay_arr', {}).get('time', [])

    def payments(
            t,
            amount= loan_amount,
            grace_period= grace_period,
            tenure= tenure,
            prepay_time= prepay_t,
        ):
        return (
            (
                amount
            )
            /
            (
                (
                    (tenure - grace_period) * 12
                ) \
                    + Offsets(
                        grace_period=grace_period,
                        prepay_time= prepay_t(t-1)
                    )
            )
            if t > grace_period * 12 else 0
        )
    
    # for t in range(len(_interest_arr_)):
    for t in range(_interest_arr_.end):
        if t > 0:
            # if prepay_amount[t] < _residual_[-1]:
            if prepay_amount.get(t, 0) < _residual_[-1]:
                # _payments_.append(prepay_amount[t] + payments(
                _payments_.append(prepay_amount.get(t, 0) + payments(
                                                        t= t,
                                                        # amount= _residual_[prepay_time[t-1]]
                                                        amount= _residual_[prepay_t(t-1)]
                                                     )
                )
            else:
                _payments_.append(
                    _residual_[t-1]
                )
            # _interest_.append(_residual_[-1] * _interest_arr_[t])
            _interest_.append(_residual_[t-1] * _interest_arr_(t))
            _residual_.append(loan_amount - sum(_payments_))
        else:
            _payments_.append(0)
            _interest_.append(0)
            _residual_.append(loan_amount)
        _total_.append(_payments_[-1] + _interest_[-1])

    return _payments_, _interest_, _total_, _residual_


# 本息平均攤還法(Equal Total Payment)
def _ETP_arr_(
    tenure,
    loan_amount: int,
    interest_arr: dict,
    grace_period: int= 0,
    **kwargs
    ) -> tuple[list, list, list, list]:
    # default value  
    _principal_payment_ = []
    _residual_ = []
    _interest_ = []
    _accum_ = [] # while the multi-stages interest rate is applied, the accumulated repament is recorded in order to calculate the present value of the residual.
    _total_ = []

    # The arrangement of interest rate applied to each period.
    # __interest_arr_= scheduler(
    #                     tenure=tenure,
    #                     interest_arr={
    #                         'interest': ensure_list_type(interest_arr.get('interest', 0)),
    #                         'time': ensure_list_type(interest_arr.get('time', []))
    #                     }
    #                 )
    
    # the dynamic arrangement of principal ratio of whole tenure.
    _interest_arr_= _scheduler_
    _interest_arr_.time_arr= ensure_list_type(interest_arr.get('time', []))
    _interest_arr_.interest_arr= ensure_list_type(interest_arr.get('interest', [0]))
    _interest_arr_.end= tenure * 12 + 1

    def principal_ratio_at_(
            timing,
            interest_arr,
            length,
            grace_period= grace_period,
            prepay_time= 0,
            ):
        return ETR(
                    t= timing,
                    interest_arr= interest_arr,
                    length= length,
                    grace_period= grace_period,
                    prepay={'time': prepay_time},
               ) * (1 + interest_arr[timing])**(-(1 + (length - 1) - timing))

    def applied_interval(arr):
        interest= []
        t= [0]
        processed_t = []
        for (v, q) in itertools.groupby(arr):
            interest.append(v)
            t.append(len([*q]))
        def accumulative_summation(list):
          """
          Calculates the accumulative summation of a list.

          Args:
            list: A list of numbers.

          Returns:
            A list of numbers, where each number is the sum of the previous numbers in the list.
          """
          cumsum = []
          for i in range(len(list)):
            if i == 0:
              cumsum.append(list[i])
            else:
              cumsum.append(cumsum[i - 1] + list[i])
          return cumsum

        def group_by_consecutive_elements(list):
         """
         Groups the results of each consecutive elements in a list.

         Args:
           list: A list of numbers.

         Returns:
           A list of lists, where each inner list contains the consecutive elements of the original list.
         """
         groups = []
         for (i, t) in zip(interest, range(len(list) - 1)):
           groups.append((i, [list[t], list[t + 1]]))
         return groups
        return group_by_consecutive_elements(accumulative_summation(t))
    
    # for (n, (interest, interval)) in enumerate(applied_interval(__interest_arr_)):
    for (n, (interest, interval)) in enumerate(_interest_arr_.interval_grouping()):
        if n > 0:
            d = (interval[1] - interval[0] + 1) # Note that the end of the interval, namely interval[1], is not included in the calculation of the number of periods.
            _accum_.append(sum(_principal_payment_[:-1])) # To address the situation that the interest rate is changed in the middle of the tenure, the accumulated repayment is recorded in order to calculate the present value of the residual. 
            # int_arr = [interest] * (len(_interest_arr_) - (interval[0] - 1))
            int_arr = [interest] * (tenure * 12 + 1 - (interval[0] - 1))
            grace_t= (round(((grace_period * 12) - interval[0] + 1)/12) if (grace_period * 12) - interval[0] > 0 else 0)

            # if isinstance(prepay_time := kwargs.get('prepay_arr', {}).get('time', 0), int):
                # raise TypeError('The data type of the time in prepay_arr must be a list, which coveted from the _time_ function in the prepay module')
            if isinstance(prepay_amount := kwargs.get('prepay_arr', {}).get('amount', 0), int):
                raise TypeError('The data type of the amount in prepay_arr must be a list, which coveted from the _amount_ function in the prepay module')
            
            # prepay_t = prepay_time[interval[0] - 1:]
            # prepay_a = prepay_amount[interval[0] - 1:]
            prepay_t = kwargs.get('prepay_arr', {}).get('time', [0])
            prepay_a = prepay_amount
            
            for t in range(interval[0], interval[1]):
                t = t - (interval[0] - 1)
                # if (prepay_t[t] == 0):
                if (prepay_t(t) == 0):
                    principal_payment= (loan_amount - (_accum_[n])) * principal_ratio_at_(
                                                                            timing= t,
                                                                            interest_arr= int_arr,
                                                                            # length= len(_interest_arr_) - (interval[0] - 1),
                                                                            length= _interest_arr_.end - (interval[0] - 1),
                                                                            grace_period= grace_t,
                                                                            # prepay_time= prepay_t[t],
                                                                            prepay_time= prepay_t(t),
                                                                      )
                    # ensure the _residual_ to be positive
                    if (_residual_[-1] - principal_payment) >= 0:
                        _principal_payment_.append(principal_payment)
                    else:
                        _principal_payment_.append(_residual_[-1])
                else:
                    # if (t == prepay_t[t] - (interval[0] - 1) and prepay_a[t] > 0): # Note that the prepay_t[t] also needed to be subtracted by (interval[0] - 1).
                    # if (t == prepay_t[t] - (interval[0] - 1) and prepay_a.get(t, 0) > 0):
                    if (t == prepay_t(t) - (interval[0] - 1) and prepay_a.get(t, 0) > 0):
                        # 提前支付金額低於前一期餘額
                        if prepay_a[t] < _residual_[-1]:
                        # if prepay_a.get(t, 0) < _residual_[-1]:
                            # _principal_payment_.append(prepay_a[t] + (_residual_[prepay_t[t-1]] - (_accum_[n])) * principal_ratio_at_(
                            # _principal_payment_.append(prepay_a.get(t, 0) + (_residual_[prepay_t[t-1]] - (_accum_[n])) * principal_ratio_at_(
                            _principal_payment_.append(prepay_a.get(t, 0) + (_residual_[prepay_t(t-1)] - (_accum_[n])) * principal_ratio_at_(
                                                                                                            timing=t,
                                                                                                            interest_arr= int_arr,
                                                                                                            # length= len(_interest_arr_) - (interval[0] - 1),
                                                                                                            length= _interest_arr_.end - (interval[0] - 1),
                                                                                                            grace_period= grace_t,
                                                                                                            # prepay_time= prepay_t[t-1]
                                                                                                            prepay_time= prepay_t(t-1)
                                                                                                        )
                            )
                        else:
                            _principal_payment_.append((loan_amount - sum(_principal_payment_[:])))
                    else:
                        # _principal_payment_.append((_residual_[prepay_t[t]]) * principal_ratio_at_(
                        _principal_payment_.append((_residual_[prepay_t(t)]) * principal_ratio_at_(
                                                                                    timing=t,
                                                                                    interest_arr= int_arr,
                                                                                    # length= len(_interest_arr_) - (interval[0] - 1),
                                                                                    length= _interest_arr_.end - (interval[0] - 1),
                                                                                    grace_period= grace_t,
                                                                                    # prepay_time= prepay_t[t] - (interval[0] - 1)
                                                                                    prepay_time= prepay_t(t) - (interval[0] - 1)
                                                                                )
                        )
                _residual_.append(loan_amount - sum(_principal_payment_))
                _interest_.append(_residual_[-2] * int_arr[t]) # Note the calculation of interest is based on the residual of the previous period.
                _total_.append(_principal_payment_[-1] + _interest_[-1])
        else: # note the group at n= 0 equal t= 0 in the _interest_arr_
            _principal_payment_.append(0)
            _residual_.append(loan_amount)
            _interest_.append(0)
            _accum_.append(0)
            _total_.append(0)
    return _principal_payment_, _interest_, _total_, _residual_

# py -m app.Loan.computation.methods
if __name__ == '__main__':
    import time
    from app.Loan.computation.helpers.prepay import _time_, _amount_
    t0= time.time()
    kwargs= {
        'tenure': 30,
        'loan_amount': 800_000_000,
        'interest_arr': {
            'interest': [0.05, 1],
            'time': [4]
        },
        'grace_period': 0,
        'prepay_arr': {
            'time': [3],
            'amount': [10000]
        },
    }

    prepay_t= _time_
    prepay_t.subsidy_time = kwargs.get('subsidy_arr', {}).get('time', 0)
    prepay_t.prepay_time = kwargs.get('prepay_arr', {}).get('time', [0])

    prepay_amount = _amount_(
        subsidy_time= kwargs.get('subsidy_arr', {}).get('time', 0),
        subsidy_amount= kwargs.get('subsidy_arr', {}).get('amount', 0),
        prepay_arr={
            'time': kwargs.get('prepay_arr', {}).get('time', []),
            'amount': ensure_list_type(kwargs.get('prepay_arr', {}).get('amount', []))
        }
    )
    
    kwargs['prepay_arr']['time'] = prepay_t
    kwargs['prepay_arr']['amount'] = prepay_amount

    print(
        # prepay_t,
        # '\n',
        # prepay_amount,
        # '\n',
        _EPP_arr_(**kwargs),
        '\n',
        'time_on_EPP: ', time.time() - t0, 's',
        '\n',
        _ETP_arr_(**kwargs),
        '\n',
        'time_on_ETP: ', time.time() - t0, 's'
    )