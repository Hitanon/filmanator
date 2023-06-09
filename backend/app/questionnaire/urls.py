from django.urls import path

from questionnaire import views


urlpatterns = [
    path('api/v1/questionnaire/', views.QuestionnaireView.as_view(), name='questionnaires'),
    path('api/v1/questionnaire/<int:session_id>/', views.QuestionnaireView.as_view(), name='questionnaire'),
]
