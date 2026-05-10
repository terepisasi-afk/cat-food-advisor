from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user
from models import User, db

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def register_user(username, email, password):
    hashed = generate_password_hash(password, method='pbkdf2:sha256')
    user = User(username=username, email=email, password_hash=hashed)
    db.session.add(user)
    db.session.commit()
    return user


def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None
