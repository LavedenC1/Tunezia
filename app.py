import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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
def hpg():
    return render_template("history.html")

@app.route("/recv_msg",methods=["POST"])
def recieve_message():
    data = request.json
    if not os.path.exists("messages.txt"):
        with open("messages.txt","w") as f:
            f.write(data['message'] + "\n")
    else:
        with open("messages.txt","a") as f:
            f.write(data["country"] + "\n" + data['message'] + "\n\n")
    return "",200

@app.route("/get_msgs")
def get_messages():
    messages = []
    if os.path.exists("messages.txt"):
        with open("messages.txt", "r") as f:
            content = f.read().strip()
        if content:
            entries = content.split("\n\n")
            for entry in entries:
                lines = entry.strip().split("\n")
                if len(lines) >= 2:
                    messages.append({"country": lines[0], "message": lines[1]})
    return jsonify(messages)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port="7675")