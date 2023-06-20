import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from titles.models import Title
from titles.serializers import TitleSerializer
from titles.services import select_titles


class TitleAPIView(generics.RetrieveAPIView):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()


@csrf_exempt
def get_films_by_criteria(request):
    """Сервис, выполняющий выборку фильмов, используя переданные критерии"""
    data = request.body.decode('utf-8')
    if not data:
        return JsonResponse({'success': False, 'message': 'Критерии отбора не были получены'})

    try:
        criteria = json.loads(data)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    history = None
    films = select_titles(criteria, history)

    return JsonResponse({'success': True, 'films': films})


class TestSelectTitles(APIView):
    def get(self, request, *args, **kwargs):
        history = None
        criteria = {'genre': (16.0, None),
                    'content_rating': (16.0, None),
                    'country': [38],
                    'acting': [5],
                    'amount_of_dialogue': [9],
                    'audience': [19],
                    'graphics': [110],
                    'intellectuality': [125],
                    'mood': [136],
                    'narrative_method': [143],
                    'viewing_method': [158],
                    'viewing_time': [163],
                    'visual_atmosphere': [169],
                    }
        films = select_titles(criteria, history)

        return Response(films)
