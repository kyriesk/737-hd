from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "hd-api",
        "message": "Cloud-native Flask API is running"
    })


@app.route("/api/message", methods=["GET"])
def message():
    return jsonify({
        "message": "Hello from the Deakin GCP cloud-native application!"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
