from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_view, name='home_page'),
    path('<str:newsletter_message>', views.home_view, name='home_page_message'),

    path('search/', views.search_view, name='search_page'),
    path('contact/', views.contact_view, name='contact_page'),
    path('delivery/', views.delivery_view, name='delivery_fees'),
    path('terms-of-use/', views.terms_condition_view, name='terms_and_conditions'),

    path('gallery/', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),

    path('artist/', views.ListArtist.as_view(), name='artist_list_page'),
    path('artist/<str:artist_username>/', views.artist_page, name='artist_details_page'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]
