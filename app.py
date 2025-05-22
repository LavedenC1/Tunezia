import os
import bleach
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def detect_xss(value: str) -> bool:
    """
    Use Bleach to clean the input. If the cleaned version differs from the input,
    we assume there's potentially unsafe content.
    """
    cleaned = bleach.clean(value, tags=[], attributes={}, strip=True)
    return cleaned != value.strip()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/paa")
def paa():
    return render_template("paa.html")

@app.route("/bor")
def bor():
    return render_template("bor.html")

@app.route("/map")
def map_page():
    return render_template("map.html")

@app.route("/pics")
def pics_pg():
    return render_template("pictures.html")

@app.route("/messages")
def messages_pg():
    return render_template("messages.html")

@app.route("/history")
def history_pg():
    return render_template("history.html")

@app.route("/recv_msg", methods=["POST"])
def receive_message():
    data = request.get_json() or {}
    country = data.get("country", "").strip()
    message = data.get("message", "").strip()
    
    if detect_xss(country) or detect_xss(message):
        return "XSS detected", 400

    if country.lower() == "tunezia":
        return "Reserved", 403
    if country.lower() == "developer":
        return "Lol nice try", 403
    if country.lower() == "tunezia-isthebest!!":
        country = "Tunezia"
    if country.lower() == "developer-iamthomas":
        country = "Developer"
    
    file_path = "messages.txt"
    try:
        with open(file_path, "a") as f:
            f.write(f"{country}\n{message}\n\n")
    except Exception as e:
        return f"Error saving message: {str(e)}", 500

    return "", 200

@app.route("/get_msgs")
def get_messages():
    messages = []
    file_path = "messages.txt"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                content = f.read().strip()
            if content:
                entries = content.split("\n\n")
                for entry in entries:
                    lines = entry.strip().split("\n")
                    if len(lines) >= 2:
                        messages.append({"country": lines[0], "message": lines[1]})
        except Exception as e:
            return jsonify({"error": "Error reading messages", "details": str(e)}), 500
    return jsonify(messages)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="7675")