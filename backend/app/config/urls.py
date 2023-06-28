from django.urls import include, path


urlpatterns = [
    path('', include('users.urls')),
    path('', include('questionnaire.urls')),
    path('', include('titles.urls')),
]
