from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_view, name='home_page'),
    path('<str:newsletter_message>', views.home_view, name='home_page'),
    path('search/', views.search_view, name='search_page'),
    path('contact/', views.contact_view, name='contact_page'),
    path('delivery/', views.delivery_view, name='delivery_fees'),
    path('terms-of-use/', views.terms_condition_view, name='terms_and_conditions'),
    path('gallery/', views.product_list, name='product_list'),
    path('gallery/<str:artist_name>/', views.product_list, name='product_list'),
    path('artist/', views.artist_page, name='artist_list'),
    path('artist/<int:artist_id>/', views.artist_page, name='artist_page'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
