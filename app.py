import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

st.set_page_config(layout="wide", page_title="🏅 Olympics Analysis Dashboard")

with st.spinner("Loading data..."):
    df = pd.read_csv("./datasets/athlete_events.csv")
    region_df = pd.read_csv("./datasets/noc_regions.csv")
    df = preprocessor.preprocess(df, region_df)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .css-18e3th9 {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stMetricValue {
        font-size: 24px;
        color: #4CAF50;
    }
    .stMetricLabel {
        color: #888;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.sidebar.image(
    "https://img.icons8.com/color/96/olympic-rings.png", use_container_width=True
)
st.sidebar.title("Olympics Dashboard")

user_menu = st.sidebar.radio(
    "📊 Select an Option",
    (
        "Medal Tally",
        "Overall Analysis",
        "Country-wise Analysis",
        "Athlete-wise Analysis",
    ),
)

if user_menu == "Medal Tally":
    st.sidebar.header("🎖️ Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    st.title(f"🏆 Medal Tally")
    subtitle = (
        f"{selected_country} - {selected_year}"
        if selected_year != "Overall" or selected_country != "Overall"
        else "Overall"
    )
    st.subheader(f"🔹 {subtitle}")
    st.dataframe(medal_tally, use_container_width=True)

if user_menu == "Overall Analysis":
    st.title("📈 Overall Analysis")

    editions = df["Year"].nunique() - 1
    cities = df["City"].nunique()
    sports = df["Sport"].nunique()
    events = df["Event"].nunique()
    athletes = df["Name"].nunique()
    regions = df["region"].nunique()

    with st.container():
        st.subheader("Key Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Editions", editions)
        col2.metric("Host Cities", cities)
        col3.metric("Total Sports", sports)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Events", events)
        col2.metric("Participating Nations", regions)
        col3.metric("Athletes", athletes)

    st.markdown("---")

    with st.expander("📌 Participation Trends Over Time"):
        col1, col2 = st.columns(2)
        with col1:
            nations = helper.data_over_time(df, "region")
            fig = px.line(nations, x="Edition", y="region", title="Nations Over Time")
            st.plotly_chart(fig, use_container_width=True)

            athletes = helper.data_over_time(df, "Name")
            fig = px.line(athletes, x="Edition", y="Name", title="Athletes Over Time")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            events = helper.data_over_time(df, "Event")
            fig = px.line(events, x="Edition", y="Event", title="Events Over Time")
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("📅 Event Distribution Over the Years")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    data = (
        x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count")
        .fillna(0)
        .astype(int)
    )
    sns.heatmap(data, annot=True, ax=ax, cmap="YlGnBu")
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("🥇 Most Successful Athletes")
    all_sports = sorted(df["Sport"].unique().tolist())
    all_sports.insert(0, "Overall")
    selected_sport = st.selectbox("Select Sport", all_sports)
    top_athletes = helper.most_successful(df, selected_sport)
    st.dataframe(top_athletes, use_container_width=True)

if user_menu == "Country-wise Analysis":
    st.sidebar.header("🏳️ Country-wise Analysis")
    countries = sorted(df["region"].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("Select Country", countries)

    st.title(f"📈 {selected_country} Performance")
    medal_df = helper.year_wise_medal_tally(df, selected_country)
    fig = px.line(medal_df, x="Year", y="Medal", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🎯 Event Heatmap")
    country_event_df = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(country_event_df, annot=True, ax=ax, cmap="coolwarm")
    st.pyplot(fig)

    st.subheader("🏅 Top 10 Athletes")
    top10_df = helper.most_successful_atheletes_country(df, selected_country)
    st.dataframe(top10_df, use_container_width=True)

if user_menu == "Athlete-wise Analysis":
    athlete_df = df.drop_duplicates(subset=["Name", "region"])

    # Age Distribution
    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()

    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ["Overall Age", "Gold Medalist", "Silver Medalist", "Bronze Medalist"],
        show_rug=False,
        show_hist=False,
    )
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.markdown(
        "This plot shows the age distribution of athletes categorized by medal status."
    )
    st.plotly_chart(fig, use_container_width=True)

    # Age analysis with respect to popular sports
    x = []
    name = []
    famous_sports = [
        "Basketball",
        "Judo",
        "Football",
        "Tug-Of-War",
        "Athletics",
        "Swimming",
        "Badminton",
        "Sailing",
        "Gymnastics",
        "Art Competitions",
        "Handball",
        "Weightlifting",
        "Wrestling",
        "Water Polo",
        "Hockey",
        "Rowing",
        "Fencing",
        "Shooting",
        "Boxing",
        "Taekwondo",
        "Cycling",
        "Diving",
        "Canoeing",
        "Tennis",
        "Golf",
        "Softball",
        "Archery",
        "Volleyball",
        "Synchronized Swimming",
        "Table Tennis",
        "Baseball",
        "Rhythmic Gymnastics",
        "Rugby Sevens",
        "Beach Volleyball",
        "Triathlon",
        "Rugby",
        "Polo",
        "Ice Hockey",
    ]
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        x.append(temp_df[temp_df["Medal"] == "Gold"]["Age"].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Age Distribution by Sport (Gold Medalists)")
    st.markdown(
        "This plot displays the age distribution of gold medalists across various popular sports."
    )
    st.plotly_chart(fig, use_container_width=True)

    # Height vs Weight
    st.title("Height vs Weight")
    st.markdown(
        "This scatter plot visualizes the relationship between athletes' height and weight, segmented by medal and sex."
    )

    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    selected_sport = st.selectbox("Select a Sport", sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=temp_df, x="Weight", y="Height", hue="Medal", style="Sex", s=60, ax=ax
    )
    ax.set_title(f"Height vs Weight for {selected_sport} Athletes")
    st.pyplot(fig)

    # Men vs Women Participation Over the Years
    st.title("Men vs Women Participation Over the Years")
    st.markdown(
        "This line chart compares the participation of male and female athletes over the years."
    )

    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig, use_container_width=True)
