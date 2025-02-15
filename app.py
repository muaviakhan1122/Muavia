import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/shutdown', methods=['POST','GET'])
def shutdown():
    """Shuts down the system."""
    os.system("shutdown /s /t 1")
    return jsonify({"status": "System shutting down..."})

@app.route('/restart', methods=['POST','GET'])
def restart():
    """Restarts the system."""
    os.system("shutdown /r /t 1")
    return jsonify({"status": "System restarting..."})

app.route('/search_google', methods=['GET'])
@app.route('/search_google', methods=['GET'])
def search_google():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)  # Opens search in a browser
    return jsonify({"message": f"Searching Google for: {query}", "url": search_url})

@app.route('/play_youtube', methods=['GET'])
def play_youtube():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    youtube_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(youtube_url)  # Opens YouTube search in a browser
    return jsonify({"message": f"Searching YouTube for: {query}", "url": youtube_url})

if __name__ == "__main__":
    app.run(debug=True)
