import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from questionnaire.services import get_history
from titles.models import Title
from titles.serializers import TitleSerializer
from titles.services import select_titles
from users.models import History


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

    history = Title.objects.none()
    films = select_titles(criteria, history)

    return JsonResponse({'success': True, 'films': films})


class TestSelectTitles(APIView):
    def get(self, request, *args, **kwargs):
        history = History.objects.filter(pk=1)
        criteria = {
            "genre": [1, 2, 3],
            "country": [1, 2],
            "mood": [1, 2, 3],
            "year": [2015, None],
            "imdb_rating": [6, None],
            "content_rating": [18, None]
        }
        films = select_titles(criteria, history)

        return Response(films)
