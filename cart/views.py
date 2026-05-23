from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from catalog.models import ProductVariant
from classes.models import Course, ClassSession
from .cart import Cart

@require_POST
def cart_add(request, item_type, item_id):
    cart = Cart(request)
    item = None
    
    if item_type == 'variant':
        item = get_object_or_404(ProductVariant, id=item_id)
    elif item_type == 'online':
        item = get_object_or_404(Course, id=item_id, course_type='online')
    elif item_type == 'session':
        item = get_object_or_404(ClassSession, id=item_id)
        
    if item:
        # Get quantity from form, default to 1
        quantity = int(request.POST.get('quantity', 1))
        update_quantity = request.POST.get('update_quantity', 'False') == 'True'
        cart.add(item=item, item_type=item_type, quantity=quantity, update_quantity=update_quantity)
        item_name = getattr(item, 'title', None) or getattr(item.product, 'name', 'Item') if hasattr(item, 'product') else 'Item'
        messages.success(request, f"Added {item_name} to your cart.")
        
    # Redirect back to where they came from (or fallback to cart)
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER', 'cart:cart_detail')
    return redirect(next_url)

@require_POST
def cart_remove(request, item_type, item_id):
    cart = Cart(request)
    cart.remove(item_type, item_id)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
