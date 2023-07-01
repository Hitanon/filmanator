import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView

from titles.services import select_titles

from users.models import History


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

    history = History.objects.none()
    films = select_titles(criteria, history)

    return JsonResponse({'success': True, 'films': films})


class TestSelectTitles(APIView):
    def get(self, request, *args, **kwargs):
        history = History.objects.none()
        criteria = {
            'is_movie': False,
            'content_rating': [16, None],
            'imdb_rating': [8.5, None],
            'year': [2004, 2005],
            }
        films = select_titles(criteria, history)

        return Response(films)
