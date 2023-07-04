import numpy as np # type: ignore
from .helpers.adjustments import ETR, Offsets
from .helpers.scheduler import ensure_list_type, scheduler
import itertools

# 本金平均攤還法(Equal Principal Payment)
def _EPP_arr_(
    tenure: int,
    loan_amount: int,
    interest_arr: dict,
    grace_period: int = 0,
    **kwargs
) -> list:
    if isinstance(prepay_time := kwargs.get('prepay_arr', {}).get('time', 0), int):
        raise TypeError('The data type of the time in prepay_arr must be a list, which coveted from the _time_ function in the prepay module')
    if isinstance(prepay_amount := kwargs.get('prepay_arr', {}).get('amount', 0), int):
        raise TypeError('The data type of the amount in prepay_arr must be a list, which coveted from the _amount_ function in the prepay module')
    _payments_ = []
    _residual_ = []
    _interest_ = []
    _total_ = []
    _interest_arr_ = scheduler(
        tenure=tenure,
        interest_arr={
            'interest': ensure_list_type(interest_arr.get('interest', 0)),
            'time': ensure_list_type(interest_arr.get('time', []))
        }
    )
    def payments(
            t,
            amount= loan_amount,
            grace_period= grace_period,
            tenure= tenure,
            prepay_time= prepay_time,
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
                        prepay_time= prepay_time[t-1]  # type: ignore
                    )
            )
            if t > grace_period * 12 else 0
        )
    
    for t in range(len(_interest_arr_)):
        if t > 0:
            if prepay_amount[t] < _residual_[-1]:
                _payments_.append(prepay_amount[t] + payments(
                                                        t= t,
                                                        amount= _residual_[prepay_time[t-1]]
                                                     )
                )
            else:
                _payments_.append(
                    _residual_[t-1]
                )
            _interest_.append(_residual_[-1] * _interest_arr_[t])
            _residual_.append(loan_amount - sum(_payments_))
        else:
            _payments_.append(0)
            _interest_.append(0)
            _residual_.append(loan_amount)
        _total_.append(_payments_[-1] + _interest_[-1])

    return _payments_, _interest_, _total_, _residual_  # type: ignore


# 本息平均攤還法(Equal Total Payment)
def _ETP_arr_(
    tenure,
    loan_amount: int,
    interest_arr: dict,
    grace_period: int= 0,
    **kwargs
    ) -> list:
    # default value  
    _principal_payment_ = []
    _residual_ = []
    _interest_ = []
    _accum_ = [] # while the multi-stages interest rate is applied, the accumulated repament is recorded in order to calculate the present value of the residual.
    _total_ = []

    # The arrangement of interest rate applied to each period.
    _interest_arr_= scheduler(
                        tenure=tenure,
                        interest_arr={
                            'interest': ensure_list_type(interest_arr.get('interest', 0)),
                            'time': ensure_list_type(interest_arr.get('time', []))
                        }
                    )
    # the dynamic arrangement of principal ratio of whole tenure.
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
    
    for (n, (interest, interval)) in enumerate(applied_interval(_interest_arr_)):   
        if n > 0:
            d = (interval[1] - interval[0] + 1) # Note that the end of the interval, namely interval[1], is not included in the calculation of the number of periods.
            _accum_.append(sum(_principal_payment_[:-1])) # To address the situation that the interest rate is changed in the middle of the tenure, the accumulated repayment is recorded in order to calculate the present value of the residual. 
            int_arr = [interest] * (len(_interest_arr_) - (interval[0] - 1))
            grace_t= (round(((grace_period * 12) - interval[0] + 1)/12) if (grace_period * 12) - interval[0] > 0 else 0)

            if isinstance(prepay_time := kwargs.get('prepay_arr', {}).get('time', 0), int):
                raise TypeError('The data type of the time in prepay_arr must be a list, which coveted from the _time_ function in the prepay module')
            if isinstance(prepay_amount := kwargs.get('prepay_arr', {}).get('amount', 0), int):
                raise TypeError('The data type of the amount in prepay_arr must be a list, which coveted from the _amount_ function in the prepay module')
            
            prepay_t = prepay_time[interval[0] - 1:]
            prepay_a = prepay_amount[interval[0] - 1:]
            for t in range(interval[0], interval[1]):
                t = t - (interval[0] - 1)
                if (prepay_t[t] == 0):
                    principal_payment= (loan_amount - (_accum_[n])) * principal_ratio_at_(
                                                                                        timing= t,
                                                                                        interest_arr= int_arr,
                                                                                        length= len(_interest_arr_) - (interval[0] - 1),
                                                                                        grace_period= grace_t,
                                                                                        prepay_time= prepay_t[t],
                                                                    )
                    # ensure the _residual_ to be positive
                    if (_residual_[-1] - principal_payment) >= 0:
                        _principal_payment_.append(principal_payment)
                    else:
                        _principal_payment_.append(_residual_[-1])
                else:
                    if (t == prepay_t[t] - (interval[0] - 1) and prepay_a[t] > 0): # Note that the prepay_t[t] also needed to be subtracted by (interval[0] - 1).
                        # 提前支付金額低於前一期餘額
                        if prepay_a[t] < _residual_[-1]:
                            _principal_payment_.append(prepay_a[t] + (_residual_[prepay_t[t-1]] - (_accum_[n])) * principal_ratio_at_(
                                                                                                            timing=t,
                                                                                                            interest_arr= int_arr,
                                                                                                            length= len(_interest_arr_) - (interval[0] - 1),
                                                                                                            grace_period= grace_t,
                                                                                                            prepay_time= prepay_t[t-1]
                                                                                                        )
                            )
                        else:
                            _principal_payment_.append((loan_amount - sum(_principal_payment_[:-1])))
                    else:
                        _principal_payment_.append((_residual_[prepay_t[t]]) * principal_ratio_at_(
                                                                                    timing=t,
                                                                                    interest_arr= int_arr,
                                                                                    length= len(_interest_arr_) - (interval[0] - 1),
                                                                                    grace_period= grace_t,
                                                                                    prepay_time= prepay_t[t] - (interval[0] - 1)
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
    return _principal_payment_, _interest_, _total_, _residual_  # type: ignore

# py -m loan.computation.methods
if __name__ == '__main__':
    kwargs= {
        'tenure': 30,
        'loan_amount': 800,
        'interest_arr': {
            'interest': [0.05],
            'time': []
        },
        'prepay_time': 0,
        'prepay_amount': 0,
        'grace_period': 0,
    }

    print(
        _EPP_arr_(**kwargs),
        \
        _ETP_arr_(**kwargs),

    )