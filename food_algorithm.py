from models import db, Food


class FoodAdvisor:

    @staticmethod
    def recommend(food_list, stone_type, age_years, weight_kg,
                  has_crf=False, has_arthritis=False, user_allergens=""):
        filtered = []

        for food in food_list:
            score = 0
            reasons = []

            if stone_type == 'struvite':
                if food.stone_type in ['struvite', 'both']:
                    if food.ph_effect == 'acidifying':
                        score += 35
                        reasons.append("✅ Подкисляющий эффект (растворяет струвиты)")
                    elif food.ph_effect == 'neutral':
                        score += 20
                        reasons.append("ℹ️ Нейтральный pH (подходит частично)")
                    else:
                        continue
                else:
                    continue

            elif stone_type == 'oxalate':
                if food.stone_type in ['oxalate', 'both']:
                    if food.ph_effect == 'alkalizing':
                        score += 35
                        reasons.append("✅ Подщелачивающий эффект (профилактика оксалатов)")
                    elif food.ph_effect == 'neutral':
                        score += 20
                        reasons.append("ℹ️ Нейтральный pH (подходит)")
                    else:
                        continue
                else:
                    continue

            if age_years < 1:
                if food.suitable_for_kitten:
                    score += 15
                    reasons.append("🐱 Подходит для котят")
                else:
                    score -= 20
                    reasons.append("⚠️ Не рекомендуется для котят")
            elif 1 <= age_years <= 7:
                if food.suitable_for_adult:
                    score += 10
            else:
                if food.suitable_for_senior:
                    score += 15
                    reasons.append("👴 Учтён возраст (пожилая кошка)")
                else:
                    score -= 10

            if stone_type == 'struvite':
                if food.magnesium_percent and food.magnesium_percent < 0.08:
                    score += 15
                    reasons.append("🔬 Пониженное содержание магния (профилактика струвитов)")
                elif food.magnesium_percent and food.magnesium_percent > 0.1:
                    score -= 10
                    reasons.append("⚠️ Повышенный магний (не рекомендуется при струвитах)")

            elif stone_type == 'oxalate':
                if food.calcium_percent and food.calcium_percent < 0.8:
                    score += 15
                    reasons.append("🔬 Пониженное содержание кальция (профилактика оксалатов)")

            if has_crf:
                if food.phosphorus_percent and food.phosphorus_percent < 0.5:
                    score += 25
                    reasons.append("🫘 Пониженный фосфор (важно при ХПН)")
                else:
                    score -= 20
                    reasons.append("⚠️ Может быть опасен при ХПН")

            if has_arthritis:
                if "сустав" in (food.indications or "").lower():
                    score += 15
                    reasons.append("🦴 Содержит компоненты для суставов")

            if user_allergens:
                allergens_list = [a.strip().lower() for a in user_allergens.split(',') if a.strip()]
                food_allergens = [a.strip().lower() for a in (food.allergens or "").split(',') if a.strip()]

                if food_allergens:
                    common = set(allergens_list) & set(food_allergens)
                    if common:
                        score -= 50
                        reasons.append(f"⚠️ Содержит аллергены: {', '.join(common)}")
                    else:
                        score += 15
                        reasons.append("✅ Не содержит указанных аллергенов")

            if weight_kg > 8:
                score -= 5
                reasons.append("⚖️ Учтён избыточный вес")

            filtered.append({
                'food': food,
                'score': score,
                'reasons': reasons[:4]
            })

        filtered.sort(key=lambda x: x['score'], reverse=True)

        result = [item for item in filtered if item['score'] >= 0][:5]

        return result if result else filtered[:3]

    @staticmethod
    def get_food_comparison(food1, food2, stone_type, age_years, has_crf=False):
        foods = [food1, food2]
        results = {}

        for food in foods:
            rec = FoodAdvisor.recommend([food], stone_type, age_years, 5, has_crf)
            if rec:
                results[food.name] = rec[0]['score']
            else:
                results[food.name] = 0

        return results