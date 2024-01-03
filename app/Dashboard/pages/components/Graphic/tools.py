"""This file contains a function that filters the data to be displayed in the graph."""
from app.Loan import calculator, default_kwargs, example_for_subsidy_arr

def filter(data):
    """
    data: dict
    """
    res= {
        'Index': [],
        'columns' : [],
        'data': [],
    }
    return res


# python -m app.Dashboard.pages.components.Graphic.filter
if __name__ == "__main__":
    default_kwargs['subsidy_arr'] = example_for_subsidy_arr
    print(
        
        calculator(
            **default_kwargs
        )
    )