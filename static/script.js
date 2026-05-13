// Дополнительный JavaScript для CatFoodAdvisor

document.addEventListener('DOMContentLoaded', function() {
    // Авто-скрытие уведомлений через 5 секунд
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // Валидация формы подбора корма
    const recommendForm = document.querySelector('form[action="/recommend"]');
    if (recommendForm) {
        recommendForm.addEventListener('submit', function(e) {
            const age = document.querySelector('input[name="age_years"]');
            const weight = document.querySelector('input[name="weight_kg"]');

            if (age && age.value && (age.value < 0.2 || age.value > 30)) {
                e.preventDefault();
                alert('Пожалуйста, введите корректный возраст (от 0.2 до 30 лет)');
            }

            if (weight && weight.value && (weight.value < 0.5 || weight.value > 15)) {
                e.preventDefault();
                alert('Пожалуйста, введите корректный вес (от 0.5 до 15 кг)');
            }
        });
    }
});