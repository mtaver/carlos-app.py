import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------
st.set_page_config(
    page_title="German Credit Risk Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------
# LOAD DATA
# ---------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("german_credit_data.csv")

    # Remove unnecessary index column
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    return df

df = load_data()

# ---------------------------------
# TITLE
# ---------------------------------
st.title("📊 German Credit Risk Analysis Dashboard")
st.markdown("Interactive dashboard built with Streamlit")

st.divider()

# ---------------------------------
# SIDEBAR FILTERS
# ---------------------------------
st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
    "Gender",
    options=df["Sex"].dropna().unique(),
    default=df["Sex"].dropna().unique()
)

risk = st.sidebar.multiselect(
    "Risk",
    options=df["Risk"].dropna().unique(),
    default=df["Risk"].dropna().unique()
)

housing = st.sidebar.multiselect(
    "Housing",
    options=df["Housing"].dropna().unique(),
    default=df["Housing"].dropna().unique()
)

filtered_df = df[
    (df["Sex"].isin(gender)) &
    (df["Risk"].isin(risk)) &
    (df["Housing"].isin(housing))
]

# ---------------------------------
# KPI SECTION
# ---------------------------------
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    len(filtered_df)
)

col2.metric(
    "Average Credit Amount",
    f"${filtered_df['Credit amount'].mean():,.0f}"
)

col3.metric(
    "Average Age",
    f"{filtered_df['Age'].mean():.1f}"
)

col4.metric(
    "Average Duration",
    f"{filtered_df['Duration'].mean():.1f} Months"
)

st.divider()

# ---------------------------------
# CHARTS
# ---------------------------------
left, right = st.columns(2)

with left:

    fig = px.histogram(
        filtered_df,
        x="Age",
        nbins=20,
        title="Age Distribution",
        color_discrete_sequence=["royalblue"]
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    fig = px.histogram(
        filtered_df,
        x="Credit amount",
        nbins=30,
        title="Credit Amount Distribution",
        color_discrete_sequence=["orange"]
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# ROW 2
# ---------------------------------
left, right = st.columns(2)

with left:

    fig = px.bar(
        filtered_df["Purpose"].value_counts().reset_index(),
        x="Purpose",
        y="count",
        title="Loan Purpose",
        labels={"count":"Count", "Purpose":"Purpose"}
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    fig = px.pie(
        filtered_df,
        names="Risk",
        title="Risk Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# ROW 3
# ---------------------------------
left, right = st.columns(2)

with left:

    fig = px.box(
        filtered_df,
        x="Risk",
        y="Credit amount",
        color="Risk",
        title="Credit Amount by Risk"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    fig = px.scatter(
        filtered_df,
        x="Age",
        y="Credit amount",
        color="Risk",
        size="Duration",
        hover_data=["Purpose"],
        title="Age vs Credit Amount"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# ROW 4
# ---------------------------------
left, right = st.columns(2)

with left:

    fig = px.bar(
        filtered_df.groupby("Sex")["Credit amount"].mean().reset_index(),
        x="Sex",
        y="Credit amount",
        color="Sex",
        title="Average Credit by Gender"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    fig = px.bar(
        filtered_df.groupby("Housing")["Credit amount"].mean().reset_index(),
        x="Housing",
        y="Credit amount",
        color="Housing",
        title="Average Credit by Housing"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# DATA TABLE
# ---------------------------------
st.divider()

st.subheader("Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ---------------------------------
# DOWNLOAD
# ---------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Data",
    data=csv,
    file_name="filtered_credit_data.csv",
    mime="text/csv"
)