class FoodAdvisor:
    @staticmethod
    def recommend(food_list, stone_type, age_years, weight_kg,
                  has_crf=False, has_arthritis=False):
        filtered = []

        for food in food_list:
            score = 0
            reasons = []

            if stone_type == 'struvite':
                if food.stone_type in ['struvite', 'both']:
                    if food.ph_effect == 'acidifying':
                        score += 35
                        reasons.append("Подкисляющий эффект (растворяет струвиты)")
                    elif food.ph_effect == 'neutral':
                        score += 20
                    else:
                        continue
                else:
                    continue

            elif stone_type == 'oxalate':
                if food.stone_type in ['oxalate', 'both']:
                    if food.ph_effect == 'alkalizing':
                        score += 35
                        reasons.append("Подщелачивающий эффект (профилактика оксалатов)")
                    elif food.ph_effect == 'neutral':
                        score += 20
                    else:
                        continue
                else:
                    continue

            if age_years < 1:
                if food.suitable_for_kitten:
                    score += 15
                else:
                    score -= 20
            elif age_years > 7:
                if food.suitable_for_senior:
                    score += 15
                    reasons.append("Учтён возраст (пожилая кошка)")

            if has_crf and food.phosphorus_percent and food.phosphorus_percent < 0.5:
                score += 25
                reasons.append("Пониженный фосфор (важно при ХПН)")

            filtered.append({
                'food': food,
                'score': score,
                'reasons': reasons[:3]
            })

        filtered.sort(key=lambda x: x['score'], reverse=True)
        return filtered[:5]