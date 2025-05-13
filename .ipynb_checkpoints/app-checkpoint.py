# app.py

from chatbot.chatter import get_chatter_response, train_chatterbot, generate_followup_prompt
from nlu.nlu_pipeline import extract_entities
from utils.helpers import normalize_entities

# Fields we need for a property search
REQUIRED_FIELDS = ["location", "price", "property_type", "bedrooms", "bathrooms", "amenities"]

# Known values for fallback
KNOWN_LOCATIONS = [
    "Punta Cana", "Bavaro", "Santo Domingo", "Casa de Campo", "Jarabacoa",
    "Santiago", "Cap Cana", "La Romana", "Baváro"
]
KNOWN_PROPERTY_TYPES = ["house", "condo", "apartment", "villa"]

# Uncomment to re-train
# train_chatterbot()

print("RealEstateBot is running! (type 'exit' to quit)")

# Persistent context across turns
context = {field: None for field in REQUIRED_FIELDS}

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Goodbye!")
        break

    # Step 1: Extract and normalize entities
    raw_entities = extract_entities(user_input)
    normalized = normalize_entities(raw_entities)

    # Fallback: Treat direct number input as price
    stripped = user_input.strip().replace(",", "").lstrip("$")
    if stripped.isdigit() and normalized.get("price") is None:
        normalized["price"] = int(stripped)

    # Fallback: Location only
    if normalized.get("location") is None:
        candidate_loc = user_input.strip().title()
        if candidate_loc in KNOWN_LOCATIONS:
            normalized["location"] = candidate_loc

    # Fallback: Property type only
    if normalized.get("property_type") is None:
        candidate_pt = user_input.strip().lower()
        if candidate_pt in KNOWN_PROPERTY_TYPES:
            normalized["property_type"] = candidate_pt

    # Update context
    for key, value in normalized.items():
        if value is not None:
            context[key] = value

    # Debug: show current state
    print(f"Current context: {context}")

    # Check if we need to ask for more info or perform search
    missing = [field for field, val in context.items() if val is None]

    # Either prompt or perform the search + show results
    followup = generate_followup_prompt(normalized, full_context=context)
    print(f"Bot: {followup}")

    # If we completed a search (i.e., nothing is missing), reset for next query
    if not missing:
        context = {field: None for field in REQUIRED_FIELDS}
