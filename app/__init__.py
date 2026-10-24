import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db

# Memuat konfigurasi dari file .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Konfigurasi Database dari .env
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inisialisasi Database
    db.init_app(app)

    # Daftarkan Blueprint API dari routes.py
    from app.routes import api_bp
    app.register_blueprint(api_bp)

    # Endpoint Root & Health Check
    @app.route("/", methods=["GET"])
    def index():
        return {
            "status": "success",
            "message": "Selamat datang di API ADHD RPG Backend!",
            "endpoints": [
                "/api/users",
                "/api/categories",
                "/api/thoughts",
                "/api/quests"
            ]
        }, 200

    @app.route("/db-check", methods=["GET"])
    def check_db():
        try:
            db.session.execute(db.select(1))
            return {"status": "success", "database": "Terhubung ke Supabase!"}, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500

    return app
