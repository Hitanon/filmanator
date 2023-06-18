from titles import models


CRITERIONS = {
    True: {
        'content_rating': models.ContentRating,
    },
    False: {
        'acting': models.Acting,
        # 'actor': models.Actor,
        'amount_of_dialogues': models.AmountOfDialogue,
        'audience': models.Audience,
        'country': models.Country,
        # 'director': models.Director,
        'genre': models.Genre,
        'graphic': models.Graphics,
        'intellectuality': models.Intellectuality,
        'mood': models.Mood,
        'narrative_method': models.NarrativeMethod,
        'viewing_method': models.ViewingMethod,
        'viewing_times': models.ViewingMethod,
        'visual_atmosphere': models.VisualAtmosphere,
    },
}

NAMED_CRITERIONS = (
    # 'actor',
    # 'director',
)

CRITERION_TITLES = (
    'content_rating',
    'genre',
    'country',
    'acting',
    'amount_of_dialogues',
    'audience',
    'graphic',
    'intellectuality',
    'mood',
    'narrative_method',
    'viewing_method',
    'viewing_times',
    'visual_atmosphere',
    # 'actor',
    # 'director',
)

QUESTIONS = {
    'Не интересует': {
        'genre': 'Какой жанр предпочитаете?',
    },
    'Не важно': {
        'content_rating': 'Какие возрастные ограничения?',
        'country': 'Какая страна производства?',
        'acting': 'Какая игра актеров?',
        'amount_of_dialogues': 'Какое количество диалогов?',
        'audience': 'Какая вы аудитория?',
        'graphic': 'Какая графика?',
        'intellectuality': 'Какая интеллектуальность?',
        'mood': 'Какое настроение?',
        'narrative_method': 'Какой нарратив?',
        'viewing_method': 'Какой способ просмотра?',
        'viewing_times': 'Какое время просмотра?',
        'visual_atmosphere': 'Какая визуальная атмосфера?',
        # 'director': 'Какой режиссер вас интересует?',
        # 'actor': 'Какой актер вас интересует?',
    },
}

CATEGORIES = {
    'genre': 1,
    'content_rating': 2,
    'country': 5,
    'acting': 5,
    'amount_of_dialogues': 6,
    'audience': 7,
    'graphic': 8,
    'intellectuality': 9,
    'mood': 10,
    'narrative_method': 11,
    'viewing_method': 12,
    'viewing_times': 13,
    'visual_atmosphere': 14,
    # 'director': 10,
    # 'actor': 20,
}
