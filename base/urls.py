from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('paras', views.create_paras, name='create_paras'),
    path('search/<str:word>', views.search_para, name='search_para')
]