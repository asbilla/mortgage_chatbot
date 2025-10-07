from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# 🔧 Customize this with your service info
SERVICE_INFO = """
We are ABC Tech Solutions.
We provide:
- Web development (WordPress, eCommerce, custom apps)
- SEO and digital marketing
- Cloud hosting and maintenance
Contact: support@abctech.com
"""

def ask_ollama(prompt):
    """Send prompt to Ollama (local AI model)"""
    cmd = ["ollama", "run", "llama3", prompt]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    full_prompt = f"You are a helpful assistant for ABC Tech. Use this info:\n{SERVICE_INFO}\n\nUser: {user_input}\nAssistant:"
    response = ask_ollama(full_prompt)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)