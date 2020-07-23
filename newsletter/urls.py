from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('add/', views.add_email, name='add_user_newsletter'),
]
