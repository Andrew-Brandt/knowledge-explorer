import json
import time

import logging
from flask import Blueprint, request, jsonify
from app.content_retrieval import (
    get_article_text,
    get_article_summary,
    get_article_links,
    get_learning_path,
    get_canonical_topic,
    regenerate_learning_path
)

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)

VALID_LEVELS = ["basic", "intermediate", "advanced"]

'''
@main.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    ...
'''

@main.route("/summary/<topic>", methods=["GET"])
def get_summary_route(topic):
    level = request.args.get("level", "basic").lower()
    if level not in VALID_LEVELS:
        return jsonify({"error": "Invalid level."}), 400

    canonical_topic = get_canonical_topic(topic)
    if not canonical_topic:
        return jsonify({"error": f"Could not resolve topic '{topic}'"}), 404

    summary = get_article_summary(canonical_topic, level)

    if summary:
        return jsonify({"topic": canonical_topic, "level": level, "summary": summary})
    logger.error(f"Failed to retrieve summary for '{canonical_topic}' at level '{level}'")
    return jsonify({"error": f"Failed to retrieve summary for '{canonical_topic}'"}), 500

@main.route("/learning-path/<topic>", methods=["GET"])
def retrieve_learning_path(topic):
    level = request.args.get("level", "basic").lower()
    if level not in VALID_LEVELS:
        return jsonify({"error": "Invalid level."}), 400

    canonical_topic = get_canonical_topic(topic)
    if not canonical_topic:
        return jsonify({"error": f"Could not resolve topic '{topic}'"}), 404

    summary = get_article_summary(canonical_topic, level)
    learning_path = get_learning_path(canonical_topic, level)

    if learning_path:
        return jsonify({
            "topic": canonical_topic,
            "level": level,
            "summary": summary,
            "links": learning_path
        })

    logger.error(f"Failed to retrieve learning path for '{canonical_topic}'")
    return jsonify({"error": f"Failed to retrieve learning path for '{canonical_topic}'"}), 500

@main.route("/rerank-learning-path/<topic>", methods=["POST"])
def rerank_learning_path(topic):
    canonical_topic = get_canonical_topic(topic)
    if not canonical_topic:
        return jsonify({"error": f"Could not resolve topic '{topic}'"}), 404

    ranked_links = regenerate_learning_path(canonical_topic)
    if not ranked_links:
        return jsonify({"error": "Failed to generate learning path"}), 500

    summary = get_article_summary(canonical_topic, level="basic")

    logger.info(f"Learning path regenerated and stored for topic '{canonical_topic}'")

    return jsonify({
        "topic": canonical_topic,
        "summary": summary,
        "links": ranked_links
    })

