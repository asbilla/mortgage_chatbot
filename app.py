from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load chatbot responses
with open('responses.json') as f:
    responses = json.load(f)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '').lower()
    reply = "I'm sorry, I don't understand that."
    for q, a in responses.items():
        if q in message:
            reply = a
            break
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
