"""Bygger Googles lokala lagerfil för butiken Mobilcenter från webbutikens produktfeed.

Lagret i Quickbutik är samma som i butiken, så lagerstatusen i feeden
(in stock / out of stock) används rakt av med butikens butikskod.
"""

import urllib.request
import xml.etree.ElementTree as ET

FEED_URL = "https://mobilcenter.nu/gshopping.xml"
STORE_CODE = "Mobilcenter Jönköping AB"  # Butikskoden i Google Företagsprofil
OUTPUT = "lokalt-lager.tsv"
G = "{http://base.google.com/ns/1.0}"


def main():
    request = urllib.request.Request(FEED_URL, headers={"User-Agent": "lokalt-lager"})
    with urllib.request.urlopen(request, timeout=120) as response:
        root = ET.fromstring(response.read())

    rows = []
    for item in root.iter("item"):
        product_id = (item.findtext(f"{G}id") or "").strip()
        availability = (item.findtext(f"{G}availability") or "").strip().replace(" ", "_")
        if product_id and availability in ("in_stock", "out_of_stock"):
            rows.append((STORE_CODE, product_id, availability))

    if len(rows) < 100:
        raise SystemExit(f"Bara {len(rows)} produkter i feeden, skriver inte över lagerfilen")

    with open(OUTPUT, "w", encoding="utf-8", newline="") as out:
        out.write("store_code\tid\tavailability\n")
        for row in rows:
            out.write("\t".join(row) + "\n")
    print(f"{len(rows)} produkter skrivna till {OUTPUT}")


if __name__ == "__main__":
    main()
