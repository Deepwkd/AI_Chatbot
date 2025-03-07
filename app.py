import os
import json
import spacy
import requests
import streamlit as st
import google.generativeai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
from dotenv import load_dotenv

# Loading api key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Loading NLP model
nlp = spacy.load("en_core_web_sm")
STOPWORDS = nlp.Defaults.stop_words

# Loading predefined responses from JSON
def load_responses():
    with open("responses.json", "r") as file:
        return json.load(file)

responses = load_responses()

# To extract keywords from user input
def extract_keywords(user_input):
    doc = nlp(user_input.lower())
    keywords = [token.text for token in doc if token.is_alpha and token.text not in STOPWORDS]
    return " ".join(keywords)

# fetching latest phone models (Mock API)
def fetch_latest_phones():
    mock_api_data = {
        "latest_models": [
            {
                "brand": "Apple",
                "model": "iPhone 16 Pro Max",
                "release_date": "2024-09-20",
                "price": "₹1,38,300 INR",
                "processor": "A18 Pro Chip",
                "camera": "48MP Triple Camera",
                "battery": "4,500mAh"
            },
            {
                "brand": "Samsung",
                "model": "Galaxy S25 Ultra",
                "release_date": "2025-02-07",
                "price": "₹1,29,999 INR",
                "processor": "Snapdragon 8 Gen 4",
                "camera": "200MP Quad Camera",
                "battery": "5,200mAh"
            },
            {
                "brand": "OnePlus",
                "model": "OnePlus 13",
                "release_date": "2025-01-07",
                "price": "₹69,999 INR",
                "processor": "Snapdragon 8 Gen 3",
                "camera": "50MP Triple Camera",
                "battery": "5,000mAh"
            },
            {
                "brand": "Google",
                "model": "Pixel 9 Pro",
                "release_date": "2024-08-22",
                "price": "₹1,09,999 INR",
                "processor": "Google Tensor G4",
                "camera": "64MP Dual Camera",
                "battery": "4,800mAh"
            },
            {
                "brand": "Xiaomi",
                "model": "Xiaomi 15 Ultra",
                "release_date": "2025-03-11",
                "price": "₹79,999 INR",
                "processor": "Snapdragon 8 Gen 4",
                "camera": "108MP Quad Camera",
                "battery": "5,300mAh"
            }
        ]
    }

    latest_models = [
        f"**{phone['brand']} {phone['model']}**\n"
        f"   - 💰 **Price**: {phone['price']}\n"
        f"   - 🏎 **Processor**: {phone['processor']}\n"
        f"   - 📷 **Camera**: {phone['camera']}\n"
        f"   - 🔋 **Battery**: {phone['battery']}\n"
        f"   - 📅 **Release Date**: {phone['release_date']}\n"
        for phone in mock_api_data["latest_models"]
    ]

    return f"📱 **Latest Phone Models:**\n\n" + "\n".join(latest_models)

# Finding the best response using TF-IDF similarity
def get_best_response(user_input):
    extracted_keywords = extract_keywords(user_input)

    corpus = []
    categories = []

    for key, value in responses.items():
        corpus.append(" ".join(value["keywords"]))
        categories.append(key)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    user_vector = vectorizer.transform([extracted_keywords])

    similarities = (tfidf_matrix * user_vector.T).toarray().flatten()
    best_match_index = similarities.argmax()

    if similarities[best_match_index] < 0.1:
        return responses["general_ai"]["response"], False

    matched_category = categories[best_match_index]

    if "api" in responses[matched_category]:
        if responses[matched_category]["api"] == "fetch_latest_phones":
            return fetch_latest_phones(), True

    return responses[matched_category]["response"], True

# to process user input with Google Gemini AI
def process_with_gemini(user_input):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"⚠️ Error connecting to Google Gemini API: {e}"


st.set_page_config(page_title="AI Phone Chatbot")
st.header("🤖 AI-Chatbot")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("💬 **Ask a question:** ")

if st.button("Ask"):
    bot_response, matched = get_best_response(user_input)

    if not matched:
        bot_response = process_with_gemini(user_input)  # Use Google Gemini for unknown queries

    st.subheader("🤖 Bot Response:")
    st.markdown(f"**You:** {user_input}")
    st.markdown(f"**Bot:** {bot_response}")
    st.session_state['chat_history'].append(("You", user_input))
    st.session_state['chat_history'].append(("Bot", bot_response))

st.subheader("📜 Chat History")
for role, text in st.session_state['chat_history']:
    st.markdown(f"**{role}:** {text}")
