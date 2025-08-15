from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, KudoViewSet, login, me

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"kudos", KudoViewSet, basename="kudos")

urlpatterns = [
    path("auth/login", login),   
    path("me", me),              
    path("", include(router.urls)),
]
