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

        # a bit of a hack to keep us from having to rename the mode column while enabling us to pass a parameter to mode to suppress a deprecation warning
        mode = lambda x: stats.mode(x, keepdims=True)
        mode.__name__ = "mode"

        grouped = df[use_cols].groupby(groupby_col).aggregate(["mean", np.median, mode, len])

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

def map_zips(zips, title="Zip Codes in King's County", width=1600, height=800, color="price_mean", size="price_len", save_html=False, save_jpg=False):
    """ Maps zip codes with Seaborn, optionally saves output to HTML or JPEG files too

    Args:
        zips (_type_): _description_
        title (str, optional): The title. Defaults to "Zip Codes in King's County".
        sizecount (bool, optional): Whether size is the count (i.e. number of data). Defaults to False.
        save_html (bool, optional): Whether to save to HTML. Defaults to True.
        save_jpg (bool, optional):
    """
    import plotly.express as px
    zips["_prefix"] = " ("
    zips["_suffix"] = ")"
    zips["hover"] = zips.index.astype(str) + zips["_prefix"] + zips["name"] + zips["_suffix"]
    fig = px.scatter_mapbox(
        zips,
        mapbox_style="open-street-map",
        lat="latitude",
        lon="longitude",
        color=color,
        title=title,
        hover_name="hover",
        width=width,
        height=height,
        size=size,
        zoom=8.5,
        labels={"price_mean": "Mean price for ZIP code"},
        color_continuous_scale=px.colors.sequential.Inferno_r
        )

    fig.show()
    if save_html or save_jpg:
        file_name = title.replace(" ", "_")
        file_name = ''.join(e for e in file_name if (e.isalnum() or e == "_")).lower()
    if save_html:
        fig.write_html(f"html/{file_name}.html")
    if save_jpg:
        pass
        fig.write_image(f"images/{file_name}.jpg", width=width, height=height)
        
def plot_monthly_prices(df, title=None, ytick_lim=1.4e6, cut_y=4e5):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    fig, ax = plt.subplots()
    df = df.copy()
    df["month"] = df["date"].dt.month
    df_month_prices = df[["month", "price"]].groupby("month").median()
    p = sns.lineplot(axes=ax, data=df_month_prices, x="month", y="price")
    plt.xticks(rotation=45)

    # calculate upper limit for y axis (ytick_lim) with padding to next 100,000 unless one is passed as argument
    if ytick_lim is None:
        pricemax = df_month_prices["price"].max()
        ytick_lim = pricemax - (pricemax // 1e5)

    ax.set_yticks(ticks=np.arange(cut_y, ytick_lim + 1e5, 1e5))
    ax.set_xticks(ticks=df_month_prices.index, labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    ax.set_title(title, fontsize=16)
    ax.set_xlabel("Month")
    ax.set_ylabel("Price")
    ax.ticklabel_format(axis="y", style="plain")
