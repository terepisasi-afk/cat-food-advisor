from flask import Flask
from flask_login import LoginManager
from models import db
from config import config
from dotenv import load_dotenv

load_dotenv()


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))

    from api import api_bp
    app.register_blueprint(api_bp)

    from routes import *

    return app


def init_database(app):
    with app.app_context():
        from models import Food
        db.create_all()

        if Food.query.count() == 0:
            foods = [
                Food(name="Urinary S/O", brand="Royal Canin",
                     stone_type="struvite", ph_effect="acidifying",
                     calcium_percent=0.6, phosphorus_percent=0.5, magnesium_percent=0.05,
                     suitable_for_adult=True, suitable_for_senior=True,
                     description="Специализированный корм для растворения струвитов", price_rating=3),
                Food(name="Oxalate Urinary", brand="Hill's",
                     stone_type="oxalate", ph_effect="alkalizing",
                     calcium_percent=0.7, phosphorus_percent=0.6, magnesium_percent=0.07,
                     suitable_for_adult=True, suitable_for_senior=True,
                     description="Для кошек с оксалатными камнями", price_rating=3),
            ]
            db.session.add_all(foods)
            db.session.commit()
            print("База данных инициализирована")


app = create_app('development')

if __name__ == '__main__':
    init_database(app)
    app.run(debug=True, host='0.0.0.0', port=5000)