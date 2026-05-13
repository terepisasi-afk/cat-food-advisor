from flask import Flask
from flask_login import LoginManager
from models import db
from config import config
from dotenv import load_dotenv
import os

load_dotenv()


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа'

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))

    return app


app = create_app('development')

from routes import *
from api import api_bp

if 'api' not in app.blueprints:
    app.register_blueprint(api_bp)


def init_database():
    with app.app_context():
        from models import Food
        db.create_all()

        if Food.query.count() == 0:
            foods = [
                Food(name="Royal Canin Urinary S/O", brand="Royal Canin",
                     stone_type="struvite", ph_effect="acidifying",
                     calcium_percent=0.6, phosphorus_percent=0.5, magnesium_percent=0.05,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=True,
                     description="Растворение струвитов, низкий уровень магния",
                     price_rating=3, allergens=""),

                Food(name="Hills Prescription Diet c/d Multicare", brand="Hills",
                     stone_type="struvite", ph_effect="acidifying",
                     calcium_percent=0.7, phosphorus_percent=0.6, magnesium_percent=0.06,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=True,
                     description="Профилактика струвитов и оксалатов",
                     price_rating=3, allergens=""),

                Food(name="Royal Canin Urinary S/O Moderate Calorie", brand="Royal Canin",
                     stone_type="oxalate", ph_effect="neutral",
                     calcium_percent=0.5, phosphorus_percent=0.4, magnesium_percent=0.07,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=False,
                     description="Оксалатные камни, контроль веса",
                     price_rating=3, allergens=""),

                Food(name="Hills Prescription Diet k/d", brand="Hills",
                     stone_type="oxalate", ph_effect="alkalizing",
                     calcium_percent=0.4, phosphorus_percent=0.3, magnesium_percent=0.05,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=True,
                     description="ХПН + оксалаты",
                     price_rating=3, allergens=""),

                Food(name="Farmina Vet Life Struvite", brand="Farmina",
                     stone_type="struvite", ph_effect="acidifying",
                     calcium_percent=0.6, phosphorus_percent=0.5, magnesium_percent=0.05,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=False,
                     description="Струвиты, профилактика",
                     price_rating=2, allergens=""),

                Food(name="Monge Vetsolution Urinary", brand="Monge",
                     stone_type="struvite", ph_effect="acidifying",
                     calcium_percent=0.55, phosphorus_percent=0.45, magnesium_percent=0.05,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=False,
                     description="Диссолюция струвитов",
                     price_rating=2, allergens=""),

                Food(name="Brit Care Cat Urinary", brand="Brit",
                     stone_type="oxalate", ph_effect="neutral",
                     calcium_percent=0.45, phosphorus_percent=0.4, magnesium_percent=0.08,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=False,
                     description="Оксалаты, поддержка мочевыводящих путей",
                     price_rating=2, allergens=""),

                Food(name="Grandorf Urinary", brand="Grandorf",
                     stone_type="both", ph_effect="neutral",
                     calcium_percent=0.5, phosphorus_percent=0.45, magnesium_percent=0.06,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=True,
                     description="Смешанный тип кристаллов",
                     price_rating=2, allergens=""),

                Food(name="Sanabelle Urinary", brand="Sanabelle",
                     stone_type="struvite", ph_effect="acidifying",
                     calcium_percent=0.6, phosphorus_percent=0.5, magnesium_percent=0.05,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=False,
                     description="Профилактика МКБ",
                     price_rating=1, allergens=""),

                Food(name="Академия при мочекаменной болезни МКБ Struvit", brand="Ветдиета",
                     stone_type="struvite", ph_effect="acidifying",
                     calcium_percent=0.95, phosphorus_percent=0.8, magnesium_percent=0.08,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=True,
                     description="Растворение струвитных камней",
                     price_rating=1, allergens=""),

                Food(name="Farmina Vet Life Struvite Management", brand="Farmina",
                     stone_type="struvite", ph_effect="acidifying",
                     calcium_percent=0.85, phosphorus_percent=0.7, magnesium_percent=0.06,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=False,
                     description="Рецидивы МКБ, идиопатический цистит",
                     price_rating=2, allergens=""),

                Food(name="AJO Vet Dieta Struvite", brand="AJO",
                     stone_type="struvite", ph_effect="acidifying",
                     calcium_percent=0.68, phosphorus_percent=0.45, magnesium_percent=0.06,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=False,
                     description="Струвитный тип МКБ",
                     price_rating=2, allergens=""),

                Food(name="Best Dinner Vet Profi Urinary", brand="Best Dinner",
                     stone_type="struvite", ph_effect="acidifying",
                     calcium_percent=0.7, phosphorus_percent=0.6, magnesium_percent=0.06,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=False,
                     description="Метионин+цистеин 1.25%, натрий 0.4%",
                     price_rating=1, allergens=""),

                Food(name="ZILLII Urinary", brand="ZILLII",
                     stone_type="struvite", ph_effect="acidifying",
                     calcium_percent=1.25, phosphorus_percent=1.05, magnesium_percent=0.07,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=False,
                     description="Профилактика МКБ. Гипоаллергенный",
                     price_rating=2, allergens="кукуруза"),

                Food(name="Royal Canin Urinary S/O Oxalate", brand="Royal Canin",
                     stone_type="oxalate", ph_effect="neutral",
                     calcium_percent=0.5, phosphorus_percent=0.4, magnesium_percent=0.05,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=False,
                     description="Профилактика оксалатных камней",
                     price_rating=3, allergens=""),

                Food(name="Hills Prescription Diet c/d Multicare Oxalate", brand="Hills",
                     stone_type="oxalate", ph_effect="neutral",
                     calcium_percent=0.6, phosphorus_percent=0.5, magnesium_percent=0.06,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=True,
                     description="Профилактика оксалатных камней. Низкое содержание кальция",
                     price_rating=3, allergens=""),

                Food(name="Monge VetSolution Urinary Oxalate Cat", brand="Monge",
                     stone_type="oxalate", ph_effect="alkalizing",
                     calcium_percent=0.55, phosphorus_percent=0.45, magnesium_percent=0.06,
                     suitable_for_kitten=False, suitable_for_adult=True, suitable_for_senior=False,
                     description="Профилактика оксалатных камней",
                     price_rating=3, allergens="курица"),
            ]
            db.session.add_all(foods)
            db.session.commit()
            print(f"✅ База данных инициализирована с {len(foods)} кормами")
        else:
            print(f"📊 В базе уже есть {Food.query.count()} кормов")


if __name__ == '__main__':
    init_database()
    print("\n" + "=" * 50)
    print("🐱 CatFoodAdvisor запущен!")
    print("=" * 50)
    print("📍 http://127.0.0.1:5000")
    print("=" * 50 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)