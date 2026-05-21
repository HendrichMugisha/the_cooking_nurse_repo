from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.filter(is_active=True).prefetch_related('variants', 'category')
    return render(request, 'catalog/product_list.html', {'products': products})
