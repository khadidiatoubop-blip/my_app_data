import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
from database import save_to_db

# ------------ SCRAPING FUNCTION --------------
def scrape_category(url_base, pages):
    all_data = []

    for page in range(1, pages + 1):
        url = f"{url_base}?page={page}"
        res = requests.get(url)
        soup = bs(res.content, "html.parser")

        containers = soup.find_all("div", class_="col s6 m4 l3")

        for container in containers:
            try:
                name = container.find("p", "ad__card-description").text
                price = container.find("p", "ad__card-price").text.replace("CFA", "").replace(" ", "")
                location = container.find("p", "ad__card-location").text.replace("location_on", "").strip()
                img_link = container.find("img", "ad__card-img")["src"]

                all_data.append({
                    "name": name,
                    "price": price,
                    "location": location,
                    "image_url": img_link
                })
            except:
                pass

    df = pd.DataFrame(all_data)
    return df


# ------------ CLEANING FUNCTION --------------
def clean_price(df):
    df["price"] = df["price"].replace("Prixsurdemande", np.nan)

    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    df["price"].fillna(df["price"].median(), inplace=True)

    df["price"] = df["price"].astype("int64")

    return df


# ------------ SINGLE CATEGORY SCRAPING --------------
def run_scraping(cat, pages):

    categories = {
        "chien": "https://sn.coinafrique.com/categorie/chiens",
        "mouton": "https://sn.coinafrique.com/categorie/moutons",
        "volaille": "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
        "autre": "https://sn.coinafrique.com/categorie/autres-animaux"
    }

    url = categories[cat]

    df = scrape_category(url, pages)

    df = clean_price(df)

    save_to_db(df, cat)

    return True
