from titles import models


CRITERIONS = {
    True: {
        'content_rating': models.ContentRating,
    },
    False: {
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
    'amount_of_dialogue',
    'audience',
    'graphics',
    'intellectuality',
    'mood',
    'narrative_method',
    'viewing_method',
    'viewing_time',
    'visual_atmosphere',
    # 'actor',
    # 'director',
)

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

# QUESTIONS = {
# 'Не интересует': {
#     'genre': 'Какой жанр предпочитаете?',
# },
# 'Не важно': {
#     'content_rating': 'Какие возрастные ограничения?',
#     'country': 'Какая страна производства?',
#     'acting': 'Какая игра актеров?',
#     'amount_of_dialogue': 'Какое количество диалогов?',
#     'audience': 'Какая вы аудитория?',
#     'graphics': 'Какая графика?',
#     'intellectuality': 'Какая интеллектуальность?',
#     'mood': 'Какое настроение?',
#     'narrative_method': 'Какой нарратив?',
#     'viewing_method': 'Какой способ просмотра?',
#     'viewing_time': 'Какое время просмотра?',
#     'visual_atmosphere': 'Какая визуальная атмосфера?',
#     # 'director': 'Какой режиссер вас интересует?',
#     # 'actor': 'Какой актер вас интересует?',
# },
# }

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
