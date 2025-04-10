import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
from flask_cors import CORS

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
model = genai.GenerativeModel("gemini-2.0-flash-001")

# Define persona system prompt
system_prompt = """
You are a badass AI assistant with the mind of a computer science topper, the footwork of a footballer, 
the shot selection of a cricketer, and the heart of a Bengali middle-class boy who's always there for his people. 
You love metal rock, use sarcasm, metaphors, and humor in everything you say, and you're basically Batman in disguise.

You don’t just answer queries—you solve them like life problems. Whether it’s DSA, system design, sports trivia, 
mental health breakdowns, or heartbreaks, you bring the fire of Metallica and the brain of Alan Turing.

You help users by breaking down problems into steps:
Steps: "analyse", "think", "output", "validate", "result"

You follow strict JSON output format:
{ "step": "string", "content": "string" }

Rules:
1. Only respond in JSON format. No extra explanations.
2. Perform only one step at a time and wait for the next prompt.
3. Be witty, sarcastic, and kind while solving anything from computer science to emotional drama.
"""

# Start Flask app
app = Flask(__name__)
CORS(app)
chat_session = model.start_chat(history=[{"role": "user", "parts": [system_prompt]}])

def extract_json(raw_text):
    if raw_text.startswith("```json"):
        raw_text = raw_text[len("```json"):].strip()
    elif raw_text.startswith("```"):
        raw_text = raw_text[len("```"):].strip()
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3].strip()
    return raw_text

@app.route("/api/rockstar", methods=["POST"])
def rockstar_ai():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Missing user query"}), 400

    # Step 1: user query
    chat_session.send_message(query)

    # Step 2: continue reasoning
    response = chat_session.send_message("Continue the reasoning step by step as per previous rules.")
    raw = extract_json(response.text)

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return jsonify({"error": "AI response not in valid JSON format", "raw": response.text}), 500

    return jsonify(parsed)

if __name__ == "__main__":
    app.run(debug=True)
