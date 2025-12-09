import streamlit as st
from database import load_from_db, init_database
from scraper import run_scraping
import pandas as pd
import os
import base64
import matplotlib.pyplot as plt
import numpy as np


# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Init DB
init_database()
#st.markdown('<div class="main-block">', unsafe_allow_html=True)

st.title("Scraping Platform – Animals in Senegal")
st.write("Welcome to the application!")


menu = ["Scraper Data", "Download Data Web Scraper", "Dashboard", "Evaluate App"]
choice = st.sidebar.selectbox("Menu", menu)

pages = [1,2,3,4,5,6,7,8,9,10]
choice2 = st.sidebar.selectbox("Number of pages to scrape", pages)


def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp 
            {{ background-image: url("data:image/jpeg;base64,{encoded_string}"); }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.5);  /* voile noir  */
            z-index: -1;
        }}
        [data-testid="stHeader"], .stApp > header {{ background: rgba(0,0,0,0); }}
        .stApp {{ background-size: cover; background-position: center; background-attachment: fixed; }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local('images/background.jpg')

# -----------------------------------------
#          SCRAPER OPTION (MODIFIÉ)
# -----------------------------------------
if choice == "Scraper Data":
    st.header("Scrape New Data (Cleaned Automatically)")

    cat = st.selectbox("Select a category", ["chien", "mouton", "volaille", "autre"])

    if st.button("Lanch the scraping"):
        run_scraping(cat, choice2)
        st.success(f"Scraping completed for '{cat}' ({choice2} pages). Clean data saved")
        
        # Charger les données nettoyées
        df = load_from_db(cat)

        st.subheader("Scraped and cleaned data")
        st.dataframe(df)

        # ----- BOUTON DE TÉLÉCHARGEMENT -----
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=" Download as CSV",
            data=csv,
            file_name=f"{cat}_clean_data.csv",
            mime="text/csv"
        )

# -----------------------------------------
#     VIEW CLEAN DATA (inchangé)
# -----------------------------------------
elif choice == "Download Data Web Scraper":
    st.header("Raw data scraped from Web Scraper")

    # Choix de la catégorie
    cat = st.selectbox(
        "Select a category",
        ["chien", "mouton", "volaille", "autre"]
    )

    # Charger les fichiers CSV bruts selon la catégorie
    if cat == "chien":
        df = pd.read_csv('data/Chien_sitemap.csv')
    elif cat == "mouton":
        df = pd.read_csv('data/Mouton_sitemap.csv')
    elif cat == "volaille":
        df = pd.read_csv('data/volaille.csv')
    elif cat == "autre":
        df = pd.read_csv('data/autres_animaux.csv')

    # Afficher le DataFrame
    st.subheader(f"Raw data : {cat}")
    st.dataframe(df)

    # Bouton de téléchargement CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name=f"{cat}_raw_data.csv",
        mime="text/csv"
    )


# -----------------------------------------
# DASHBOARD (inchangé)
# -----------------------------------------
elif choice == "Dashboard":
    st.header("Price analysis")

    cat = st.selectbox("Select a category", ["chien", "mouton", "volaille", "autre"])
    df = load_from_db(cat)

    if df.empty:
        st.warning("Aucune donnée disponible pour cette catégorie.")
    else:
        st.subheader("Statistics")
        st.write(df["price"].describe())

        st.subheader("Histogram of price")
        st.bar_chart(df["price"])
# -----------------------------------------
# EVALUATE APP (inchangé)
# -----------------------------------------
elif choice == "Evaluate App":
    st.header("Evaluate App")

    st.subheader("Please complete one of the forms below")

    st.markdown("### Form KoboToolbox")
    st.markdown(
        "[Open the KoboToolbox form](https://ee.kobotoolbox.org/x/BlxvnMBf)",
        unsafe_allow_html=True
    )

    st.markdown("### Form Google Forms")
    st.markdown(
        "[Open the Google Form](https://docs.google.com/forms/d/1mcRk-3yzJKQP7H0gqWXzqE3zbJa7g-zEf5Jp51T-nGw/edit)",
        unsafe_allow_html=True
                                
    )
