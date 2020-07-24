from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_view, name='home_page'),
    path('search/', views.search_view, name='search_page'),
    path('dummy/', views.dummy_view, name='dummy_page'),
    path('contact/', views.contact_view, name='contact_page'),
    path('terms-of-use/', views.terms_condition_view, name='contact_page'),
    path('gallery/', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
