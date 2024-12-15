from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import MovieViewSet, RatingViewSet, UserViewSet
from rest_framework.views import APIView

router=routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('movies', MovieViewSet)
router.register('ratings', RatingViewSet)



urlpatterns = [
    path('', include(router.urls)),  # Include all router URLs
]


