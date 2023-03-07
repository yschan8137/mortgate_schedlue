from lib2to3.pytree import convert
import pandas as pd

from Amort.loan import calculator
from collections import OrderedDict
from Amort.loan.main import test_df

def convert_df_to_dash(df):
    """
    Converts a multicolumns pandas data frame to a format accepted by dash
    Returns columns and data in the format dash requires
    """

    cols = [{"name": [""]* (len(df.columns[0]) - 1) + ["Time"], "id": "Ccy Pair"}] + [{"name": [*col], "id": "_".join([*col])} for col in df.columns]
    # [{"name": ["Time", "1", "2"], "id": "Ccy Pair"}] + [{"name": [x1, x2, x3], "id": f"{x1}_{x2}_{x3}"} for x1, x2, x3 in df.columns]
    
    # build data list from ids and rows of the dataframe
    data = [
        {
            **{"Ccy Pair": df.index[n]},
            **{"_".join([*col]): y for col, y in data},
        }
        for (n, data) in [
            *enumerate(
              [
                list(x.items()) for x in df.T.to_dict().values()])
            ]
           ]
    return cols, data

# py -m Amort.test.multilevels_df_to_nested_dictionary
if __name__ == "__main__":
  df_test= test_df() 
  print(
    # len(df_test.columns[0])
    # (len(df_test.values) - 1) / 100
      convert_df_to_dash(df_test)[0]
  )