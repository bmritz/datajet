from functools import lru_cache
from types import FunctionType


def data_map_from_df(df_factory: FunctionType, use_cache: bool = True) -> dict:
    if use_cache:
        df_factory = lru_cache(maxsize=1)(df_factory)
    df = df_factory()
    return {
        # This is tricky but necessary: https://stackoverflow.com/a/7546960
        # Without 2 lambdas, the field gets evaluated inside this function scope
        # when you do go and call the lambda.
        # Solution is to call the field inside this scope (1st lambda) and
        # return another lambda that doesn't need field as an input
        field: dict(f=(lambda field: (lambda: df_factory()[field]))(field))
        for field in df.columns
    }
