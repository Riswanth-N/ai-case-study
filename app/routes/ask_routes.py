from flask import Blueprint, jsonify, request

from database import db
from app.services.openai_service import client
from datetime import datetime, timezone


ask_bp = Blueprint("ask", __name__)


@ask_bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    user_input = data.get("userInput")

    if not user_input:
        return jsonify({
            "error": "userInput is required"
        }), 400

    try:
        prompt = db.prompts.find_one({
            "_id": "Education_Prompt"
        })

        if not prompt:
            return jsonify({
                "error": "Education prompt not found"
            }), 404

        final_prompt = prompt["template"].replace(
            "{{userInput}}",
            user_input
        )

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=final_prompt
        )

        ai_response = response.output_text

        db.history.insert_one({
            "userInput": user_input,
            "response": ai_response,
            "createdAt": datetime.now(timezone.utc)
        })

        return jsonify({
            "response": ai_response
        })

    except Exception as error:
        print("Error:", error)

        return jsonify({
            "error": "Something went wrong while processing the request"
        }), 500