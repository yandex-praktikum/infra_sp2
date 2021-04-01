from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet,
                    send_confirmation_code, get_jwt_token)

v1_router = DefaultRouter()
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(r'users', UserViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

# Надо исправить: Урлы с одинаковым префиксом выносим в
# отдельный список, чтобы сделать инклуд
v1_auth_patterns = [
    path('email/', send_confirmation_code, name='send_confirmation_code'),
    path('token/', get_jwt_token, name='get_token'),
]

urlpatterns = [
    path('v1/auth/', include(v1_auth_patterns)),
    path('v1/', include(v1_router.urls))
]
