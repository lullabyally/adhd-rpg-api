from datetime import datetime
from app.extensions import db

# ==========================================
# 1. TABEL USERS
# ==========================================
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    level = db.Column(db.Integer, default=1)
    total_xp = db.Column(db.Integer, default=0)
    quests_completed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi ke tabel lain
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    thoughts = db.relationship('Thought', backref='user', lazy=True, cascade="all, delete-orphan")
    quests = db.relationship('Quest', backref='user', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "level": self.level,
            "total_xp": self.total_xp,
            "quests_completed": self.quests_completed,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

# ==========================================
# 2. TABEL USER_PROFILES
# ==========================================
class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "profile_id": self.profile_id,
            "user_id": self.user_id,
            "bio": self.bio,
            "avatar_url": self.avatar_url
        }

# ==========================================
# 3. TABEL CATEGORIES
# ==========================================
class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), default='#FFFFFF')

    thoughts = db.relationship('Thought', backref='category', lazy=True)
    quests = db.relationship('Quest', backref='category', lazy=True)

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "name": self.name,
            "color": self.color
        }

# ==========================================
# 4. TABEL THOUGHTS (Brain Dump)
# ==========================================
class Thought(db.Model):
    __tablename__ = 'thoughts'

    thought_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    is_converted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    quests = db.relationship('Quest', backref='thought', lazy=True)

    def to_dict(self):
        return {
            "thought_id": self.thought_id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "title": self.title,
            "notes": self.notes,
            "is_converted": self.is_converted,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

# ==========================================
# 5. TABEL QUESTS
# ==========================================
class Quest(db.Model):
    __tablename__ = 'quests'

    quest_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=True)
    thought_id = db.Column(db.Integer, db.ForeignKey('thoughts.thought_id'), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    difficulty = db.Column(db.String(20), default='Easy')  # Easy, Medium, Hard
    xp_reward = db.Column(db.Integer, default=50)
    status = db.Column(db.String(20), default='pending')   # pending, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "quest_id": self.quest_id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "thought_id": self.thought_id,
            "title": self.title,
            "difficulty": self.difficulty,
            "xp_reward": self.xp_reward,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

# ==========================================
# 6. TABEL BADGES & USER_BADGES (Bonus / Nilai Tambah)
# ==========================================
class Badge(db.Model):
    __tablename__ = 'badges'

    badge_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            "badge_id": self.badge_id,
            "name": self.name,
            "description": self.description
        }

class UserBadge(db.Model):
    __tablename__ = 'user_badges'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.badge_id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "badge_id": self.badge_id,
            "earned_at": self.earned_at.isoformat() if self.earned_at else None
        }