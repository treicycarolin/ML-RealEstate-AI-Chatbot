# chatbot/chatter.py
import os
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from utils.property_search import find_properties
from utils.helpers import get_valid_locations 

# Fallback if __file__ is not defined (e.g. in Jupyter)
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    current_dir = os.getcwd()

db_path = os.path.join(current_dir, "memory.sqlite3")

# Initialize chatbot with memory and logic adapters
chatbot = ChatBot(
    "RealEstateBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri=f"sqlite:///{db_path}",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        "chatterbot.logic.SpecificResponseAdapter"
    ],
    read_only=False
)

# --- Training Logic ---
def train_chatterbot():
    # General small talk
    corpus_trainer = ChatterBotCorpusTrainer(chatbot)
    corpus_trainer.train("chatterbot.corpus.english.greetings")

    # Custom real estate FAQs
    faqs = [
        "What is a villa?",
        "A villa is a large and luxurious country house.",
        "What is a condo?",
        "A condo is an apartment that is individually owned.",
        "How can I buy property in the Dominican Republic?",
        "To buy property, you'll need a lawyer and a signed purchase agreement.",
        "Do I need a visa to buy a home?",
        "No, foreigners can buy property in the Dominican Republic without a visa.",
        "What is the average cost of a home in Punta Cana?",
        "It depends on the area, but homes can range from $100,000 to over $1 million.",
        "Is financing available?",
        "Yes, some developers and banks offer financing options."
    ]

    list_trainer = ListTrainer(chatbot)
    list_trainer.train(faqs)

# --- Helper to format listings into a human-readable string ---
def format_listings(listings):
    lines = []
    for prop in listings:
        amen_str = ''
        amenities = prop.get('amenities')
        if isinstance(amenities, str):
            # Convert comma-separated string to a list
            amenities = [a.strip() for a in amenities.split(',')]
        if amenities:
            amen_str = f" (amenities: {', '.join(amenities)})"
        lines.append(
            f"• {prop['bedrooms']}-bd {prop['property_type']} in {prop['location']} for ${prop['price']:,}{amen_str}"
        )
    return "\n".join(lines)

# --- Get ChatterBot Response ---
def get_chatter_response(user_input):
    response = chatbot.get_response(user_input)
    return str(response)

# --- Custom Follow-Up Prompt and Search ---
def generate_followup_prompt(extracted_entities, full_context=None):
    # Use the full accumulated context if provided
    ctx = full_context or {}

    # Prompt for missing information based on accumulated context
    if not ctx.get("location"):
        return "Can you tell me which area or city you’re interested in?"
    if not ctx.get("price"):
        return "What is your budget range?"
    if not ctx.get("property_type"):
        return "Are you looking for a villa, apartment, condo, or something else?"
    if not ctx.get("bedrooms"):
        return "How many bedrooms would you like?"
    if not ctx.get("bathrooms"):
        return "How many bathrooms do you need?"

     # Validate location
    valid_locations = get_valid_locations()
    location = ctx.get("location")
    if location not in valid_locations:
        return f"Sorry, we currently don’t support listings in {location}. Please choose a location in the Dominican Republic like Punta Cana or Cap Cana."

    # Proceed to search if all fields are present and valid
    if full_context is not None:
        listings = find_properties(full_context)
        if not listings:
            return "Sorry, I couldn't find any matching properties. Would you like to adjust your criteria?"
        reply = "Great news! I’ve found some perfect matches for you:\n"
        reply += format_listings(listings[:5])
        return reply

    return "Great! Let me find some properties that match your request."
