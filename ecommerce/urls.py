from django.urls import path
from .views import ( checkout, add_to_cart, HomeView, ItemDetailView)

app_name='ecommerce'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', checkout, name='checkout'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
]

