from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # allow cross-origin requests from WordPress or local dev

# Global cache for responses
responses = {}
last_loaded = 0

def get_responses():
    """Load responses.json only when it changes."""
    global responses, last_loaded
    path = 'responses.json'

    if not os.path.exists(path):
        print("⚠️  responses.json not found!")
        return {}

    modified = os.path.getmtime(path)
    if modified > last_loaded:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                responses = json.load(f)
                last_loaded = modified
                print(f"✅ Loaded responses.json at {time.ctime(modified)} with {len(responses)} entries.")
        except Exception as e:
            print(f"❌ Error reading responses.json: {e}")
            responses = {}
    return responses


@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "message": "✅ Mortgage Chatbot API is running. Use POST /chat to send messages."
    })


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)
        message = data.get('message', '').lower().strip()

        if not message:
            return jsonify({'reply': "Please type a message."})

        responses = get_responses()

        # Default reply
        reply = "I'm sorry, I don't understand that yet."

        # Match by keyword (simple search)
        for q, a in responses.items():
            if q.lower() in message:
                reply = a
                break

        return jsonify({'reply': reply})

    except Exception as e:
        print(f"❌ Error processing message: {e}")
        return jsonify({'reply': 'Error processing your request.'}), 500


if __name__ == '__main__':
    import time
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Mortgage Chatbot API running on port {port}")
    app.run(host='0.0.0.0', port=port)
