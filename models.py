"""
Модели базы данных (ORM)
Определяют структуру таблиц и связи между ними
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


# noinspection PyDeprecation
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    recommendations = db.relationship('Recommendation', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'


class Food(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)

    stone_type = db.Column(db.String(50))
    ph_effect = db.Column(db.String(50))

    calcium_percent = db.Column(db.Float)
    phosphorus_percent = db.Column(db.Float)
    magnesium_percent = db.Column(db.Float)

    target_ph_min = db.Column(db.Float)
    target_ph_max = db.Column(db.Float)

    suitable_for_kitten = db.Column(db.Boolean, default=True)
    suitable_for_adult = db.Column(db.Boolean, default=True)
    suitable_for_senior = db.Column(db.Boolean, default=True)

    indications = db.Column(db.Text)
    contraindications = db.Column(db.Text)
    description = db.Column(db.Text)
    price_rating = db.Column(db.Integer, default=2)

    def to_dict(self):
        """Преобразование в словарь для API"""
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'stone_type': self.stone_type,
            'ph_effect': self.ph_effect,
            'description': self.description,
            'price_rating': self.price_rating,
            'calcium_percent': self.calcium_percent,
            'phosphorus_percent': self.phosphorus_percent,
            'magnesium_percent': self.magnesium_percent
        }


class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)

    cat_age_years = db.Column(db.Integer)
    cat_weight_kg = db.Column(db.Float)
    stone_type = db.Column(db.String(50))
    has_crf = db.Column(db.Boolean, default=False)
    has_arthritis = db.Column(db.Boolean, default=False)

    # noinspection PyDeprecation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    food = db.relationship('Food')

    user = db.relationship('User', backref='recommendations')
    def __repr__(self):
        return f'<Recommendation for user {self.user_id} at {self.created_at}>'
