from django.urls import path
from . import views

urlpatterns = [
    path('', views.tables, name="horizon"),
    path('test/', views.test, name="test"),
    path('load/', views.load, name="load"),
]
