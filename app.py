from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__, template_folder="templates")

# Put your API key here
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImJiNzYwYjNlLTRhMmQtNGExNC1iMTAwLTIyNTc3ZDhiMWUwNyIsImlhdCI6MTc1MTUxODM1MSwic3ViIjoiZGV2ZWxvcGVyLzQ3MTBkOGUwLTY0ZjYtYzA2Ny0xZTI4LTQwOGU1OTA5YzQ0YiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMTAuMjI2LjIwNy4xODIiXSwidHlwZSI6ImNsaWVudCJ9XX0.XABSUOtu7-CjH5-wBdx5jaqgxoIWZDAdy3fM69t-xOAEfYZag_HAgxIMox5aNih4HJmVF19ei0bZY55YFkEyKQ"
HEADERS = {
    "Accept": "application/json",
    "authorization": f"Bearer {API_TOKEN}"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_deck', methods=['POST'])
def get_deck():
    data = request.json
    medals = int(data.get("medals"))
    url = "https://api.clashroyale.com/v1/rankings/global/players"

    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch leaderboard"}), 500

    leaderboard = response.json().get("items", [])
    for player in leaderboard:
        if player["trophies"] == medals:
            tag = player["tag"].replace("#", "%23")
            player_url = f"https://api.clashroyale.com/v1/players/{tag}"
            player_res = requests.get(player_url, headers=HEADERS)
            if player_res.status_code != 200:
                return jsonify({"error": "Failed to fetch player data"}), 500
            player_data = player_res.json()
            deck = player_data.get("currentDeck", [])
            return jsonify({"player": player["name"], "deck": deck})

    return jsonify({"message": "No player found with exact medal count"})

if __name__ == '__main__':
    app.run(debug=True)
