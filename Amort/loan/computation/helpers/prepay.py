import numpy as np
from .scheduler import scheduler, ensure_list_type
from typing import Optional


def _time_(
    subsidy_time: Optional[int],
    tenure: int,
    **kwargs
) -> list:
    kws_prepay_multi_arr = sorted(
        ensure_list_type(
            kwargs.get('prepay_arr', {}).get('multi_arr', [0]))
        + ensure_list_type(subsidy_time)
    )
    prepay_time = scheduler(
        tenure=tenure,
        prepay_arr={
            "multi_arr": kws_prepay_multi_arr
        }
    )
    return prepay_time


def _amount_(
    prepay_time: list,
    tenure: int,
    subsidy_time: Optional[int],
    subsidy_amount=Optional[int],
    **kwargs
) -> list:
    kws_prepay_multi_arr = sorted(
        ensure_list_type(
            kwargs.get('prepay_arr', {}).get('multi_arr', [0]))
        + ensure_list_type(subsidy_time)
    )
    prepay_amount = scheduler(
        tenure=tenure,
        prepay_arr={
            'amount': ensure_list_type(kwargs.get('prepay_arr', {}).get('amount', 0)),
            'multi_arr': [
                v for v in np.unique(prepay_time)
                if v > 0
                and v != subsidy_time
            ]
        }
    )
    prepay_amount = [
        prepay_amount[t] + subsidy_amount if t >= subsidy_time
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
