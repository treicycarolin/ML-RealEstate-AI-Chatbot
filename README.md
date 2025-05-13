
# 🏡 RealEstateBot — AI-Powered Real Estate Assistant

**Live App:** [https://rechatbot.streamlit.app/](https://rechatbot.streamlit.app/)

---

## 📋 What It Does

RealEstateBot is an intelligent real estate assistant built with **Streamlit**, **ChatterBot**, and **spaCy**. It interacts with users to collect key preferences for a property search (e.g., location, price, bedrooms) and guides the conversation naturally using AI.

---

## 🚀 How to Use It

1. Open the app: [https://rechatbot.streamlit.app/](https://rechatbot.streamlit.app/)
2. Type your query or preferences in the chat box, like:
   - *“I’m looking for a villa in Punta Cana.”*
   - *“My budget is around $300,000.”*
3. The bot will ask for missing details until it has everything it needs to perform a property search.
4. After completing one search session, the context resets for a new conversation.

---

## 🧠 What the Bot Understands

The chatbot recognizes and extracts the following property search fields:

- **Location** (e.g., Punta Cana, Santo Domingo)
- **Price** (e.g., 250000, $300,000)
- **Property Type** (e.g., house, condo, villa, apartment)
- **Bedrooms** (e.g., 3 bedrooms)
- **Bathrooms** (e.g., 2 bathrooms)
- **Amenities** (e.g., pool, garden, parking)

---

## 💬 Example Test Conversations

Here are a few test cases your professor can try directly in the app:

---

### ✅ Test Case 1: Full Query at Once

**You:**  
> I want a 3-bedroom house in Santo Domingo with 2 bathrooms and a garden. Budget is $200,000.

**Bot:**  
> Great! I've got all your preferences. Let me show you some options...

---

### ✅ Test Case 2: Progressive Dialogue

**You:**  
> I'm looking for a villa in Cap Cana.  
**Bot:**  
> Got it. What's your budget for the property?  
**You:**  
> Around 350,000 dollars.  
**Bot:**  
> How many bedrooms would you like?  
**You:**  
> 4 bedrooms, 3 bathrooms.  
**Bot:**  
> Any specific amenities you need?  
**You:**  
> A pool and parking.  
**Bot:**  
> Great! I have everything needed to find your ideal property.

---

### ✅ Test Case 3: Only Budget First

**You:**  
> I can spend $250,000.  
**Bot:**  
> Got it. What location are you interested in?

---

## 🛠️ Technical Stack

- **Streamlit** – Web UI framework
- **ChatterBot** – Conversational AI engine
- **spaCy** – Natural language processing
- **Python** – Core language
- **Session state** – Used to track context and conversation history

---

## 👩‍💻 Developed By

**Treicy Herrera**  
Master’s student in AI | Tech Project Manager | [LinkedIn](#)
