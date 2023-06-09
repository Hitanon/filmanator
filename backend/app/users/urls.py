from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users import views


urlpatterns = [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/users/', views.UserView.as_view(), name='users'),

    path('api/v1/users/history/', views.HistoryView.as_view(), name='histories'),
    path('api/v1/users/history/<int:history_id>/', views.HistoryView.as_view(), name='history'),

    path('api/v1/users/title/liked/', views.LikedTitleView.as_view(), name='liked_titles'),
    path('api/v1/users/title/liked/<int:title_id>/', views.LikedTitleView.as_view(), name='liked_title'),

    path('api/v1/users/title/disliked/', views.DislikedTitleView.as_view(), name='disliked_titles'),
    path('api/v1/users/title/disliked/<int:title_id>/', views.DislikedTitleView.as_view(), name='disliked_title'),

    path('api/v1/users/genre/preffered/', views.PreferredGenreView.as_view(), name='preffered_genres'),
    path('api/v1/users/genre/preffered/<int:id>/', views.PreferredGenreView.as_view(), name='preffered_genre'),

    path('api/v1/users/genre/disfavored/', views.DisfavoredGenreView.as_view(), name='disfavored_genres'),
    path('api/v1/users/genre/disfavored/<int:id>/', views.DisfavoredGenreView.as_view(), name='disfavored_genre'),
]
