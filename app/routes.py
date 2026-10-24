from datetime import datetime
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User, UserProfile, Category, Thought, Quest

# Inisialisasi Blueprint API
api_bp = Blueprint('api', __name__, url_prefix='/api')

# ===================================================
# 1. ENDPOINTS: USERS & PROFILE (CRUD)
# ===================================================

# [POST] Tambah User Baru
@api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if not data.get('username') or not data.get('email'):
        return jsonify({"status": "error", "message": "Username dan email wajib diisi!"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"status": "error", "message": "Username sudah terdaftar!"}), 400

    new_user = User(
        username=data['username'],
        email=data['email']
    )
    db.session.add(new_user)
    db.session.commit()

    # Buat profil default
    new_profile = UserProfile(user_id=new_user.user_id, bio=data.get('bio', 'Petualang baru di ADHD RPG'))
    db.session.add(new_profile)
    db.session.commit()

    return jsonify({"status": "success", "message": "User berhasil dibuat", "data": new_user.to_dict()}), 201

# [GET] Ambil Semua User
@api_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify({"status": "success", "data": [u.to_dict() for u in users]}), 200

# [GET] getProfile() - Ambil Profil & Statistik User Tertentu
@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    profile_data = user.to_dict()
    profile_data['bio'] = user.profile.bio if user.profile else None
    return jsonify({"status": "success", "data": profile_data}), 200

# [PUT] Update Profil User
@api_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    if user.profile and 'bio' in data:
        user.profile.bio = data['bio']

    db.session.commit()
    return jsonify({"status": "success", "message": "Data user diperbarui", "data": user.to_dict()}), 200

# [DELETE] Hapus User
@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"status": "success", "message": f"User dengan ID {user_id} berhasil dihapus"}), 200

# ===================================================
# 2. ENDPOINTS: CATEGORIES
# ===================================================

# [POST] Tambah Kategori
@api_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({"status": "error", "message": "Nama kategori wajib diisi!"}), 400

    category = Category(name=data['name'], color=data.get('color', '#3498db'))
    db.session.add(category)
    db.session.commit()
    return jsonify({"status": "success", "data": category.to_dict()}), 201

# [GET] Ambil Semua Kategori
@api_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify({"status": "success", "data": [c.to_dict() for c in categories]}), 200

# ===================================================
# 3. ENDPOINTS: THOUGHTS / BRAIN DUMP (CRUD)
# ===================================================

# [POST] tambahThought() - Catat Pikiran/Ide
@api_bp.route('/thoughts', methods=['POST'])
def create_thought():
    data = request.get_json() or {}
    if not data.get('user_id') or not data.get('title'):
        return jsonify({"status": "error", "message": "user_id dan title wajib diisi!"}), 400

    thought = Thought(
        user_id=data['user_id'],
        category_id=data.get('category_id'),
        title=data['title'],
        notes=data.get('notes', '')
    )
    db.session.add(thought)
    db.session.commit()
    return jsonify({"status": "success", "message": "Thought berhasil dicatat", "data": thought.to_dict()}), 201

# [GET] getDaftarThought() - Ambil Semua Thought
@api_bp.route('/thoughts', methods=['GET'])
def get_thoughts():
    user_id = request.args.get('user_id')
    query = Thought.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    thoughts = query.all()
    return jsonify({"status": "success", "data": [t.to_dict() for t in thoughts]}), 200

# [PUT] Update Thought
@api_bp.route('/thoughts/<int:thought_id>', methods=['PUT'])
def update_thought(thought_id):
    thought = Thought.query.get_or_404(thought_id)
    data = request.get_json() or {}

    thought.title = data.get('title', thought.title)
    thought.notes = data.get('notes', thought.notes)
    thought.category_id = data.get('category_id', thought.category_id)
    db.session.commit()
    return jsonify({"status": "success", "message": "Thought diperbarui", "data": thought.to_dict()}), 200

# [DELETE] Hapus Thought
@api_bp.route('/thoughts/<int:thought_id>', methods=['DELETE'])
def delete_thought(thought_id):
    thought = Thought.query.get_or_404(thought_id)
    db.session.delete(thought)
    db.session.commit()
    return jsonify({"status": "success", "message": "Thought berhasil dihapus"}), 200

# [POST] convertToQuest() - Konversi Thought Menjadi Quest
@api_bp.route('/thoughts/<int:thought_id>/convert-to-quest', methods=['POST'])
def convert_thought_to_quest(thought_id):
    thought = Thought.query.get_or_404(thought_id)
    data = request.get_json() or {}

    difficulty = data.get('difficulty', 'Easy')
    xp_map = {'Easy': 50, 'Medium': 100, 'Hard': 200}
    xp_reward = xp_map.get(difficulty, 50)

    new_quest = Quest(
        user_id=thought.user_id,
        category_id=thought.category_id,
        thought_id=thought.thought_id,
        title=thought.title,
        difficulty=difficulty,
        xp_reward=xp_reward,
        status='pending'
    )
    thought.is_converted = True

    db.session.add(new_quest)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Thought berhasil diubah menjadi Quest!",
        "data": new_quest.to_dict()
    }), 201

# ===================================================
# 4. ENDPOINTS: QUESTS (CRUD & GAME LOGIC)
# ===================================================

# [POST] tambahQuest() - Tambah Quest Langsung
@api_bp.route('/quests', methods=['POST'])
def create_quest():
    data = request.get_json() or {}
    if not data.get('user_id') or not data.get('title'):
        return jsonify({"status": "error", "message": "user_id dan title wajib diisi!"}), 400

    difficulty = data.get('difficulty', 'Easy')
    xp_map = {'Easy': 50, 'Medium': 100, 'Hard': 200}
    xp_reward = data.get('xp_reward', xp_map.get(difficulty, 50))

    quest = Quest(
        user_id=data['user_id'],
        category_id=data.get('category_id'),
        title=data['title'],
        difficulty=difficulty,
        xp_reward=xp_reward,
        status='pending'
    )
    db.session.add(quest)
    db.session.commit()
    return jsonify({"status": "success", "data": quest.to_dict()}), 201

# [GET] getDaftarQuest() - Ambil Semua Quest
@api_bp.route('/quests', methods=['GET'])
def get_quests():
    user_id = request.args.get('user_id')
    status = request.args.get('status')

    query = Quest.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)

    quests = query.all()
    return jsonify({"status": "success", "data": [q.to_dict() for q in quests]}), 200

# [PUT] Update Quest
@api_bp.route('/quests/<int:quest_id>', methods=['PUT'])
def update_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    data = request.get_json() or {}

    quest.title = data.get('title', quest.title)
    quest.difficulty = data.get('difficulty', quest.difficulty)
    quest.category_id = data.get('category_id', quest.category_id)
    db.session.commit()
    return jsonify({"status": "success", "message": "Quest diperbarui", "data": quest.to_dict()}), 200

# [DELETE] Hapus Quest
@api_bp.route('/quests/<int:quest_id>', methods=['DELETE'])
def delete_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    db.session.delete(quest)
    db.session.commit()
    return jsonify({"status": "success", "message": "Quest berhasil dihapus"}), 200

# [PUT] selesaikanQuest() + tambahXP() + cekLevel()
@api_bp.route('/quests/<int:quest_id>/complete', methods=['PUT'])
def complete_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    if quest.status == 'completed':
        return jsonify({"status": "error", "message": "Quest ini sudah pernah diselesaikan sebelumnya!"}), 400

    quest.status = 'completed'
    quest.completed_at = datetime.utcnow()

    user = User.query.get(quest.user_id)
    user.total_xp += quest.xp_reward
    user.quests_completed += 1

    # Naik 1 level setiap kelipatan 100 XP
    user.level = 1 + (user.total_xp // 100)

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": f"Selamat! Quest '{quest.title}' selesai. Mendapatkan {quest.xp_reward} XP!",
        "quest": quest.to_dict(),
        "user_stats": {
            "user_id": user.user_id,
            "current_level": user.level,
            "total_xp": user.total_xp,
            "quests_completed": user.quests_completed
        }
    }), 200