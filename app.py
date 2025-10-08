from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # allow cross-origin requests from WordPress or local dev

# -------------------- Load responses from JSON --------------------
RESPONSES_FILE = os.path.join(os.path.dirname(__file__), 'responses.json')

def get_responses():
    if not os.path.exists(RESPONSES_FILE):
        return {}
    with open(RESPONSES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# -------------------- Chat endpoint --------------------
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)
        message = data.get('message', '').lower().strip()
        if not message:
            return jsonify({'reply': "Please type a message."})

        responses = get_responses()
        reply = "I'm sorry, I don't understand that yet."

        # ---- Fuzzy match for closest question ----
        questions = list(responses.keys())
        matches = difflib.get_close_matches(message, questions, n=1, cutoff=0.5)
        if matches:
            reply = responses[matches[0]]
        else:
            # ---- Keyword match fallback ----
            for q, a in responses.items():
                if any(word in message for word in q.lower().split()):
                    reply = a
                    break

        return jsonify({'reply': reply})

    except Exception as e:
        print(f"❌ Error processing message: {e}")
        return jsonify({'reply': 'Error processing your request.'}), 500

# -------------------- Health check --------------------
@app.route('/', methods=['GET'])
def index():
    return "✅ Mortgage Chatbot API is running. Use POST /chat to send messages."

# -------------------- Run server --------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
