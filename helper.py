import numpy as np


def country_year_list(df):
    years = df["Year"].unique().tolist()
    years.sort()
    years.insert(0, "Overall")

    country = np.unique(df["region"].dropna().values).tolist()
    country.sort()
    country.insert(0, "Overall")

    return years, country


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
    )
    flag = 0

    if year == "Overall" and country == "Overall":
        temp_df = medal_df
    if year == "Overall" and country != "Overall":
        flag = 1

        temp_df = medal_df[medal_df["region"] == country]
    if year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df["Year"] == int(year)]
    if year != "Overall" and country != "Overall":
        temp_df = medal_df[
            (medal_df["Year"] == int(year)) & (medal_df["region"] == country)
        ]

    if flag == 1:
        x = (
            temp_df.groupby("Year")
            .sum()[["Gold", "Silver", "Bronze"]]
            .sort_values("Year", ascending=True)
            .reset_index()
        )
    else:
        x = (
            temp_df.groupby("region")
            .sum()[["Gold", "Silver", "Bronze"]]
            .sort_values("Gold", ascending=False)
            .reset_index()
        )

    x["total"] = x["Gold"] + x["Silver"] + x["Bronze"]

    return x


def data_over_time(df, col):
    over_time = (
        df.drop_duplicates(["Year", col])["Year"]
        .value_counts()
        .reset_index()
        .sort_values("Year")
    )

    over_time.rename(columns={"Year": "Edition", "count": col}, inplace=True)

    return over_time


def most_successful(df, sport):
    df.columns = df.columns.str.strip()
    temp_df = df.dropna(subset=["Medal"])

    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]

    # Count medals per athlete and rename properly
    top_athletes = (
        temp_df["Name"]
        .value_counts()
        .reset_index()
        .rename(
            columns={"Medal Count": "Name", "count": "Medal Count"}
        )  # Use this if column is still 'Name'
        .head(15)
    )

    # Merge with original df to get more info
    merged_df = top_athletes.merge(df, on="Name", how="left")[
        ["Name", "Medal Count", "Sport", "region"]
    ].drop_duplicates("Name")

    return merged_df.reset_index(drop=True)


def year_wise_medal_tally(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"],
        inplace=True,
    )

    new_df = temp_df[temp_df["region"] == country]
    final_df = new_df.groupby("Year").count()["Medal"].reset_index()

    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"],
        inplace=True,
    )

    new_df = temp_df[temp_df["region"] == country]
    final_df = new_df.pivot_table(
        index="Sport", columns="Year", values="Medal", aggfunc="count"
    ).fillna(0)

    return final_df


def most_successful_atheletes_country(df, country):
    df.columns = df.columns.str.strip()
    temp_df = df.dropna(subset=["Medal"])

    temp_df = temp_df[temp_df["region"] == country]

    # Count medals per athlete and rename properly
    top_athletes = (
        temp_df["Name"]
        .value_counts()
        .reset_index()
        .rename(
            columns={"Medal Count": "Name", "count": "Medal Count"}
        )  # Use this if column is still 'Name'
        .head(10)
    )

    # Merge with original df to get more info
    merged_df = top_athletes.merge(df, on="Name", how="left")[
        ["Name", "Medal Count", "Sport"]
    ].drop_duplicates("Name")

    return merged_df.reset_index(drop=True)


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=["Name", "region"])
    athlete_df["Medal"].fillna("No Medal", inplace=True)
    
    if sport != "Overall":
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=["Name", "region"])

    men = (
        athlete_df[athlete_df["Sex"] == "M"]
        .groupby("Year")
        .count()["Name"]
        .reset_index()
    )
    women = (
        athlete_df[athlete_df["Sex"] == "F"]
        .groupby("Year")
        .count()["Name"]
        .reset_index()
    )

    final = men.merge(women, on="Year", how="left")
    final.rename(columns={"Name_x": "Male", "Name_y": "Female"}, inplace=True)

    final.fillna(0, inplace=True)

    return final
