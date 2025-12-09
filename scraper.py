import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
from database import save_to_db

# ------------ SCRAPING FUNCTION --------------
def scrape_category(url_base, pages):

    all_data = []

    # Loop through each requested page
    for page in range(1, pages + 1):
        url = f"{url_base}?page={page}"
        res = requests.get(url)
        soup = bs(res.content, "html.parser")

        # Each listing is inside this container
        containers = soup.find_all("div", class_="col s6 m4 l3")

        # Extract fields from each listing card
        for container in containers:
            try:
                name = container.find("p", "ad__card-description").text
                price = container.find("p", "ad__card-price").text.replace("CFA", "").replace(" ", "")
                location = container.find("p", "ad__card-location").text.replace("location_on", "").strip()
                img_link = container.find("img", "ad__card-img")["src"]

                # Store extracted data
                all_data.append({
                    "name": name,
                    "price": price,
                    "location": location,
                    "image_url": img_link
                })
            except:
                # If any element is missing, skip the card
                pass

    # Convert scraped records into a DataFrame
    df = pd.DataFrame(all_data)
    return df


# ------------ CLEANING FUNCTION --------------
def clean_price(df):

    # Replace "Prixsurdemande" with missing value
    df["price"] = df["price"].replace("Prixsurdemande", np.nan)

    # Convert price text to numeric (handles errors safely)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Fill missing values with the median price
    df["price"].fillna(df["price"].median(), inplace=True)

    # Ensure integer type for further analysis
    df["price"] = df["price"].astype("int64")

    return df


# ------------ SINGLE CATEGORY SCRAPING --------------
def run_scraping(cat, pages):

    # Define base URLs for each category
    categories = {
        "chien": "https://sn.coinafrique.com/categorie/chiens",
        "mouton": "https://sn.coinafrique.com/categorie/moutons",
        "volaille": "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
        "autre": "https://sn.coinafrique.com/categorie/autres-animaux"
    }

    url = categories[cat]

    # Step 1: Scrape raw data
    df = scrape_category(url, pages)

    # Step 2: Clean the price column
    df = clean_price(df)

    # Step 3: Save cleaned data to database
    save_to_db(df, cat)

    return True
