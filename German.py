import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="German Credit Risk Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("german_credit_data.csv")

        # Remove index column if present
        if "Unnamed: 0" in df.columns:
            df = df.drop(columns=["Unnamed: 0"])

        return df

    except FileNotFoundError:
        st.error("❌ german_credit_data.csv not found.")
        st.stop()

    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()


df = load_data()

# ==========================================
# TITLE
# ==========================================
st.title("📊 German Credit Risk Dashboard")
st.markdown("Interactive Credit Risk Dashboard built with Streamlit")

st.divider()

# ==========================================
# SIDEBAR FILTERS
# ==========================================
st.sidebar.header("Dashboard Filters")

gender = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Sex"].dropna().unique()),
    default=sorted(df["Sex"].dropna().unique())
)

risk = st.sidebar.multiselect(
    "Risk",
    options=sorted(df["Risk"].dropna().unique()),
    default=sorted(df["Risk"].dropna().unique())
)

housing = st.sidebar.multiselect(
    "Housing",
    options=sorted(df["Housing"].dropna().unique()),
    default=sorted(df["Housing"].dropna().unique())
)

filtered_df = df[
    (df["Sex"].isin(gender))
    & (df["Risk"].isin(risk))
    & (df["Housing"].isin(housing))
]

# ==========================================
# KPI SECTION
# ==========================================
st.subheader("Key Performance Indicators")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Customers", len(filtered_df))

k2.metric(
    "Average Age",
    f"{filtered_df['Age'].mean():.1f}"
)

k3.metric(
    "Average Credit",
    f"${filtered_df['Credit amount'].mean():,.0f}"
)

k4.metric(
    "Average Duration",
    f"{filtered_df['Duration'].mean():.1f} Months"
)

st.divider()

# ==========================================
# ROW 1
# ==========================================
c1, c2 = st.columns(2)

with c1:

    fig = px.histogram(
        filtered_df,
        x="Age",
        title="Age Distribution",
        nbins=20
    )

    st.plotly_chart(fig, width="stretch")

with c2:

    fig = px.histogram(
        filtered_df,
        x="Credit amount",
        title="Credit Amount Distribution",
        nbins=25
    )

    st.plotly_chart(fig, width="stretch")

# ==========================================
# ROW 2
# ==========================================
c1, c2 = st.columns(2)

purpose_df = (
    filtered_df.groupby("Purpose")
    .size()
    .reset_index(name="Count")
)

with c1:

    fig = px.bar(
        purpose_df,
        x="Purpose",
        y="Count",
        color="Purpose",
        title="Loan Purpose"
    )

    st.plotly_chart(fig, width="stretch")

with c2:

    fig = px.pie(
        filtered_df,
        names="Risk",
        title="Risk Distribution"
    )

    st.plotly_chart(fig, width="stretch")

# ==========================================
# ROW 3
# ==========================================
c1, c2 = st.columns(2)

with c1:

    fig = px.box(
        filtered_df,
        x="Risk",
        y="Credit amount",
        color="Risk",
        title="Credit Amount by Risk"
    )

    st.plotly_chart(fig, width="stretch")

with c2:

    fig = px.scatter(
        filtered_df,
        x="Age",
        y="Credit amount",
        color="Risk",
        size="Duration",
        hover_name="Purpose",
        title="Age vs Credit Amount"
    )

    st.plotly_chart(fig, width="stretch")

# ==========================================
# ROW 4
# ==========================================
c1, c2 = st.columns(2)

gender_df = (
    filtered_df.groupby("Sex")["Credit amount"]
    .mean()
    .reset_index()
)

housing_df = (
    filtered_df.groupby("Housing")["Credit amount"]
    .mean()
    .reset_index()
)

with c1:

    fig = px.bar(
        gender_df,
        x="Sex",
        y="Credit amount",
        color="Sex",
        title="Average Credit by Gender"
    )

    st.plotly_chart(fig, width="stretch")

with c2:

    fig = px.bar(
        housing_df,
        x="Housing",
        y="Credit amount",
        color="Housing",
        title="Average Credit by Housing"
    )

    st.plotly_chart(fig, width="stretch")

# ==========================================
# SUMMARY STATISTICS
# ==========================================
st.divider()

st.subheader("Summary Statistics")

st.dataframe(
    filtered_df.describe(include="all"),
    width="stretch"
)

# ==========================================
# DATA TABLE
# ==========================================
st.subheader("Filtered Dataset")

st.dataframe(
    filtered_df,
    width="stretch"
)

# ==========================================
# DOWNLOAD BUTTON
# ==========================================
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_credit_data.csv",
    mime="text/csv"
)
