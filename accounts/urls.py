from django.urls import path, include
from .views import *

urlpatterns = [
    path('signup', RegisterView.as_view()),
    path('login', LoginView.as_view()),
]