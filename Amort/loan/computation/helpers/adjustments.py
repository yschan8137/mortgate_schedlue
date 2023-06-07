from .scheduler import ensure_list_type, scheduler

def Adjustments(
    t: int, 
    grace_period: int, 
    prepay_time: int, 
    # subsidy_time: int
    ):
  """
  The adjust item of the timepoints regarding the prepayments and payments from subsidy loan.
  Note that the [full_length] is the whole lentgh of the data series, the data array would start from 0, 
  it should equal to the full period of the loan + 1.   
  """
  grace_period_adjustments = lambda x: (x - grace_period * 12 if x > grace_period * 12 else 0)
  return (
       - (grace_period_adjustments(prepay_time)
        )
       )

def ETR(
    t: int, 
    interest_arr: list, 
    length: int, 
    grace_period: int = 0, 
    **kwargs
    ):
  """
  1. 本息攤還率的調整項(adjustments)，須考量3種情境：
  (1) 只有提前付款而不申請房貸補貼 --> 僅須減1次prepay_time
  (2) 只有申請房貸補貼而不提前付款 --> 僅須減1次subsidy_time
  (3) 不但提前付款，也申請房貸補貼 --> 須再考量3種情況：
    i 提前付款在申請房貸補貼之前 --> 須先減prepay_time，再加回(subsidy_time - prepay_time)
    ii 申請房貸補貼在提前付款之前 --> 須先減subsidy_time，再加回(prepay_time - subsidy_time)
    iii 同時提前付款與申請房貸補貼 --> 扣prepay_time或subsidy_time其中1項，偏好設定扣prepay_time的條件
  
  2. 考慮加入寬限期(grace_period * 12)的影響：
    寬限期內本息攤還率(ETR)為0，
    若在寬限期到期後提前付款，調整項存在重複扣除項，須再扣除grace_period * 12。
    若在寬限期內提前付款，雖然已經有設定本金攤還率為0，但保險起見，還是把調整項(grace_period_adjustments)設為0 
  """
  prepay_time = kwargs.get('prepay', {}).get('multi_arr', length - 1)
  multi_arr = [0] + kwargs.get('interest_arr', [])
  length_in_year = (length - 1) / 12

  if len(interest_arr) == length:
    pass
  else: 
    interest_arr = scheduler(
        tenure= length_in_year,
        interest_arr = {
            'interest': ensure_list_type(interest_arr),
            'interest_arr': ensure_list_type(multi_arr),    
              }
          )
  return (
       (
        (
         (
          (1 + interest_arr[t])**((length_in_year - grace_period) * 12 + Adjustments(t, grace_period= grace_period, prepay_time= prepay_time))
         ) * interest_arr[t] 
       )
       / 
        (
         (
          (1 + interest_arr[t])**((length_in_year - grace_period) * 12 + Adjustments(t, grace_period= grace_period ,prepay_time= prepay_time))
         ) - 1
        )
       ) if interest_arr[t] > 0 and t > grace_period * 12 else 0
      )


# py -m Amort.loan.computation.helpers.adjustments
if __name__ == '__main__':
  print(
    ETR(
      t= 12, 
      interest_arr= [1.38], 
      tenure= 30, 
      grace_period= 0, 
      )
  )