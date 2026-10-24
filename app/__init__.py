import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from app.extensions import db

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Konfigurasi Database dari .env
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # ==========================================
    # MODEL DATABASE (5 Tabel Saling Berelasi)
    # ==========================================
    class User(db.Model):
        __tablename__ = "users"
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        bio = db.Column(db.String(255), default="")
        level = db.Column(db.Integer, default=1)
        total_xp = db.Column(db.Integer, default=0)

        # Relasi
        thoughts = db.relationship("Thought", backref="user", lazy=True, cascade="all, delete-orphan")
        quests = db.relationship("Quest", backref="user", lazy=True, cascade="all, delete-orphan")
        badges = db.relationship("Badge", backref="user", lazy=True, cascade="all, delete-orphan")
        profile = db.relationship("Profile", backref="user", uselist=False, cascade="all, delete-orphan")

    class Profile(db.Model):
        __tablename__ = "profiles"
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
        title = db.Column(db.String(100), default="Pemula")
        streak_days = db.Column(db.Integer, default=1)

    class Thought(db.Model):
        __tablename__ = "thoughts"
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
        title = db.Column(db.String(200), nullable=False)
        notes = db.Column(db.Text, default="")
        status = db.Column(db.String(50), default="active")

    class Quest(db.Model):
        __tablename__ = "quests"
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
        thought_id = db.Column(db.Integer, db.ForeignKey("thoughts.id"), nullable=True)
        title = db.Column(db.String(200), nullable=False)
        difficulty = db.Column(db.String(50), default="Easy")
        xp_reward = db.Column(db.Integer, default=50)
        is_completed = db.Column(db.Boolean, default=False)

    class Badge(db.Model):
        __tablename__ = "badges"
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
        name = db.Column(db.String(100), nullable=False)
        description = db.Column(db.String(255), default="")

    # Sinkronisasi pembuatan tabel di Supabase
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print("Catatan sinkronisasi database:", e)

    # ==========================================
    # REST API ROUTES
    # ==========================================

    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "status": "success",
            "message": "Selamat datang di API ADHD RPG Backend!"
        }), 200

    @app.route("/db-check", methods=["GET"])
    def check_db():
        try:
            db.session.execute(db.select(1))
            return jsonify({"status": "success", "database": "Terhubung ke Supabase!"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    # 1. USERS: GET & POST
    @app.route("/users", methods=["GET", "POST"])
    def handle_users():
        if request.method == "POST":
            data = request.get_json() or {}
            if not data.get("username") or not data.get("email"):
                return jsonify({"error": "Field username dan email wajib diisi"}), 400

            new_user = User(
                username=data.get("username"),
                email=data.get("email"),
                bio=data.get("bio", "")
            )
            db.session.add(new_user)
            db.session.commit()

            profile = Profile(user_id=new_user.id)
            db.session.add(profile)
            db.session.commit()

            return jsonify({
                "message": "User baru berhasil dibuat!",
                "data": {
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email,
                    "level": new_user.level,
                    "total_xp": new_user.total_xp
                }
            }), 201

        users = User.query.all()
        result = [
            {"id": u.id, "username": u.username, "level": u.level, "total_xp": u.total_xp}
            for u in users
        ]
        return jsonify({"status": "success", "data": result}), 200

    # 2. PROFILE: GET /users/<id>
    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_profile(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User tidak ditemukan"}), 404
        return jsonify({
            "status": "success",
            "data": {
                "id": user.id,
                "username": user.username,
                "level": user.level,
                "total_xp": user.total_xp,
                "title": user.profile.title if user.profile else "Pemula"
            }
        }), 200

    # 3. THOUGHTS: GET, POST, & DELETE
    @app.route("/thoughts", methods=["GET", "POST"])
    def handle_thoughts():
        if request.method == "POST":
            data = request.get_json() or {}
            if not data.get("title") or not data.get("user_id"):
                return jsonify({"error": "Field title dan user_id wajib diisi"}), 400

            new_thought = Thought(
                user_id=data.get("user_id"),
                title=data.get("title"),
                notes=data.get("notes", "")
            )
            db.session.add(new_thought)
            db.session.commit()

            return jsonify({
                "message": "Thought berhasil dicatat!",
                "data": {
                    "id": new_thought.id,
                    "user_id": new_thought.user_id,
                    "title": new_thought.title
                }
            }), 201

        thoughts = Thought.query.all()
        result = [
            {"id": t.id, "user_id": t.user_id, "title": t.title, "notes": t.notes, "status": t.status}
            for t in thoughts
        ]
        return jsonify({"status": "success", "data": result}), 200

    @app.route("/thoughts/<int:thought_id>", methods=["DELETE"])
    def delete_thought(thought_id):
        thought = Thought.query.get(thought_id)
        if not thought:
            return jsonify({"error": "Thought tidak ditemukan"}), 404
        db.session.delete(thought)
        db.session.commit()
        return jsonify({"status": "success", "message": "Thought berhasil dihapus!"}), 200

    # 4. QUESTS: GET, POST, & PUT
    @app.route("/quests", methods=["GET", "POST"])
    def handle_quests():
        if request.method == "POST":
            data = request.get_json() or {}
            difficulty = data.get("difficulty", "Easy")
            
            # Hitung XP reward berdasarkan tingkat kesulitan
            rewards = {"Easy": 50, "Medium": 100, "Hard": 200}
            xp = rewards.get(difficulty, 50)

            new_quest = Quest(
                user_id=data.get("user_id", 1),
                thought_id=data.get("thought_id"),
                title=data.get("title", "Misi Baru"),
                difficulty=difficulty,
                xp_reward=xp
            )
            db.session.add(new_quest)
            db.session.commit()

            return jsonify({
                "message": "Quest berhasil ditambahkan!",
                "data": {
                    "id": new_quest.id,
                    "title": new_quest.title,
                    "difficulty": new_quest.difficulty,
                    "xp_reward": new_quest.xp_reward
                }
            }), 201

        quests = Quest.query.all()
        result = [
            {"id": q.id, "title": q.title, "difficulty": q.difficulty, "is_completed": q.is_completed}
            for q in quests
        ]
        return jsonify({"status": "success", "data": result}), 200

    @app.route("/quests/<int:quest_id>", methods=["PUT"])
    def complete_quest(quest_id):
        quest = Quest.query.get(quest_id)
        if not quest:
            return jsonify({"error": "Quest tidak ditemukan"}), 404

        quest.is_completed = True
        
        # Tambah XP & Update Level Otomatis
        user = User.query.get(quest.user_id)
        if user:
            user.total_xp += quest.xp_reward
            user.level = 1 + (user.total_xp // 100)

        db.session.commit()
        return jsonify({
            "message": "Quest selesai! XP berhasil ditambahkan.",
            "data": {
                "quest_id": quest.id,
                "is_completed": quest.is_completed,
                "user_level": user.level if user else 1,
                "user_total_xp": user.total_xp if user else 0
            }
        }), 200

    return app