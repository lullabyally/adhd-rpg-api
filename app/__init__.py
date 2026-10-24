import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db

# Memuat variabel dari file .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Konfigurasi Database dari .env
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Hubungkan SQLAlchemy dengan app Flask
    db.init_app(app)

    # Endpoint Health Check Sederhana
    @app.route("/", methods=["GET"])
    def index():
        return {
            "status": "success",
            "message": "Selamat datang di API Flask & Supabase!"
        }, 200

    @app.route("/db-check", methods=["GET"])
    def check_db():
        try:
            # Mencoba query sederhana ke Supabase
            db.session.execute(db.select(1))
            return {"status": "success", "database": "Terhubung ke Supabase!"}, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500

    return app