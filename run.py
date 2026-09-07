from flask import Flask, jsonify

from database import check_database_connection
from app.routes.ask_routes import ask_bp
from app.routes.multiple_routes import multiple_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(ask_bp)
    app.register_blueprint(multiple_bp)

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "AI Case Study API is running"
        })

    return app


if __name__ == "__main__":
    check_database_connection()

    app = create_app()

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )