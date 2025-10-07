from flask import Flask, request, jsonify

app = Flask(__name__)

# ✅ Home route for browser testing
@app.route('/')
def home():
    return "✅ Mortgage Chatbot API is running. Use POST /chat to send messages."


# ✅ Chat route for the chatbot widget
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    reply = ask_ollama(user_message)
    return jsonify({"reply": reply})


# ✅ Simple business-specific chatbot logic (no Ollama, no API key)
def ask_ollama(prompt):
    """Simple local chatbot logic for free hosting."""
    prompt = prompt.lower()

    if "home" in prompt or "mortgage" in prompt:
        return "We help clients find the best home loan and mortgage options across Brisbane and nearby suburbs."
    elif "car" in prompt:
        return "We offer tailored car and vehicle finance for personal and business needs."
    elif "refinance" in prompt:
        return "We assist clients with refinancing their existing loans to access better rates or release equity."
    elif "investment" in prompt:
        return "We specialise in investment property loans for new and experienced investors."
    elif "commercial" in prompt:
        return "We provide expert finance solutions for commercial properties and vehicles across Queensland."
    elif "hello" in prompt or "hi" in prompt:
        return "Hello! I'm your Brisbane mortgage and finance assistant. How can I help you today?"
    else:
        return (
            "We are your local mortgage and finance specialists in Brisbane, Queensland. "
            "We offer home loans, car loans, refinancing, investment property finance, "
            "and commercial property and vehicle loans. How can I assist you today?"
        )


# ✅ Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
