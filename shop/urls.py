from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),

    path('search/', views.search_view, name='search_page'),
    path('contact/', views.contact_view, name='contact_page'),
    path('delivery/', views.delivery_view, name='delivery_fees'),
    path('terms-of-use/', views.terms_condition_view, name='terms_and_conditions'),

    path('gallery/', views.ProductList.as_view(), name='product_list'),
    path('gallery/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('collection/<slug:category_slug>/', views.ProductList.as_view(), name='product_list_by_category'),

    path('artist/', views.ListArtist.as_view(), name='artist_list_page'),
    path('artist/<str:artist_username>/', views.artist_page, name='artist_details_page'),
]
