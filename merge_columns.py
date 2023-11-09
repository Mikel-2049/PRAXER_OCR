import pandas as pd

def merge_columns(*dataframes):
    """
    Merges multiple DataFrames into a single DataFrame.
    Assumes that all DataFrames have the same index and are to be concatenated horizontally.

    Parameters:
    *dataframes: a variable number of DataFrame objects to merge

    Returns:
    A single DataFrame with all of the provided columns merged.
    """
    return pd.concat(dataframes, axis=1)

