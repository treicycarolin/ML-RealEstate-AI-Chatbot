import streamlit as st
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

# Optional: Uncomment if you want to train the bot each time
# train_chatterbot()

st.set_page_config(page_title="Real Estate AI Chatbot", layout="centered")
st.title("🏡 Real Estate AI Chatbot")
st.markdown("Talk to the bot to search for properties. Type your preferences below.")

# Initialize session state for context and chat history
if "context" not in st.session_state:
    st.session_state.context = {field: None for field in REQUIRED_FIELDS}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input box
user_input = st.chat_input("Ask about a property...")

if user_input:
    # Add user input to chat history
    st.session_state.chat_history.append(("You", user_input))

    # Step 1: Extract and normalize entities
    raw_entities = extract_entities(user_input)
    normalized = normalize_entities(raw_entities)

    # Fallbacks
    stripped = user_input.strip().replace(",", "").lstrip("$")
    if stripped.isdigit() and normalized.get("price") is None:
        normalized["price"] = int(stripped)

    candidate_loc = user_input.strip().title()
    if normalized.get("location") is None and candidate_loc in KNOWN_LOCATIONS:
        normalized["location"] = candidate_loc

    candidate_pt = user_input.strip().lower()
    if normalized.get("property_type") is None and candidate_pt in KNOWN_PROPERTY_TYPES:
        normalized["property_type"] = candidate_pt

    # Update persistent context
    for key, value in normalized.items():
        if value is not None:
            st.session_state.context[key] = value

    # Generate bot reply
    bot_reply = generate_followup_prompt(normalized, full_context=st.session_state.context)
    st.session_state.chat_history.append(("Bot", bot_reply))

    # If all fields are collected, reset context for new search
    if all(st.session_state.context[field] is not None for field in REQUIRED_FIELDS):
        st.session_state.context = {field: None for field in REQUIRED_FIELDS}

# Display chat history
for sender, message in st.session_state.chat_history:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.markdown(message)
