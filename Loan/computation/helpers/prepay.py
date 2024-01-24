from numpy import unique  # type: ignore
from .scheduler import scheduler, ensure_list_type
from typing import Optional


# def _time_(
#     tenure: int,
#     subsidy_time: Optional[int] = None,
#     **kwargs
# ) -> list:
#     """
#     The subsidy can be  viewed as a prepayment, we can combine it's time with the prepayment time into a single list.

#     Args:
#     1. subsidy_time(int): the time when the subsidy is applied.
#     2. tenure(int): the tenure of the loan. 
#     3. prepay_arr(dict): a series of prepayment time.
#     """
#     # combine the subsidy time with the prepayment time
#     time_combo = sorted(
#         ensure_list_type(
#             kwargs.get('prepay_arr', {}).get('time', [0]))
#         + (ensure_list_type(subsidy_time) if subsidy_time else [])
#     )
#     # compute the prepayment time
#     prepay_time = scheduler(
#         tenure=tenure,
#         prepay_arr={
#             "time": time_combo,
#         }
#     )
#     return prepay_time


class _time_:
    subsidy_time: Optional[int]= None
    prepay_time: list
    def __new__(cls, value):
        time_combo = sorted(
            ensure_list_type(
                (prepay_time if len(prepay_time:= cls.prepay_time) > 0 else [0]))
            + (ensure_list_type(cls.subsidy_time) if cls.subsidy_time else [])
        )
        return max(k if k <= value else 0 for k in time_combo)


def _amount_(
    # tenure: int,
    subsidy_time,
    subsidy_amount,
    **kwargs
):
    """
    The combined prepayment time can be used to compute the prepayment amount. The subsidy amount is added to the prepayment amount.    
    """
    accumulate_or_not = kwargs.get('prepay_arr', {}).get('accumulator', False)

    # compute the prepayment amount
    prepay_amount = ensure_list_type(kwargs.get('prepay_arr', {}).get('amount', [0]*len(kwargs.get('prepay_arr', {}).get('time', [0]))))
    # prepay_amount = scheduler(
        # tenure=tenure,
        # prepay_arr={
            # 'amount': ensure_list_type(kwargs.get('prepay_arr', {}).get('amount', 0)),
            # 'time': ensure_list_type(kwargs.get('prepay_arr', {}).get('time', [0])),
            # 'accumulator': accumulate_or_not
        # }
    # )
 
    # res = [(prepay if t in kwargs.get('prepay_arr', {}).get('time', [0]) else 0) + int(subsidy_amount if t == subsidy_time else 0) for (t, prepay) in enumerate(prepay_amount)]

    # res=  {
        # k: prepay_amount[n] + int(subsidy_amount if k== subsidy_time else 0) for (n, k) in enumerate(kwargs.get('prepay_arr', {}).get('time', [0]))
        # }
    res= {
        k: (prepay_amount[n] if n < len(prepay_amount) else 0) + int(subsidy_amount if k== subsidy_time else 0) for (n, k) in enumerate(sorted(kwargs.get('prepay_arr', {}).get('time', [0]) + ([subsidy_time] if subsidy_time else [])))
        
    }
    
    return res
     


# py -m app.Loan.computation.helpers.prepay
if __name__ == "__main__":
    import time
    t0= time.time()
    # res_time = _time_(
    #     subsidy_time=13,
    #     tenure= 30,
    #     prepay_arr={
    #         'time': [1, 6, 7, 8, 9]
    #     }
    # )
    res_amount = _amount_(
        # prepay_time=time,
        # tenure= 30,
        subsidy_time= 0,#13,
        subsidy_amount=0,#1000,
        prepay_arr={
            'amount': [1.1, 3.1, 5.1], #[1000, 1000, 1000, 1000, 1000],
            'time': [2, 4, 6], #[1, 6, 7, 8, 13],
            # 'accumulator': True
        },

    )
    prepay_time = _time_
    prepay_time.subsidy_time = 0
    prepay_time.prepay_time = []
    print(
        prepay_time(15),
          '\n',
          res_amount,
          '\n',
          'time: ', time.time() - t0, 's')
