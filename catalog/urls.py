from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('shop/', views.product_list, name='product_list'),
    path('download/<int:variant_id>/', views.download_digital_item, name='download_digital_item'),
]
