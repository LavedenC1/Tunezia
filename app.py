import os
import nh3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def detect_xss(value: str) -> bool:
    """
    Use nh3 to clean the input. Allowed_tags is empty so any tag is removed.
    If the cleaned version differs from the original, disallowed tags were present.
    """
    cleaned = nh3.clean(value, tags=nh3.ALLOWED_TAGS - nh3.ALLOWED_TAGS)
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
    picture_dir = os.path.join(app.static_folder, "media", "pictures")
    pictures = []
    if os.path.exists(picture_dir):
        for filename in os.listdir(picture_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                description = filename.split(".")[0]
                pictures.append({
                    "url": f"/static/media/pictures/{filename}",
                    "description": description
                })
    return render_template("pictures.html", pictures=pictures)

@app.route("/messages")
def messages_pg():
    return render_template("messages.html")

@app.route("/government")
def govt_pg():
    return render_template("govt.html")

@app.route("/history")
def history_pg():
    return render_template("history.html")

@app.route("/recv_msg", methods=["POST"])
def receive_message():
    data = request.get_json() or {}
    country = data.get("country", "").strip()
    message = data.get("message", "").strip()
    
    # Use nh3-based XSS check; disallow any HTML tags
    if detect_xss(country) or detect_xss(message):
        return "XSS detected", 400

    if country.lower() == "tunezia":
        return "Reserved", 403
    if country.lower() == "magnavector":
        return "Reserved", 403
    if country.lower() == "developer":
        return "Lol nice try", 403
    if country.lower() == "tunezia-isthebest!!":
        country = "Tunezia"
    if country.lower() == "developer-iamthomas":
        country = "Developer"
    if country.lower() == "magvect-visviv":
        country = "Magnavector"
    
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