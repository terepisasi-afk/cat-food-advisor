from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db, Food, Recommendation # noqa
from food_algorithm import FoodAdvisor

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'CatFoodAdvisor API работает',
        'version': '1.0.0'
    })


@api_bp.route('/foods', methods=['GET'])
def get_foods():
    query = Food.query

    stone_type = request.args.get('stone_type')
    if stone_type:
        query = query.filter(Food.stone_type.in_([stone_type, 'both']))

    brand = request.args.get('brand')
    if brand:
        query = query.filter(Food.brand.ilike(f'%{brand}%'))

    foods = query.all()
    return jsonify([f.to_dict() for f in foods])


@api_bp.route('/foods/<int:food_id>', methods=['GET'])
def get_food(food_id):
    food = Food.query.get_or_404(food_id)
    return jsonify(food.to_dict())


@api_bp.route('/recommend', methods=['POST'])
@login_required
def api_recommend():
    data = request.get_json()

    required_fields = ['stone_type', 'age_years', 'weight_kg']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    valid_stone_types = ['struvite', 'oxalate']
    if data['stone_type'] not in valid_stone_types:
        return jsonify({'error': f'Invalid stone_type. Must be one of {valid_stone_types}'}), 400

    all_foods = Food.query.all()
    recommendations = FoodAdvisor.recommend(
        all_foods,
        stone_type=data['stone_type'],
        age_years=data['age_years'],
        weight_kg=data['weight_kg'],
        has_crf=data.get('has_crf', False),
        has_arthritis=data.get('has_arthritis', False),
        user_allergens=data.get('user_allergens', '')
    )

    result = []
    for rec in recommendations:
        result.append({
            'food': rec['food'].to_dict(),
            'score': rec['score'],
            'reasons': rec['reasons']
        })

    return jsonify({
        'success': True,
        'recommendations': result,
        'count': len(result)
    })


@api_bp.route('/history', methods=['GET'])
@login_required
def get_history():
    history = Recommendation.query.filter_by(user_id=current_user.id) \
        .order_by(Recommendation.created_at.desc()).all()

    return jsonify([{
        'id': h.id,
        'food_name': h.food.name,
        'food_brand': h.food.brand,
        'stone_type': h.stone_type,
        'cat_age': h.cat_age_years,
        'cat_weight': h.cat_weight_kg,
        'created_at': h.created_at.isoformat(),
        'allergens': h.allergens_input
    } for h in history])


@api_bp.route('/stats', methods=['GET'])
def get_stats():
    total_foods = Food.query.count()
    by_stone_type = {}

    for stone in ['struvite', 'oxalate', 'both']:
        count = Food.query.filter(Food.stone_type == stone).count()
        if count > 0:
            by_stone_type[stone] = count

    return jsonify({
        'total_foods': total_foods,
        'by_stone_type': by_stone_type,
        'brands': list(set(f.brand for f in Food.query.all()))
    })
