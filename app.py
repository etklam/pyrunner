from flask import Flask, jsonify, request
from datetime import datetime
from public_house.scraper import HousingAllocationScraper

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the API"})


@app.route("/items", methods=["GET"])
def get_items():
    items = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]
    return jsonify(items)


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = {"id": item_id, "name": f"Item {item_id}"}
    return jsonify(item)


@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    item = {"id": len(data) + 1, "name": data.get("name")}
    return jsonify(item), 201


@app.route("/public-house", methods=["GET"])
def get_public_house():
    scraper = HousingAllocationScraper()
    result = scraper.crawl()
    if result:
        result["fetch_date"] = result["fetch_date"].isoformat()
        return jsonify(result)
    return jsonify({"error": "Failed to fetch data"}), 500


if __name__ == "__main__":
    app.run(debug=True)
