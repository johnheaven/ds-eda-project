def groupby_avg_and_len(df, use_cols, groupby_col, mean_only=True):
    """Groupby on a df object with mean and count

    Args:
        df (DataFrame): The DF to to the groupby on
        use_cols (list): List of columns to use
        groupby_col (string): Column to group by

    Returns:
        _type_: _description_
    """

    import numpy as np
    import pandas as pd
    df = df.copy()
    if mean_only:
        grouped = df[use_cols].groupby(groupby_col).aggregate([np.mean, len])
    else:
        from scipy import stats
        grouped = df[use_cols].groupby(groupby_col).aggregate([np.mean, np.median, stats.mode, len])

    grouped.columns = grouped.columns.to_flat_index()
    grouped.columns = ["_".join(col) for col in grouped.columns]
    return grouped

def get_zip_averages(df, mean_only=True):
    """
    Generates a DataFrame with lat and long information about ZIPs.
    Args:
        df (pd.DataFrame): A DataFrame with `zipcode` and `price` columns

    Returns:
        Pandas DataFrame: A DataFrame with zip codes, lat, long and mean price + count of items in each zip code
    """
    
    import pgeocode
    import numpy as np
    import pandas as pd
    nomi = pgeocode.Nominatim("us")

    # group by zipcode and get the mean price for each one along with the count
    zips = groupby_avg_and_len(df, ["zipcode", "price"], "zipcode", mean_only)
    # round
    zips["price_mean"] = np.around(zips["price_mean"], -3).astype(int)
    if not mean_only:
        zips["price_median"] = np.around(zips["price_median"], -3).astype(int)
    # get lat and long for zip codes
    zips["latitude"] = zips.index.to_series().apply(lambda s: nomi.query_postal_code(s)["latitude"])
    zips["longitude"] = zips.index.to_series().apply(lambda s: nomi.query_postal_code(s)["longitude"])
    zips["name"] = zips.index.to_series().apply(lambda s: nomi.query_postal_code(s)["place_name"])
    return zips
