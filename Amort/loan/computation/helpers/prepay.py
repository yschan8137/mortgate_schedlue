import numpy as np
from .scheduler import scheduler, ensure_list_type
from typing import Optional


def _time_(
    subsidy_time: Optional[int],
    tenure: int,
    **kwargs
) -> list:
    """
    Since the subsidy can be  viewed as a prepayment, we can combine it's time with the prepayment time into a single list.

    Args:
    1. subsidy_time(int): the time when the subsidy is applied.
    2. tenure(int): the tenure of the loan. 
    3. prepay_arr(dict): a series of prepayment time.
    """
    # combine the subsidy time with the prepayment time
    time_combo = sorted(
        ensure_list_type(
            kwargs.get('prepay_arr', {}).get('multi_arr', [0]))
        + ensure_list_type(subsidy_time)
    )
    # compute the prepayment time
    prepay_time = scheduler(
        tenure=tenure,
        prepay_arr={
            "multi_arr": time_combo
        }
    )
    return prepay_time


def _amount_(
    prepay_time: list,
    tenure: int,
    subsidy_time: Optional[int],
    subsidy_amount: Optional[int],
    **kwargs
) -> list:
    """
    The combined prepayment time can be used to compute the prepayment amount. The subsidy amount is added to the prepayment amount.    
    """
    # combine the subsidy time with the prepayment time
    kws_prepay_multi_arr = sorted(
        ensure_list_type(
            kwargs.get('prepay_arr', {}).get('multi_arr', [0]))
        + ensure_list_type(subsidy_time)
    )
    # compute the prepayment amount
    prepay_amount = scheduler(
        tenure= tenure,
        prepay_arr={
            'amount': ensure_list_type(kwargs.get('prepay_arr', {}).get('amount', 0)),
            'multi_arr': [
                v for v in np.unique(prepay_time)
                if v > 0
                and v != subsidy_time
            ],
            # 'accumulator': True # Note: updated on 5/28
        }
    )
    # add the subsidy amount to the prepayment amount
    prepay_amount = [
        prepay_amount[t] + subsidy_amount if t >= subsidy_time  # type: ignore
        and
        (
            t < kws_prepay_multi_arr[kws_prepay_multi_arr.index(
                subsidy_time) + 1]
            if len(kws_prepay_multi_arr) >= kws_prepay_multi_arr.index(subsidy_time) + 2
            else True
        )
        else prepay_amount[t] for t in range(len(prepay_amount))
    ]
    return prepay_amount


# py -m Amort.loan.computation.helpers.prepay
if __name__ == "__main__":
    time= _time_(
            subsidy_time=13,
            tenure=10,
            prepay_arr={
                'multi_arr': [1, 6, 7, 8, 9]
            }
        )
    amount= _amount_(
                prepay_time= time,
                tenure=5,
                subsidy_time=13,
                subsidy_amount=1000,
                prepay_arr={
                    'amount': [1000, 1000, 1000, 1000, 1000],
                    'multi_arr': [1, 6, 7, 8, 9]
                }
            )
    print(amount)