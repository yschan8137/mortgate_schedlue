# 本金平均攤還法(Equal Principal Payment)
import numpy as np

from .helpers.adjustments import ETR, Adjustments
from .helpers.scheduler import ensure_list_type, scheduler

def _EPP_arr_(
  loan_period: int,
  loan_amount: int,
  interest_arr: dict, 
  prepay_time: list,
  prepay_amount: list,
  grace_period: int = 0, 
  ) -> list:
  if isinstance(prepay_amount, int):
    prepay_amount =  [prepay_amount] * (loan_period * 12 + 1)
  if isinstance(prepay_time, int):
    prepay_time = [prepay_time] * (loan_period * 12 + 1)
  _payments_ = []
  _residual_ = []
  _interest_ = []
  _total_ = []
  _interest_arr_ = scheduler(
      loan_period= loan_period, 
      interest_arr= {
          'interest': ensure_list_type(interest_arr.get('interest', 0)), 
          'multi_arr': ensure_list_type(interest_arr.get('multi_arr', []))
          }
      )
  _unique_sum_ = lambda t, prepay_amount= prepay_amount, prepay_time= prepay_time: sum([*np.unique(prepay_amount[:prepay_time[t]])])
  def payments(t,
         amount= loan_amount,
         grace_period= grace_period, 
         loan_period= loan_period,
         prepay_time = prepay_time,
         ):
    return (
         (
          amount
         ) 
         /
         (
          (
           (loan_period - grace_period) * 12
          ) + Adjustments(
              t, 
              grace_period= grace_period ,
              prepay_time= prepay_time[t]
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
            if prepay_amount[t] < payments(t-1):
              _payments_.append(payments(
                    t= prepay_time[t-1],
                    amount= _residual_[prepay_time[t-1]],
                    ))
              prepay_time = [prepay_time[t-1] if t_1 == prepay_time[t] else t_1 for t_1 in prepay_time]
            else:
              _payments_.append(prepay_amount[t])
          else:
            _payments_.append(
                _residual_[t-1]
                    )
        else:
          _payments_.append(
              payments(
                   t= prepay_time[t],
                   amount= _residual_[prepay_time[t]]
            )
          )
      _interest_.append(_residual_[-1] * _interest_arr_[t])
      _residual_.append(loan_amount - sum(_payments_))
    else:
      _payments_.append(0)
      _interest_.append(0)
      _residual_.append(loan_amount)
    _total_.append(_payments_[-1] + _interest_[-1])
  
  return _payments_, _interest_, _total_, _residual_

# 本息平均攤還法(Equal Total Payment)
def _ETP_arr_(
  loan_period: int,
  loan_amount: int, 
  interest_arr: dict, 
  prepay_time: list,
  prepay_amount: list,
  grace_period: int= 0,
  ) -> list:
  if isinstance(prepay_amount, int):
    prepay_amount = [prepay_amount] * (loan_period * 12 + 1)
  if isinstance(prepay_time, int):
    prepay_time = [prepay_time] * (loan_period * 12 + 1)
  _principal_payment_ = []
  _residual_ = []
  _interest_ = []
  _total_ = []
  _interest_arr_ = scheduler(
      loan_period= loan_period, 
      interest_arr= {
          'interest': ensure_list_type(interest_arr.get('interest', 0)), 
          'multi_arr': ensure_list_type(interest_arr.get('multi_arr', []))
          }
      )
  principal_ratio_at_ = lambda timing, prepay_time: ETR(
                      t= timing,
                      interest_arr= _interest_arr_, 
                      loan_period= loan_period, 
                      grace_period= grace_period, 
                      prepay= {'multi_arr': prepay_time}, 
                      ) * (1 + _interest_arr_[t])**(-(1 + loan_period * 12 - t))
  for t in range(0, len(_interest_arr_)):
    if t > 0:
      if (prepay_time[t] == 0):
        _principal_payment_.append(loan_amount * principal_ratio_at_(timing= t, prepay_time = prepay_time[t]))
      else:
        if (t == prepay_time[t] and prepay_amount[t] > 0):
          # 提前支付金額低於前一期餘額
          if prepay_amount[t] < _residual_[-1]:
            # 若提前支付金額低額原始分期付款金額
            if prepay_amount[t] < _residual_[prepay_time[t-1]] * principal_ratio_at_(timing= t, prepay_time = prepay_time[t-1]):
              _principal_payment_.append(_residual_[prepay_time[t-1]] * principal_ratio_at_(timing= t, prepay_time = prepay_time[t-1]))
              # 因調整為原始分配時點
              prepay_time = [prepay_time[t-1] if t_1 == prepay_time[t] else t_1 for t_1 in prepay_time]
            else:  
              _principal_payment_.append(prepay_amount[t])
          else:
            _principal_payment_.append((loan_amount - sum(_principal_payment_[:t])))
        else:
          _principal_payment_.append(_residual_[prepay_time[t]] * principal_ratio_at_(timing= t, prepay_time = prepay_time[t]))
      _residual_.append(loan_amount - sum(_principal_payment_))
      _interest_.append(_residual_[-1] * _interest_arr_[t])
    else:
      _principal_payment_.append(0)
      _residual_.append(loan_amount)
      _interest_.append(0)
    _total_.append(_principal_payment_[-1] + _interest_[-1])

  return _principal_payment_, _interest_, _total_, _residual_