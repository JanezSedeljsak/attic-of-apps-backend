from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Base.as_view()),
]