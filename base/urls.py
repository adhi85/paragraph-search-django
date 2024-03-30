from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", views.index, name="index"),
    path("paras", views.create_paras, name="create_paras"),
    path("search/<str:word>", views.search_para, name="search_para"),
    path(
        "token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # create a token
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # refresh a token
]
