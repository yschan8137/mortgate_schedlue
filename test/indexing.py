from loan import calculator, kwargs, df_schema

#  py -m test.indexing
if __name__ == "__main__":
    df = calculator(**kwargs)
    print(
        # df_schema.level_2
        df[[(l0, l1, l2) for (l0, l1, l2) in df.columns if l2 != "剩餘貸款"]]
    )
