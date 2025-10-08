from flask import Flask, request, jsonify
from flask_cors import CORS  # 👈 add this

app = Flask(__name__)
CORS(app)  # 👈 add this line (enables requests from your website)

# Load Q&A from JSON file
def load_responses():
    json_path = os.path.join(os.path.dirname(__file__), 'responses.json')
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            return json.load(f)
    return {}

responses = load_responses()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get('message', '').strip().lower()

    # Find best match
    for key, reply in responses.items():
        if key in user_msg:
            return jsonify({"reply": reply})
    
    return jsonify({"reply": "Sorry, I don't have an answer for that yet."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
