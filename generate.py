"""Bygger Googles lokala lagerfil för butiken Mobilcenter från webbutikens produktfeed.

Lagret i Quickbutik är samma som i butiken, så lagerstatusen i feeden
(in stock / out of stock) används rakt av med butikens butikskod.

Webbreor på exakt 25 % gäller bara online. För de produkterna anges
ordinarie pris som butikspris; övriga produkter lämnas utan pris så att
Google använder samma pris som i webbutiken.
"""

import urllib.request
import xml.etree.ElementTree as ET

FEED_URL = "https://mobilcenter.nu/gshopping.xml"
STORE_CODE = "Mobilcenter Jönköping AB"  # Butikskoden i Google Företagsprofil
OUTPUT = "lokalt-lager.tsv"
G = "{http://base.google.com/ns/1.0}"
ONLINE_ONLY_DISCOUNT = 0.25


def amount(text):
    """"249.00 SEK" -> 249.0"""
    return float(text.split()[0]) if text else None


def store_price(item):
    """Ordinarie pris om produkten har webbrea på 25 %, annars tomt."""
    price = amount(item.findtext(f"{G}price"))
    sale_price = amount(item.findtext(f"{G}sale_price"))
    if price and sale_price and abs(sale_price - price * (1 - ONLINE_ONLY_DISCOUNT)) < 0.5:
        return f"{price:.2f} SEK"
    return ""


def main():
    request = urllib.request.Request(FEED_URL, headers={"User-Agent": "lokalt-lager"})
    with urllib.request.urlopen(request, timeout=120) as response:
        root = ET.fromstring(response.read())

    rows = []
    for item in root.iter("item"):
        product_id = (item.findtext(f"{G}id") or "").strip()
        availability = (item.findtext(f"{G}availability") or "").strip().replace(" ", "_")
        if product_id and availability in ("in_stock", "out_of_stock"):
            rows.append((STORE_CODE, product_id, availability, store_price(item)))

    if len(rows) < 100:
        raise SystemExit(f"Bara {len(rows)} produkter i feeden, skriver inte över lagerfilen")

    with open(OUTPUT, "w", encoding="utf-8", newline="") as out:
        out.write("store_code\tid\tavailability\tprice\n")
        for row in rows:
            out.write("\t".join(row) + "\n")
    print(f"{len(rows)} produkter skrivna till {OUTPUT}")


if __name__ == "__main__":
    main()
