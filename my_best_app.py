import streamlit as st
from database import load_from_db, init_database
from scraper import run_scraping
import pandas as pd
import os
import base64
import matplotlib.pyplot as plt
import numpy as np


# -----------------------------------------------------
# Load external CSS styles from style.css
# -----------------------------------------------------
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# -----------------------------------------------------
# Initialize database (creates tables if not existing)
# -----------------------------------------------------
init_database()

st.title("Scraping Platform – Animals in Senegal")
st.write("Welcome to the application!")


# -----------------------------------------------------
# Sidebar menu and page selection
# -----------------------------------------------------
menu = ["Scraper Data", "Download Data Web Scraper", "Dashboard", "Evaluate App"]
choice = st.sidebar.selectbox("Menu", menu)

# Sidebar: number of pages to scrape
pages = [1,2,3,4,5,6,7,8,9,10]
choice2 = st.sidebar.selectbox("Number of pages to scrape", pages)


# -----------------------------------------------------
# Background image function (encoded in Base64)
# -----------------------------------------------------
def add_bg_from_local(image_file):

    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        /* Apply the background image */
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Dark overlay effect */
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            z-index: -1;
        }}

        /* Remove default Streamlit header background */
        [data-testid="stHeader"], .stApp > header {{
            background: rgba(0,0,0,0);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply background image
add_bg_from_local('images/background.jpg')



# =====================================================
# 1) SCRAPER SECTION
# =====================================================
if choice == "Scraper Data":
    st.header("Scrape New Data (Cleaned Automatically)")

    # Select animal category
    cat = st.selectbox("Select a category", ["chien", "mouton", "volaille", "autre"])

    if st.button("Lanch the scraping"):
        # Run scraper and cleaning
        run_scraping(cat, choice2)
        st.success(f"Scraping completed for '{cat}' ({choice2} pages). Clean data saved")
        
        # Load cleaned data
        df = load_from_db(cat)

        st.subheader("Scraped and cleaned data")
        st.dataframe(df)

        # Provide download button
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"{cat}_clean_data.csv",
            mime="text/csv"
        )



# =====================================================
# 2) RAW DATA VIEW (Web Scraper files)
# =====================================================
elif choice == "Download Data Web Scraper":
    st.header("Raw data scraped from Web Scraper")

    # Choose category
    cat = st.selectbox(
        "Select a category",
        ["chien", "mouton", "volaille", "autre"]
    )

    # Load CSV files exported by WebScraper.io
    if cat == "chien":
        df = pd.read_csv('data/Chien_sitemap.csv')
    elif cat == "mouton":
        df = pd.read_csv('data/Mouton_sitemap.csv')
    elif cat == "volaille":
        df = pd.read_csv('data/volaille.csv')
    elif cat == "autre":
        df = pd.read_csv('data/autres_animaux.csv')

    st.subheader(f"Raw data : {cat}")
    st.dataframe(df)

    # Button to download raw CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name=f"{cat}_raw_data.csv",
        mime="text/csv"
    )



# =====================================================
# 3) DASHBOARD (basic statistics and charts)
# =====================================================
elif choice == "Dashboard":
    st.header("Price analysis")

    # Select animal category
    cat = st.selectbox("Select a category", ["chien", "mouton", "volaille", "autre"])
    df = load_from_db(cat)

    if df.empty:
        st.warning("No data available for this category.")
    else:
        st.subheader("Statistics")
        st.write(df["price"].describe())

        st.subheader("Histogram of price")
        st.bar_chart(df["price"])



# =====================================================
# 4) EVALUATION FORMS
# =====================================================
elif choice == "Evaluate App":
    st.header("Evaluate App")

    st.subheader("Please complete one of the forms below")

    # KoboToolbox link
    st.markdown("### Form KoboToolbox")
    st.markdown(
        "[Open the KoboToolbox form](https://ee.kobotoolbox.org/x/BlxvnMBf)",
        unsafe_allow_html=True
    )

    # Google Forms link
    st.markdown("### Form Google Forms")
    st.markdown(
        "[Open the Google Form](https://docs.google.com/forms/d/1mcRk-3yzJKQP7H0gqWXzqE3zbJa7g-zEf5Jp51T-nGw/edit)",
        unsafe_allow_html=True
    )
