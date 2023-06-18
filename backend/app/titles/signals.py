from django.db.models.signals import post_migrate
from django.dispatch import receiver

from titles.models import Acting, AmountOfDialogue, Audience, Graphics, Intellectuality, Mood, NarrativeMethod, \
    ViewingMethod, ViewingTime, VisualAtmosphere

mood = {
    'веселый': 1,
    'грустный': 2,
    'страшный': 3,
    'смешный': 4,
    'раздражающий': 5,
    'драматичный': 6,
    'захватывающий': 7,
    'скучный': 8,
    'вдохновляющий': 9,
    'срываюший башку': 10,
    'романтический': 11,
    'тревожный': 12,
    'напряженный': 13,
    'ностальгический': 14,
    'меланхоличный': 15,
}

viewing_method = {
    'один': 1,
    'с друзьями': 2,
    'с семьей': 3,
    'с партнером': 4,
    'с незнакомцами': 5,
}

viewing_time = {
    'утро': 1,
    'день': 2,
    'вечер': 3,
    'ночь': 4,
}

visual_atmosphere = {
    'красочная': 1,
    'мрачная': 2,
    'реалистичная': 3,
    'сюрреалистичная': 4,
    'абстрактная': 5,
    'темная': 6,
    'яркая': 7,
    'натуральная': 8,
    'искусственная': 9,
    'минималистичная': 10,
}

audience = {
    'для всей семьи': 1,
    'детская': 2,
    'взрослая': 3,
    'подростковая': 4,
    'универсальная': 5,
    'нишевая': 6,
    'пожилых людей': 7,
    'женская': 8,
    'мужская': 9,
}

intellectuality = {
    'глубокая': 1,
    'сложная': 2,
    'простая': 3,
    'скучная': 4,
    'умная': 5,
    'глупая': 6,
    'оригинальная': 7,
    'банальная': 8,
    'эрудированная': 9,
    'философская': 10,
    'историческая': 11,
    'научная': 12,
    'художественная': 13,
    'культурная': 14,
}

narrative_method = {
    'линейный': 1,
    'нелинейный': 2,
    'эпизодический': 3,
    'циклический': 4,
    'извилистый': 5,
    'предсказуемый': 6,
    'непредсказуемый': 7,
    'последовательный': 8,
    'несвязный': 9,
    'обратный': 10,
    'рекурсивный': 11,
    'флешбек': 12,
    'инвертированный': 13,
    'параллельный': 14,
    'всеведущий': 15,
}

acting = {
    'убедительная': 1,
    'неубедительная': 2,
    'эмоциональная': 3,
    'выразительная': 4,
}

amount_of_dialogue = {
    'много': 1,
    'мало': 2,
    'сбалансированно': 3,
    'необычный стиль диалогов': 4,
}

graphics = {
    'реалистичная': 1,
    'нереалистичная': 2,
    'современная': 3,
    'устаревшая': 4,
    'стилизованная': 5,
}


def add_data(data, model):
    for key, value in data.items():
        if not model.objects.filter(title=key).exists():
            model.objects.create(title=key)


@receiver(post_migrate)
def add_initial_data(**kwargs):
    add_data(mood, Mood)
    add_data(viewing_method, ViewingMethod)
    add_data(viewing_time, ViewingTime)
    add_data(visual_atmosphere, VisualAtmosphere)
    add_data(audience, Audience)
    add_data(intellectuality, Intellectuality)
    add_data(narrative_method, NarrativeMethod)
    add_data(acting, Acting)
    add_data(amount_of_dialogue, AmountOfDialogue)
    add_data(graphics, Graphics)
