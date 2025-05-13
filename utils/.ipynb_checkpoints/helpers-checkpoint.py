import re
import pandas as pd

NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
}

def get_valid_locations():
    df = pd.read_csv("data/properties.csv")
    return set(df["location"].dropna().str.strip().unique())

def normalize_entities(entities: dict) -> dict:
    norm = {}

    # --- PRICE ---
    price = entities.get("price")
    if isinstance(price, int):
        norm["price"] = price
    elif isinstance(price, str):
        # strip dollar/comma, then try int
        cleaned = price.replace("$", "").replace(",", "").strip()
        try:
            norm["price"] = int(cleaned)
        except ValueError:
            norm["price"] = None
    else:
        norm["price"] = None

    # --- LOCATION ---
    loc = entities.get("location")
    norm["location"] = loc.strip().title() if isinstance(loc, str) else None

    # --- PROPERTY_TYPE ---
    pt = entities.get("property_type")
    norm["property_type"] = pt.strip().lower() if isinstance(pt, str) else None

    # --- BEDROOMS & BATHROOMS (digit or word or hyphen-form) ---
    def parse_number_field(val):
        if isinstance(val, int):
            return val
        if isinstance(val, str):
            # look for digits
            m = re.search(r"(\d+)", val)
            if m:
                return int(m.group(1))
            # look for word
            w = val.strip().lower()
            if w in NUMBER_WORDS:
                return NUMBER_WORDS[w]
        return None

    norm["bedrooms"] = parse_number_field(entities.get("bedrooms"))
    norm["bathrooms"] = parse_number_field(entities.get("bathrooms"))

    # --- AMENITIES (preserve list or comma-string) ---
    amen = entities.get("amenities") or entities.get("amenity")
    if isinstance(amen, list):
        norm["amenities"] = amen
    elif isinstance(amen, str):
        # split on commas
        pieces = [x.strip().lower() for x in amen.split(",") if x.strip()]
        norm["amenities"] = pieces or None
    else:
        norm["amenities"] = None

    return norm
