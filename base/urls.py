from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Paragraph search API",
        default_version="v1",
        description="API endpoints to search for a word in paragraphs",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
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
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
