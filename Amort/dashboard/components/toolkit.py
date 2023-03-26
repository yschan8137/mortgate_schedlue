# Convert to form of the options in dcc.dropdown
def to_dropdown_options(values: list[str]) -> list[dict[str, str]]:
    return [{"label": value, "value": value} for value in values]

# Convert to form of the data in dash.DataTable


def convert_df_to_dash(df):
    """
    Converts a multicolumns pandas data frame to a format accepted by dash
    Returns columns and data in the format which dash requires
    """

    cols = [{"name": [""] * (len(df.columns[0]) - 1) + ["Time"], "id": "Ccy Pair"}] + [
        {"name": [*col], "id": "_".join([*col])} for col in df.columns]
    # build data list from ids and rows of the dataframe
    data = [
        {
            **{"Ccy Pair": df.index[n]},
            **{"_".join([*col]): y for col, y in data},
        }
        for (n, data) in [
            *enumerate([list(x.items()) for x in df.T.to_dict().values()])
        ]
    ]
    return cols, data

# suffix format for prepayment and subsidy to avoid id conflict.


def suffix_for_type(x): return x + "_" + type
