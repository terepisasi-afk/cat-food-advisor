from app import app
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Food, Recommendation
from auth import register_user, authenticate_user
from food_algorithm import FoodAdvisor


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not email or not password:
            flash('Заполните все поля', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Пароли не совпадают', 'danger')
            return render_template('register.html')

        if len(password) < 4:
            flash('Пароль должен быть не менее 4 символов', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует', 'danger')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует', 'danger')
            return render_template('register.html')

        user = register_user(username, email, password)
        if user:
            flash('Регистрация успешна! Теперь войдите', 'success')
            return redirect(url_for('login'))
        else:
            flash('Ошибка при регистрации', 'danger')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        user = authenticate_user(email, password)
        if user:
            login_user(user)
            flash(f'Добро пожаловать, {user.username}!', 'success')

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Неверный email или пароль', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))


@app.route('/recommend', methods=['GET', 'POST'])
@login_required
def recommend():
    if request.method == 'POST':
        try:
            stone_type = request.form.get('stone_type')
            age_years = float(request.form.get('age_years', 0))
            weight_kg = float(request.form.get('weight_kg', 0))
            has_crf = 'has_crf' in request.form
            has_arthritis = 'has_arthritis' in request.form
            user_allergens = ','.join(request.form.getlist('allergens'))

            if age_years <= 0 or age_years > 30:
                flash('Некорректный возраст', 'danger')
                return redirect(url_for('recommend'))
            if weight_kg <= 0 or weight_kg > 20:
                flash('Некорректный вес', 'danger')
                return redirect(url_for('recommend'))

            all_foods = Food.query.all()

            if not all_foods:
                flash('База кормов пуста. Обратитесь к администратору.', 'warning')
                return redirect(url_for('recommend'))

            recommendations = FoodAdvisor.recommend(
                all_foods, stone_type, age_years, weight_kg,
                has_crf, has_arthritis, user_allergens
            )

            if recommendations:
                top_food = recommendations[0]['food']
                rec = Recommendation(
                    user_id=current_user.id,
                    food_id=top_food.id,
                    cat_age_years=age_years,
                    cat_weight_kg=weight_kg,
                    stone_type=stone_type,
                    has_crf=has_crf,
                    has_arthritis=has_arthritis,
                    allergens_input=user_allergens
                )
                db.session.add(rec)
                db.session.commit()

            session['last_recommendations'] = {
                'stone_type': stone_type,
                'age': age_years,
                'weight': weight_kg,
                'allergens': user_allergens
            }

            return render_template('result.html',
                                   recommendations=recommendations,
                                   stone_type=stone_type,
                                   age=age_years,
                                   weight=weight_kg,
                                   allergens=user_allergens)

        except ValueError as e:
            flash(f'Ошибка в данных: {str(e)}', 'danger')
            return redirect(url_for('recommend'))
        except Exception as e:
            flash(f'Произошла ошибка: {str(e)}', 'danger')
            return redirect(url_for('recommend'))

    return render_template('recommend.html')


@app.route('/profile')
@login_required
def profile():
    history = Recommendation.query.filter_by(user_id=current_user.id) \
        .order_by(Recommendation.created_at.desc()).all()

    stats = {
        'total': len(history),
        'by_stone': {}
    }

    for rec in history:
        stone = rec.stone_type
        stats['by_stone'][stone] = stats['by_stone'].get(stone, 0) + 1

    return render_template('profile.html', history=history, stats=stats)


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500