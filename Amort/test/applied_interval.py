from flask import app
from Amort.loan.computation.helpers.scheduler import *
import itertools
import numpy as np

_interest_arr_= scheduler(
                    tenure= 30,
                    interest_arr={
                        'interest': [1.38, 1.5],
                        'multi_arr': [5]
                    }
                )

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
       

# py -m Amort.test.applied_interval
if __name__ == "__main__":
    print(
      #  _interest_arr_,
        applied_interval(_interest_arr_)
    )