import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="SSBB Project Dashboard",
    page_icon="📊",
    layout="wide"
)

# ----------------------------
# AUTO REFRESH EVERY 60 SEC
# ----------------------------
st_autorefresh(interval=60000, key="refresh")

# ----------------------------
# FILE DETAILS
# ----------------------------
EXCEL_FILE = "SSBB Tracking system updated(1).xlsx"
SHEET_NAME = "SSBB Batch 1&2 Tracking"

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ----------------------------
# HEADER
# ----------------------------
col1, col2 = st.columns([8, 1])

with col1:
    st.title("📊 SSBB PROJECT DASHBOARD")

with col2:
    if st.button("🔄 Sync"):
        st.cache_data.clear()
        st.rerun()

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("Filters")

# Function to safely create filters
def filter_column(column_name):
    if column_name in df.columns:
        values = sorted(df[column_name].dropna().unique())
        return st.sidebar.multiselect(column_name, values, default=values)
    return []

batch = filter_column("Batch")
department = filter_column("Department")
participant = filter_column("Participant's Name")

filtered = df.copy()

if "Batch" in df.columns:
    filtered = filtered[filtered["Batch"].isin(batch)]

if "Department" in df.columns:
    filtered = filtered[filtered["Department"].isin(department)]

if "Participant's Name" in df.columns:
    filtered = filtered[filtered["Participant's Name"].isin(participant)]

# ----------------------------
# KPI CARDS
# ----------------------------
total_projects = len(filtered)

participants = (
    filtered["Participant's Name"].nunique()
    if "Participant's Name" in filtered.columns
    else 0
)

departments = (
    filtered["Department"].nunique()
    if "Department" in filtered.columns
    else 0
)

ars = 0

for col in filtered.columns:
    if "ARS" in col.upper():
        ars = pd.to_numeric(filtered[col], errors="coerce").fillna(0).sum()
        break

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Projects", total_projects)
k2.metric("Participants", participants)
k3.metric("Departments", departments)
k4.metric("Total ARS", round(ars, 2))

st.divider()

# ----------------------------
# DEPARTMENT WISE ARS
# ----------------------------
st.subheader("Department-wise ARS")

ars_column = None

for col in filtered.columns:
    if "ARS" in col.upper():
        ars_column = col
        break

if ars_column and "Department" in filtered.columns:

    chart = (
        filtered.groupby("Department")[ars_column]
        .sum()
        .reset_index()
        .sort_values(ars_column, ascending=False)
    )

    fig = px.bar(
        chart,
        x="Department",
        y=ars_column,
        color=ars_column,
        title="Department-wise ARS"
    )

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# DATA TABLE
# ----------------------------
st.subheader("Project Details")

st.dataframe(filtered, use_container_width=True)

# ----------------------------
# DOWNLOAD
# ----------------------------
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "Filtered_Data.csv",
    "text/csv"
)