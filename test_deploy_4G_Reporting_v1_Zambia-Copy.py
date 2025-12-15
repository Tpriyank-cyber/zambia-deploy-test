# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 12:17:20 2025

@author: tpriyank
"""

import os
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

# ===================== PAGE CONFIG =====================
favicon = "favicon.png"
st.set_page_config(
    page_title="LTE Data Processing Application",
    page_icon=favicon,
    layout="wide"
)

background_text_color = "#001135"
background_header_text_color = "#a235b6"

# ===================== SIDEBAR =====================
with st.sidebar:
    selected = option_menu(
        menu_title="Region Name",
        options=["About", "Tool", "Contact Us"],
        icons=["person", "slack", "telephone"],
        menu_icon=None,
        styles={
            "menu-title": {"color": "#660a93", "font-weight": "bold", "text-align": "center"},
            "nav-link": {
                "color": "#61206d",
                "font-size": "16px",
                "font-weight": "bold",
            },
            "nav-link-selected": {
                "background-color": "#a235b6",
                "color": "white"
            },
        },
    )

# ===================== KPI LIST =====================
KPI_Obj = [
    'Cell Avail excl BLU',
    'Total E-UTRAN RRC conn stp SR',
    'E-UTRAN E-RAB stp SR',
    'E-RAB DR RAN',
    'E-UTRAN Avg PRB usage per TTI DL',
    'Average CQI',
    'Avg RRC conn UE',
    'Avg IP thp DL QCI9',
    'Total LTE data volume, DL + UL',
    'Avg UE distance',
    'Intra eNB HO SR',
    'E-UTRAN Intra-Freq HO SR',
    'E-UTRAN Inter-Freq HO SR'
]

# ===================== COMMON FUNCTIONS =====================
def safe_kpis(df):
    """Return only KPIs available in file"""
    available = [k for k in KPI_Obj if k in df.columns]
    df[available] = df[available].apply(pd.to_numeric, errors='coerce')
    return available

def read_file():
    uploaded_file = st.file_uploader("Upload LTE KPI File", type=["xlsx", "xls"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()
        df['Period start time'] = pd.to_datetime(df['Period start time'], errors='coerce')
        df["Date"] = df["Period start time"].dt.date
        df["Hour"] = df["Period start time"].dt.hour
        return df
    return None

# ===================== ABOUT =====================
if selected == "About":
    st.markdown(
        f"<h3 style='color:{background_text_color};'>Tool Introduction</h3>",
        unsafe_allow_html=True
    )
    st.write(
        "This LTE Data Processing tool automates Day and Hour level KPI aggregation "
        "for Cell and PLMN views, enabling faster OSS-based performance analysis."
    )

    st.markdown(
        f"<h3 style='color:{background_text_color};'>Key Capabilities</h3>",
        unsafe_allow_html=True
    )
    st.write(
        "- Day / Hour KPI aggregation\n"
        "- Cell & PLMN level analysis\n"
        "- Automated KPI validation\n"
        "- Streamlit-based interactive UI"
    )

# ===================== TOOL =====================
if selected == "Tool":
    st.title("LTE Data Processing Application")
    st.write("**Developed By Priyank Tomar**")

    df = read_file()

    if df is not None:
        available_kpis = safe_kpis(df)
        unique_dates = df['Date'].nunique()

        sheet_type = st.selectbox(
            "Select Sheet Type",
            ["BBH (Cell Day)", "Continue (Hour / Day)"]
        )

        # -------- DAY CELL LEVEL --------
        if sheet_type == "BBH (Cell Day)" and "LNCEL name" in df.columns:
            pivot = pd.pivot_table(
                df,
                index=['MRBTS name', 'LNCEL name'],
                columns='Date',
                values=available_kpis,
                aggfunc='sum'
            )
            st.success("Day Cell Level KPI Generated")
            st.dataframe(pivot)

        # -------- CONTINUE MODE --------
        elif sheet_type == "Continue (Hour / Day)" and "LNCEL name" in df.columns:
            if unique_dates == 1:
                pivot = pd.pivot_table(
                    df,
                    index=['MRBTS name', 'LNCEL name'],
                    columns=['Date', 'Hour'],
                    values=available_kpis,
                    aggfunc='sum'
                )
                st.success("Hour Cell Level KPI Generated")
                st.dataframe(pivot)
            else:
                hour = st.number_input("Select Hour", 0, 23)
                df_h = df[df["Hour"] == hour]

                pivot = pd.pivot_table(
                    df_h,
                    index=['MRBTS name', 'LNCEL name'],
                    columns='Date',
                    values=available_kpis,
                    aggfunc='sum'
                )
                st.success(f"Hour {hour} KPI Generated")
                st.dataframe(pivot)
        else:
            st.error("Invalid file structure or missing mandatory columns.")

# ===================== CONTACT US =====================
if selected == "Contact Us":
    st.markdown(
        f"<h3 style='color:{background_header_text_color};'>Need Help?</h3>",
        unsafe_allow_html=True
    )
    st.write(
        "**Developer:** Priyank Tomar  \n"
        "**Domain:** LTE / OSS / KPI Automation  \n"
        "**Email:** priyank.tomar@nokia.com"
    )

# ===================== HIDE STREAMLIT BRANDING =====================
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
