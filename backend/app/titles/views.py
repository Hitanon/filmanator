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
        criteria = {'genre': [1, 2],
                    'acting': [3],
                    'amount_of_dialogue': [2],
                    'audience': [1],
                    'graphics': [3],
                    }
        films = select_titles(criteria, history)

        return Response(films)
