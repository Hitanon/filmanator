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
    path('api/v1/users/history/', views.HistoryView.as_view(), name='user_history'),
    path('api/v1/users/history/<int:id>/', views.HistoryView.as_view(), name='user_history'),
    path('api/v1/users/title/liked/', views.LikedTitleView.as_view(), name='user_liked_title'),
    path('api/v1/users/title/liked/<int:id>/', views.LikedTitleView.as_view(), name='user_liked_title'),
    path('api/v1/users/title/disliked/', views.DislikedTitleView.as_view(), name='user_disliked_title'),
    path('api/v1/users/title/disliked/<int:id>/', views.DislikedTitleView.as_view(), name='user_disliked_title'),
    path('api/v1/users/genre/preffered/', views.PreferredGenreView.as_view(), name='user_preffered_genre'),
    path('api/v1/users/genre/disfavored/', views.DisfavoredGenreView.as_view(), name='user_disfavored_genre'),
]
