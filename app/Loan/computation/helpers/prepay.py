from numpy import unique  # type: ignore
from app.Loan.computation.helpers.scheduler import scheduler, ensure_list_type
from typing import Optional


def _time_(
    tenure: int,
    subsidy_time: Optional[int] = None,
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
            kwargs.get('prepay_arr', {}).get('time', [0]))
        + (ensure_list_type(subsidy_time) if subsidy_time else [])
    )
    # compute the prepayment time
    prepay_time = scheduler(
        tenure=tenure,
        prepay_arr={
            "time": time_combo,
        }
    )
    return prepay_time


def _amount_(
    tenure: int,
    # prepay_time: list,
    subsidy_time,
    subsidy_amount,
    **kwargs
) -> list:
    """
    The combined prepayment time can be used to compute the prepayment amount. The subsidy amount is added to the prepayment amount.    
    """
    # combine the subsidy time with the prepayment time
    # kws_prepay_time = sorted(
    # ensure_list_type(
    # kwargs.get('prepay_arr', {}).get('time', [0]))
    # + ensure_list_type(subsidy_time)
    # )

    # prepay_time = _time_(
    # tenure=tenure,
    # subsidy_time=subsidy_time,
    # prepay_arr={
    # 'time': kwargs.get('prepay_arr', {}).get('time', [0]),
    # }
    # )

    accumulate_or_not = kwargs.get('prepay_arr', {}).get('accumulator', False)

    # compute the prepayment amount
    prepay_amount = scheduler(
        tenure=tenure,
        prepay_arr={
            'amount': ensure_list_type(kwargs.get('prepay_arr', {}).get('amount', 0)),
            'time': ensure_list_type(kwargs.get('prepay_arr', {}).get('time', [0])),
            'accumulator': accumulate_or_not
        }
    )
    
    prepay_amount = [(prepay if t in kwargs.get('prepay_arr', {}).get('time', [0]) else 0) + int(subsidy_amount if t == subsidy_time else 0) for (t, prepay) in enumerate(prepay_amount)]
    # prepay_amount = scheduler(
    # tenure=tenure,
    # prepay_arr={
    # 'amount': ensure_list_type(kwargs.get('prepay_arr', {}).get('amount', 0)),
    # 'time': [
    # v for v in unique(prepay_time)
    # if v > 0
    # and v != subsidy_time
    # ],
    # 'accumulator': accumulate_or_not  # Note: updated on 6/27
    # }
    # )
    # add the subsidy amount to the prepayment amount
    # prepay_amount = [
    # prepay_amount[t] + subsidy_amount if t >= subsidy_time  # type: ignore
    # and
    # (
    # t < prepay_time[prepay_time.index(
    # subsidy_time) + 1]
    # if len(prepay_time) >= prepay_time.index(subsidy_time) + 2
    # else True
    # )
    # else prepay_amount[t] for t in range(len(prepay_amount))
    # ]
    return prepay_amount


# py -m loan.computation.helpers.prepay
if __name__ == "__main__":
    time = _time_(
        # subsidy_time=13,
        tenure=10,
        prepay_arr={
            'time': [1, 6, 7, 8, 9]
        }
    )
    amount = _amount_(
        # prepay_time=time,
        tenure=5,
        subsidy_time=13,
        subsidy_amount=1000,
        prepay_arr={
            'amount': [1000, 1000, 1000, 1000, 1000],
            'time': [1, 6, 7, 8, 13],
            # 'accumulator': True
        },

    )
    # print(f"the time is {time}")
    print([*enumerate(amount)])
