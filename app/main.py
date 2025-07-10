from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import uuid
import os

app = Flask(__name__)
es = Elasticsearch(os.getenv("ELASTIC_URL", "http://elasticsearch:9200"))

@app.route("/catalog", methods=["POST"])
def add_item():
    data = request.json
    data["id"] = str(uuid.uuid4())
    es.index(index="catalog", id=data["id"], document=data)
    print(f"EVENT: catalog.item_created -> {data['id']}")
    return jsonify({"message": "Item added", "item": data}), 201

@app.route("/catalog", methods=["GET"])
def search():
    query = request.args.get("q", "")
    response = es.search(index="catalog", query={"multi_match": {"query": query, "fields": ["title", "description"]}})
    results = [hit["_source"] for hit in response["hits"]["hits"]]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
