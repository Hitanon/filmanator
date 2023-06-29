from titles import models

LIMITED_CRITERIONS = {
    'content_rating': models.ContentRating,
}

UNLIMITED_CRITERIONS = {
    'acting': models.Acting,
    # 'actor': models.Actor,
    'amount_of_dialogue': models.AmountOfDialogue,
    'audience': models.Audience,
    'country': models.Country,
    # 'director': models.Director,
    'genre': models.Genre,
    'graphics': models.Graphics,
    'intellectuality': models.Intellectuality,
    'mood': models.Mood,
    'narrative_method': models.NarrativeMethod,
    'viewing_method': models.ViewingMethod,
    'viewing_time': models.ViewingTime,
    'visual_atmosphere': models.VisualAtmosphere,
}

CRITERIONS = {
    True: LIMITED_CRITERIONS,
    False: UNLIMITED_CRITERIONS,
}

NAMED_CRITERIONS = (
    # 'actor',
    # 'director',
)

CRITERION_TITLES = [
    *[limited_criterion_key for limited_criterion_key in LIMITED_CRITERIONS.keys()],
    *[unlimited_criterion_key for unlimited_criterion_key in UNLIMITED_CRITERIONS.keys()],
]

QUESTIONS = {
    'content_rating': 'Какие возрастные ограничения?',
    'country': 'Какая страна производства?',
    'acting': 'Какая игра актеров?',
    'amount_of_dialogue': 'Какое количество диалогов?',
    'audience': 'Какая вы аудитория?',
    'graphics': 'Какая графика?',
    'intellectuality': 'Какая интеллектуальность?',
    'mood': 'Какое настроение?',
    'narrative_method': 'Какой нарратив?',
    'viewing_method': 'Какой способ просмотра?',
    'viewing_time': 'Какое время просмотра?',
    'visual_atmosphere': 'Какая визуальная атмосфера?',
    'genre': 'Какой жанр предпочитаете?',
    # 'director': 'Какой режиссер вас интересует?',
    # 'actor': 'Какой актер вас интересует?',
}

CATEGORIES = {
    'genre': 10,
    'content_rating': 9,
    'country': 8,
    'acting': 7,
    'amount_of_dialogue': 6,
    'audience': 5,
    'graphics': 4,
    'intellectuality': 3,
    'mood': 2,
    'narrative_method': 1,
    'viewing_method': 1,
    'viewing_time': 1,
    'visual_atmosphere': 1,
    # 'director': 10,
    # 'actor': 20,
}

DEFAULT_CUSTOM_QUESTION_PRIORITY = 100
