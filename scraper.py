
import os
import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://m3.protonmovies.top"
headers = {"User-Agent": "Mozilla/5.0"}

# Create output folder
os.makedirs("output", exist_ok=True)

# CSV setup
csv_file = open("output/movies.csv", "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Title", "Page URL", "Poster URL", "Quality", "IMDb", "Download Links"])

def scrape_home():
    print("🔄 Scraping home page...")
    res = requests.get(BASE_URL, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

    cards = soup.select(".card-body a")

    for card in cards:
        title = card.get("title", "No Title").strip()
        link = BASE_URL + card["href"]
        print(f"🎬 {title}")
        scrape_movie_detail(title, link)

def scrape_movie_detail(title, url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

    try:
        poster = soup.find("img", class_="card-img-top")["src"]
    except:
        poster = "N/A"

    # IMDb/quality details
    details = soup.find_all("li")
    imdb = quality = "N/A"
    for item in details:
        text = item.text.strip().lower()
        if "imdb" in text:
            imdb = text
        if "quality" in text:
            quality = text

    # Download buttons
    download_buttons = soup.select(".btn.btn-primary.btn-sm")
    links = [btn["href"] for btn in download_buttons]

    csv_writer.writerow([title, url, poster, quality, imdb, " | ".join(links)])

if __name__ == "__main__":
    scrape_home()
    csv_file.close()
    print("✅ Done! Data saved to output/movies.csv")
