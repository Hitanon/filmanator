from django.urls import path

from .import views

urlpatterns = [
    path('films/', views.get_films_by_criteria, name='titles'),
    # путь для дебага запросов к бд
    path('testfilms/', views.TestSelectTitles.as_view(), name='titles'),
]
