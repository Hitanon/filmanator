from django.urls import path

from .import views

urlpatterns = [
    path('<int:pk>/', views.TitleAPIView.as_view(), name='title'),
    path('films/', views.get_films_by_criteria, name='titles')
]