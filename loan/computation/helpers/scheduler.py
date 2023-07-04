from itertools import accumulate
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


def merge_sublist(x) -> list:
    """
    To merge sublists into sole list.
    """
    return [value for sublist in x for value in sublist if value != None]


def ensure_list_type(x) -> list:
    """
    Ensuring the outcome type is list, which as mentioned as the name of the function.
    """
    return (x if isinstance(x, list) else [x])


def kwargs_detection(
    kws_spec={
        'tenure': int,
        'loan': int,
        'interest_arr': {
            'interest': list,
            'time': list
        },
        'prepay_arr': {
            'amount': list,
            'time': list,
            'accumulator': bool
        }
    },
        **kwargs) -> None:
    """
    Serving a purpose for examing the keyword arguments fitting the given argument structure.   
    """
    false_kwargs = [
        v for v in [
            (
                v
                if v not in kws_spec
                else (
                    [
                        {v: {[*kwargs[v]][0]}}, [*kwargs[v].values()][0]]
                    if isinstance(kwargs[v], dict) and type([*kwargs[v].values()][0]) not in [*kws_spec[v].values()]
                    else
                    (
                        {v: [*kwargs[v]][0]}
                        if isinstance(kwargs[v], dict) and [*kwargs[v].keys()][0] not in [*kws_spec[v]]
                        else None
                    )
                )
            )
            for v in kwargs
        ]
        if v != None
    ]

    if false_kwargs:
        for false in false_kwargs:
            if isinstance(false, str):
                raise KeyError(
                    f"Error in arguments: {false}.  The available arguments: {kws_spec}")
            elif isinstance(false, dict):
                raise KeyError(
                    f"Error in arguments: {[*false.values()]} in {[*false.keys()]}.  The available arguments: {kws_spec}")
            else:
                raise KeyError(
                    f"Error in arguments types: {false[1]} in {false[0]}.  The right type is: {kws_spec[[*false[0].keys()][0]][[*[*false[0].values()][0]][0]]}")


def scheduler(
    tenure: int,
    loan: int = 0,
    convert_to_month_base: bool = True,
    **kwargs: dict
) -> list:
    """
    The scheduler of the applied interest (feasible for single and multistage loan interest rate), loan and loan prepayment.

    Arguments:

    1. tenure (on a yearly basis): Length of total loan period.

    2. interest_arr:

      2.1 interest: Interest rates applied on each time point. Multistage rate is allowed if the [time] is specified in list of sequential time when the rate adjustment happended. 

      2.2 time (yearly basis): The end time points of the multistage interests applied. 
          Singlestage rate is not required to specified the [time], the value would be set as [0] by default. 
          Note: [mulit_arr] should be specified as list and the number of the elements is restricted to be the (number of applied interest - 1). 

    3. loan (on a yearly basis): The total amount of the loan.    

    4. prepay_arr 
      4.1 prepay: The total amount of the loan prepayment(s). If prepayment occured multiple times within the loan period, the prepayments should be set in list.

      4.2 time (yearly basis): The time points when the prepayments occured. 
                       If prepayment occured multiple times within the loan period, the prepa_time should be set in list.  

      4.3 accumulator(False by default): accumulate the amount on the change point.

    Example:

        Suppose a 10-year multi-stage interest rate loan of 500,000 with the interest rate changing at t=12, along with prepayments of 200,000 at t=5 and at t=60. 
        The arguments setting would be as follows:

        scheduler(
          tenure= 10, 
          interest_arr= {
            'interest': [1.38, 1.01],
            'time': [12]
          }, 
          loan= 500_000,
          prepay_arr = {
            'amount': [200_000, 200_000],
            'time': [5, 60],
            'accumulator': True
          }
       )
    """
    kwargs_detection(
        kws_spec={
            'tenure': int,
            'interest_arr': {'interest': list,
                             'time': list},
            'prepay_arr': {'amount': list,
                           'time': list,
                           'accumulator': bool}
        },
        **kwargs)

    tenure = tenure * 12
    interest = list(map(
        lambda x: x/100, ensure_list_type(kwargs.get('interest_arr', {}).get('interest', 0))))
    interest_arr = [
        0] + sorted(ensure_list_type(kwargs.get('interest_arr', {}).get('time', [])))
    prepay = [0] + \
        ensure_list_type(kwargs.get('prepay_arr', {}).get('amount', []))
    prepay_arr = [
        0] + sorted(ensure_list_type(kwargs.get('prepay_arr', {}).get('time', [])))
    prepay_accumulator = kwargs.get('prepay_arr', {}).get('accumulator', False)

    if prepay_accumulator == True:
        prepay = list(accumulate(prepay))

    if len(interest) > 1:
        if len(interest_arr) == 0:
            raise KeyError(
                '\r' + 'The [time] should be specified under multistage interest rate frsmework' + '\n')
        if len(interest_arr) > len(interest):
            raise ValueError(
                '\r' + '[time] should be indicated as the rate adjusting points. The example is shown in arguments discription for reference' + '\n')
        elif len(interest_arr) < len(interest):
            raise ValueError(
                '\r' + f'The adjustments of the interest rate is {len(interest)}, exceed the given time points, which is {len(interest_arr)}' + '\n')

    def _arr_(
        period: int = tenure,
        amount_arr=None,
        time_arr=[0]
    ):
        res = []
        amount_arr = ensure_list_type(amount_arr)
        time_arr = ensure_list_type(time_arr)
        for (v, thred) in zip([0] + (amount_arr if len(amount_arr) == len(time_arr) else time_arr), time_arr + [period]):
            for t in range(0 + len(res), thred + 1):
                if t == 0:
                    res.append(0)
                elif t < thred or t == period:
                    res.append(v)
        return res

    res = map(
        lambda loan, interest, prepay: (
            loan - (prepay if loan > 0 else (loan - 1 if prepay ==
                                             0 and interest > 0 else - prepay))
        ) * (interest if interest > 0 else 1),
        _arr_(amount_arr=loan),
        map(lambda x: (x/12 if convert_to_month_base == True else x),
            _arr_(amount_arr=interest, time_arr=interest_arr)),
        _arr_(amount_arr=prepay, time_arr=prepay_arr)
    )
    res = list(map(lambda x: x if x > 0 else 0, res))
    return res


# py -m loan.computation.helpers.scheduler
payment = scheduler(
    tenure=10,
    interest_arr={
        'interest': [1.38, 1],
        'time': [12]
    },
    loan=500_000,
    prepay_arr={
        'amount': [200_000, 200_000],
        'time': [5, 60],
        'accumulator': True
    }
)
if __name__ == "__main__":
    import pandas as pd  # type: ignore
    print(
        [(t, v) for t, v in enumerate(payment)]
    )
