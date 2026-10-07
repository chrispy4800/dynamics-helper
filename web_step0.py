import json
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, send_file


app = Flask(__name__)



# The instructor chooses the problem folder on the server.
PROBLEM_FOLDER = Path(
    os.environ.get("PROBLEM_FOLDER", "problem")
).resolve()

print(PROBLEM_FOLDER)

IMAGE_PATH = PROBLEM_FOLDER / "Vehicle_Image.png"
CONFIG_PATH = PROBLEM_FOLDER / "problem_config.json"


@app.get("/")
def step0():
    return render_template("step0.html")


@app.get("/api/problem")
def problem_info():
    if not IMAGE_PATH.is_file():
        return jsonify({
            "error": "Vehicle_Image.png is missing on the server."
        }), 500

    intersection = None

    if CONFIG_PATH.is_file():
        try:
            with CONFIG_PATH.open("r", encoding="utf-8") as file:
                config = json.load(file)

            intersection = config.get("quadrant_intersection")
        except (OSError, json.JSONDecodeError):
            return jsonify({
                "error": "problem_config.json could not be read."
            }), 500

    # Send only information needed to display the problem.
    # Do not expose instructor answers or private config fields.
    return jsonify({
        "image_url": "/api/vehicle-image",
        "quadrant_intersection": intersection
    })


@app.get("/api/vehicle-image")
def vehicle_image():
    if not IMAGE_PATH.is_file():
        return jsonify({"error": "Image not found."}), 404

    return send_file(IMAGE_PATH, mimetype="image/png")


if __name__ == "__main__":
    # Local development only. Use a production web server for
    # a publicly accessible deployment.
    app.run(debug=True, host="127.0.0.1", port=5000)