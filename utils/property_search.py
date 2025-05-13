# utils/property_search.py

import pandas as pd

# e.g. load your CSV once
DF = pd.read_csv("data/properties.csv")  

def find_properties(ctx):
    df = DF
    df = df[df.location == ctx["location"]]
    df = df[df.property_type == ctx["property_type"]]
    df = df[df.bedrooms == ctx["bedrooms"]]
    if ctx["bathrooms"]:
        df = df[df.bathrooms.astype(int) == int(ctx["bathrooms"])]
    df = df[df.price <= ctx["price"]]

    if ctx["amenities"]:
        df['amenities'] = df['amenities'].astype(str)
        for amen in ctx["amenities"]:
            df = df[df.amenities.str.contains(amen, case=False)]

    return df.to_dict(orient="records")