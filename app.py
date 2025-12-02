from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_KEY = os.getenv("PINATA_SECRET_KEY")

PINATA_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    files = {
        "file": (file.filename, file.stream, file.mimetype)
    }

    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_KEY,
    }

    response = requests.post(PINATA_URL, files=files, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Upload failed", "details": response.text}), 500

    data = response.json()
    cid = data["IpfsHash"]

    return jsonify({
        "cid": cid,
        "url": f"https://gateway.pinata.cloud/ipfs/{cid}"
    })


@app.route("/", methods=["GET"])
def home():
    return {"message": "IPFS Backend Running Successfully 🚀"}


if __name__ == "__main__":
    app.run(debug=True)
