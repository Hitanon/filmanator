import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status

from titles.models import Title
from titles.serializers import TitleSerializer
from titles.services import get_titles_by_attrs


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

    films = get_titles_by_attrs(criteria)

    return JsonResponse({'success': True, 'films': films})