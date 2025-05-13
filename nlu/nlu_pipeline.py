import spacy

# Load your trained model
# Adjust this path if you named the model folder differently
# nlp = spacy.load("nlu/spacy_ner_model")
nlp = spacy.load("nlu/beta_test_model")

# Entity keys you expect (based on training)
def extract_entities(user_input):
    doc = nlp(user_input)
    entities = {
        "location": None,
        "price": None,
        "property_type": None,
        "bedrooms": None,
        "bathrooms": None,
        "amenities": []
    }

    for ent in doc.ents:
        label = ent.label_.lower()
        text = ent.text.strip()

        if label == "location":
            entities["location"] = text
        elif label == "price":
            try:
                entities["price"] = int(text.replace("$", "").replace(",", ""))
            except ValueError:
                entities["price"] = text  # fallback to string
        elif label == "property_type":
            entities["property_type"] = text.lower()
        elif label == "bedrooms":
            entities["bedrooms"] = text
        elif label == "bathrooms":
            entities["bathrooms"] = text
        elif label == "amenity":
            entities["amenities"].append(text.lower())

    # If no amenities were found, return None instead of empty list
    if not entities["amenities"]:
        entities["amenities"] = None

    return entities
