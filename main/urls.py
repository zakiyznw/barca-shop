from django.urls import path
<<<<<<< HEAD
from . import views

app_name = "main"

urlpatterns = [
    path("", views.show_main, name="show_main"),
]
=======
from main.views import show_main

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
]
>>>>>>> cf934d4 (Complete tugas Individu 2)
