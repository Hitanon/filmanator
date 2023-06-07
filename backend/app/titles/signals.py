from django.db.models.signals import post_migrate
from django.dispatch import receiver

from titles.models import *

mood = {
    'happy': 1,
    'sad': 2,
    'scary': 3,
    'funny': 4,
    'annoying': 5,
    'dramatic': 6,
    'exciting': 7,
    'boring': 8,
    'inspiring': 9,
    'mind-blowing': 10,
    'romantic': 11,
    'thrilling': 12,
    'suspenseful': 13,
    'nostalgic': 14,
    'melancholic': 15
}

viewing_method = {
    'alone': 1,
    'with friends': 2,
    'with family': 3,
    'with partner': 4,
    'with strangers': 5
}

viewing_time = {
    'morning': 1,
    'day': 2,
    'evening': 3,
    'night': 4
}

visual_atmosphere = {
    'colorful': 1,
    'gloomy': 2,
    'realistic': 3,
    'surrealistic': 4,
    'abstract': 5,
    'dark': 6,
    'bright': 7,
    'natural': 8,
    'artificial': 9,
    'minimalist': 10
}

audience = {
    'family-friendly': 1,
    'children': 2,
    'adult': 3,
    "teenage": 4,
    'universal': 5,
    'niche-specific': 6,
    'elderly': 7,
    'women': 8,
    'men': 9
}

intellectuality = {
    'deep': 1,
    'complex': 2,
    'simple': 3,
    'boring': 4,
    'smart': 5,
    'stupid': 6,
    'original': 7,
    'banal': 8,
    'knowledgeable': 9,
    'philosophical': 10,
    'historical': 11,
    'scientific': 12,
    'artistic': 13,
    'cultural': 14
}

narrative_method = {
    'linear': 1,
    'nonlinear': 2,
    'episodic': 3,
    'cyclic': 4,
    'winding': 5,
    'predictable': 6,
    'unpredictable': 7,
    'sequential': 8,
    'incoherent': 9,
    'inverted': 10,
    'recursive': 11,
    'flashback': 12,
    'flashforward': 13,
    'parallel': 14,
    'omniscient': 15
}

acting = {
    'convincing': 1,
    'unconvincing': 2,
    'emotional': 3,
    'expressive': 4
}

amount_of_dialogue = {
    'many': 1,
    'few': 2,
    'balanced': 3,
    'unconventional dialogue style': 4
}

graphics = {
    'realistic': 1,
    'unrealistic': 2,
    'modern': 3,
    'outdated': 4,
    'stylized': 5
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
