import numpy as np
from .helpers.adjustments import ETR, Adjustments
from .helpers.scheduler import ensure_list_type, scheduler
import itertools

# 本金平均攤還法(Equal Principal Payment)
def _EPP_arr_(
    tenure: int,
    loan_amount: int,
    interest_arr: dict,
    prepay_time: list,
    prepay_amount: list,
    grace_period: int = 0,
) -> list:
    if isinstance(prepay_amount, int):
        prepay_amount = [prepay_amount] * (tenure * 12 + 1)
    if isinstance(prepay_time, int):
        prepay_time = [prepay_time] * (tenure * 12 + 1)
    _payments_ = []
    _residual_ = []
    _interest_ = []
    _total_ = []
    _interest_arr_ = scheduler(
        tenure=tenure,
        interest_arr={
            'interest': ensure_list_type(interest_arr.get('interest', 0)),
            'multi_arr': ensure_list_type(interest_arr.get('multi_arr', []))
        }
    )

    def _unique_sum_(t, prepay_amount=prepay_amount, prepay_time=prepay_time): 
        return sum([*np.unique(prepay_amount[:prepay_time[t]])])

    def payments(t,
                 amount=loan_amount,
                 grace_period=grace_period,
                 tenure=tenure,
                 prepay_time=prepay_time,
                 ):
        return (
            (
                amount
            )
            /
            (
                (
                    (tenure - grace_period) * 12
                ) + Adjustments(
                    t,
                    grace_period=grace_period,
                    prepay_time=prepay_time[t]  # type: ignore
                )
            )
            if t > grace_period * 12 else 0
        )
    for t in range(len(_interest_arr_)):
        if t > 0:
            if (prepay_time[t] == 0):
                _payments_.append(payments(t))
            else:
                if (t == prepay_time[t] and prepay_amount[t] > 0):
                    if prepay_amount[t] < _residual_[-1]:
                        _payments_.append(prepay_amount[t] + payments(t))
                    #########################################
                        # if prepay_amount[t] < payments(t-1):
                            # print('prepay_time on line 64: ', prepay_time)
                            # print("_residual_ on line 65", _residual_)
                            # _payments_.append(
                                # payments(t=prepay_time[t-1], amount=_residual_[prepay_time[t-1]])
                                # )
                            # prepay_time = [
                                # prepay_time[t-1] if t_1 == prepay_time[t] else t_1 for t_1 in prepay_time]
                        # else:
                            # _payments_.append(prepay_amount[t])
                    #########################################
                    else:
                        _payments_.append(
                            _residual_[t-1]
                        )
                else:
                    _payments_.append(
                        payments(
                            t=prepay_time[t],
                            amount=_residual_[prepay_time[t]]
                        )
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
    prepay_time: list,
    prepay_amount: list,
    grace_period: int = 0,
) -> list:
    # default value  
    _principal_payment_ = []
    _residual_ = []
    _interest_ = []
    _accum_ = [] # while the multi-stages interest rate is applied, the accumulated repament is recorded in order to calculate the present value of the residual.
    _accum_interval_= [] # the accumulated interval of the multi-stages interest rate.
    _total_ = []

    # The arrangement of interest rate applied to each period.
    _interest_arr_= scheduler(
                        tenure=tenure,
                        interest_arr={
                            'interest': ensure_list_type(interest_arr.get('interest', 0)),
                            'multi_arr': ensure_list_type(interest_arr.get('multi_arr', []))
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
                    prepay={'multi_arr': prepay_time},
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
    
    # prepay有問題
    for (n, (interest, interval)) in enumerate(applied_interval(_interest_arr_)):   
        if n > 0: 
            d = (interval[1] - interval[0] + 1) # Note that the end of the interval, namely interval[1], is not included in the calculation of the number of periods.
            print('d on line 185: ', d)
            _accum_.append(sum(_principal_payment_[:-1])) # To address the situation that the interest rate is changed in the middle of the tenure, the accumulated repayment is recorded in order to calculate the present value of the residual. 
            int_arr = [interest] * (len(_interest_arr_) - (interval[0] - 1))
            if isinstance(prepay_amount, int):
                prepay_amount = [prepay_amount] * d
            if isinstance(prepay_time, int):
                prepay_time = [prepay_time] * d
            for t in range(interval[0], interval[1]):
                t = t - (interval[0] - 1)
                grace_period= (g := grace_period - round(interval[0]/12) if (g >= 0) else 0)
                prepay_time[t] = ((p:= prepay_time[t] - (interval[0]/12)) if (p>= 0) else 0)
                if (prepay_time[t] == 0):
                    principal_payment= (loan_amount - (_accum_[n])) * principal_ratio_at_(
                                                                                        timing= t,
                                                                                        interest_arr= int_arr,
                                                                                        length= len(_interest_arr_) - (interval[0] - 1),
                                                                                        grace_period= grace_period,
                                                                                        prepay_time= prepay_time[t],
                                                                    )
                    # ensure the _residual_ to be positive
                    if (_residual_[-1] - principal_payment) >= 0:
                        _principal_payment_.append(principal_payment)
                    else:
                        _principal_payment_.append(_residual_[-1])
                else:
                    if (t == prepay_time[t] and prepay_amount[t] > 0):
                        # 提前支付金額低於前一期餘額
                        if prepay_amount[t] < _residual_[-1]:
                            _principal_payment_.append(prepay_amount[t] + _residual_[prepay_time[t-1]] * principal_ratio_at_(
                                                                                                            timing=t,
                                                                                                            interest_arr= int_arr,
                                                                                                            length= len(_interest_arr_) - (interval[0] - 1),
                                                                                                            grace_period= grace_period,
                                                                                                            prepay_time=prepay_time[t-1]
                                                                                                        )
                            )
                        else:
                            _principal_payment_.append((loan_amount - sum(_principal_payment_[:-1])))
                    else:
                        _principal_payment_.append(_residual_[
                                                   prepay_time[t]] * principal_ratio_at_(
                                                                        timing=t,
                                                                        interest_arr= int_arr,
                                                                        length= len(_interest_arr_) - (interval[0] - 1),
                                                                        grace_period= grace_period,
                                                                        prepay_time= prepay_time[t]
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

# py -m Amort.loan.computation.methods
if __name__ == '__main__':
    kwargs= {
        'tenure': 30,
        'loan_amount': 800,
        'interest_arr': {
            'interest': [0.05],
            'multi_arr': []
        },
        'prepay_time': 0,
        'prepay_amount': 0,
        'grace_period': 0,
    }

    print(
        # _EPP_arr_(**kwargs),
        # \
        _ETP_arr_(**kwargs),

    )