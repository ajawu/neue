from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:product_id>/', views.create_review, name='create_review'),
    path('create/', views.create_review, name='create_review'),
    path('', views.create_review, name='create_review')
]
