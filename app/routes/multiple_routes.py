import asyncio
from flask import Blueprint, jsonify, request

from app.services.multiple_service import process_multiple_inputs

multiple_bp = Blueprint("multiple", __name__)


@multiple_bp.route("/ask-multiple", methods=["POST"])
def ask_multiple():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    user_inputs = data.get("userInputs")

    if not user_inputs:
        return jsonify({
            "error": "userInputs is required"
        }), 400

    if not isinstance(user_inputs, list):
        return jsonify({
            "error": "userInputs must be a list"
        }), 400

    for user_input in user_inputs:
        if not isinstance(user_input, str) or not user_input.strip():
            return jsonify({
                "error": "Each item in userInputs must be a non-empty string"
            }), 400

    try:
        responses = asyncio.run(
            process_multiple_inputs(user_inputs)
        )

        return jsonify({
            "responses": responses
        })

    except Exception as error:
        print("Error:", error)

        return jsonify({
            "error": "Something went wrong while processing the requests"
        }), 500