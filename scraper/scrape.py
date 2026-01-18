import requests
from bs4 import BeautifulSoup
import json
import hashlib
import os

URL = "https://www.gamersberg.com/blox-fruits/stock"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape():
    res = requests.get(URL, headers=HEADERS, timeout=15)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    normal, mirage = [], []

    for ul in soup.find_all("ul"):
        text = ul.get_text(" ", strip=True).lower()
        items = [li.text.strip() for li in ul.find_all("li")]

        if any(x in text for x in ["rocket", "spin", "ice"]):
            normal = items
        if any(x in text for x in ["dough", "dragon", "kitsune"]):
            mirage = items

    if not normal and not mirage:
        raise Exception("No stock found")

    return {
        "normal": normal,
        "mirage": mirage
    }

def main():
    stock = scrape()

    if os.path.exists("stock.json"):
        old = json.load(open("stock.json"))
        if stock == old:
            print("No change")
            return

    with open("stock.json", "w") as f:
        json.dump(stock, f, indent=2)

    print("Stock updated")

if __name__ == "__main__":
    main()

