
🤖 AI Chatbot for Latest Smartphones

This is an AI-powered chatbot that provides real-time information about the latest smartphones using a mock API and Google Gemini AI.

✅ Latest phone details (price, processor, camera, battery life)

✅ Uses NLP (Natural Language Processing) for understanding queries

✅ Matches user input using TF-IDF & keyword extraction

✅ Google Gemini AI for answering complex questions

✅ Streamlit UI for an interactive chatbot experience





📌 Project Approach

1️⃣ User asks a question (e.g., "What is the latest iPhone?")

2️⃣ NLP processes the question → Extracts keywords using spaCy

3️⃣ TF-IDF similarity matching → Checks responses.json for predefined answers

4️⃣ Mock API fetches latest phone data for dynamic responses

5️⃣ Google Gemini AI handles complex queries if no match is found

6️⃣ Streamlit displays response + saves chat history


📌 Sample Interaction

User Input	Chatbot Response:

User:  "Hello"

Bot:  "Hello! How may I assist you today?"

User:  "Which phone has the best camera?"

Bot: "The best camera phones in 2025 include the iPhone 16 Pro Max, Samsung Galaxy S25 Ultra, and Google Pixel 9 Pro. They offer incredible night photography, zoom, and AI-powered enhancements."

User: "What are the latest phones?"

Bot: 📱 Latest Phone Models 

**iPhone 16 Pro Max** (₹1,38,300, A18 Pro Chip, 48MP Camera)

**Samsung Galaxy S25 Ultra** (₹1,29,999, Snapdragon 8 Gen 4, 200MP Camera)

**OnePlus 13** (₹69,999, Snapdragon 8 Gen 3, 50MP Camera)


📌 Technologies Used

🔹 Python (Backend logic)

🔹 Streamlit (UI for chatbot)

🔹 spaCy (NLP for keyword extraction)

🔹 TF-IDF (Scikit-Learn) (Matching user queries)

🔹 Google Gemini AI (Handles unknown questions)

🔹 Mock API (Simulates real-time phone data)
