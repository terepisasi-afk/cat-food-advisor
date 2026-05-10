from app import app
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Food, Recommendation
from auth import register_user, authenticate_user
from food_algorithm import FoodAdvisor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = register_user(
            request.form['username'],
            request.form['email'],
            request.form['password']
        )
        if user:
            flash('Регистрация успешна!', 'success')
            return redirect(url_for('login'))
        flash('Ошибка регистрации', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = authenticate_user(request.form['email'], request.form['password'])
        if user:
            login_user(user)
            return redirect(url_for('index'))
        flash('Неверный email или пароль', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/recommend', methods=['GET', 'POST'])
@login_required
def recommend():
    if request.method == 'POST':
        all_foods = Food.query.all()
        recommendations = FoodAdvisor.recommend(
            all_foods,
            stone_type=request.form['stone_type'],
            age_years=int(request.form['age_years']),
            weight_kg=float(request.form['weight_kg']),
            has_crf='has_crf' in request.form,
            has_arthritis='has_arthritis' in request.form
        )
        return render_template('result.html', recommendations=recommendations)
    return render_template('recommend.html')

@app.route('/profile')
@login_required
def profile():
    history = Recommendation.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', history=history)