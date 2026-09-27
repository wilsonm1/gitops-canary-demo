import os
import random

from flask import Flask, jsonify

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "v1")
FAIL_RATE = float(os.getenv("FAIL_RATE", "0"))


@app.route("/")
def index():
    if random.random() < FAIL_RATE:
        return jsonify(error="simulated failure", version=VERSION), 500
    return jsonify(message="hello from the orders service", version=VERSION)


@app.route("/healthz")
def healthz():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
