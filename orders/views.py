from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from cart.cart import Cart
from .forms import CheckoutForm
from .models import Order, OrderItem
from catalog.models import ProductVariant
from classes.models import Course, ClassSession

User = get_user_model()

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('catalog:product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST, request=request)
        if form.is_valid():
            user = request.user
            
            # Create user inline if they are a guest
            if not user.is_authenticated:
                user = User.objects.create_user(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    phone_number=form.cleaned_data['phone_number']
                )
                login(request, user) # Automatically log them in
            
            # Create the Order
            order = Order.objects.create(
                user=user,
                total_amount=cart.get_total_price(),
                city=form.cleaned_data['city'],
                neighborhood=form.cleaned_data['neighborhood'],
                street_address=form.cleaned_data['street_address'],
                delivery_notes=form.cleaned_data['delivery_notes']
            )

            # Process Cart Items
            for item in cart:
                order_item = OrderItem(
                    order=order,
                    quantity=item['quantity'],
                    price_at_time=item['price']
                )
                
                if item['type'] == 'variant':
                    variant = ProductVariant.objects.get(id=item['id'])
                    variant.stock -= item['quantity'] # Deduct stock
                    variant.save()
                    order_item.product_variant = variant
                
                elif item['type'] == 'session':
                    session = ClassSession.objects.get(id=item['id'])
                    session.attendees_count += item['quantity'] # Increase bookings
                    session.save()
                    order_item.class_session = session
                
                elif item['type'] == 'online':
                    course = Course.objects.get(id=item['id'])
                    order_item.online_course = course
                    
                order_item.save()

            # Clear the cart session
            cart.clear()
            
            return redirect('orders:success', order_id=order.id)
    else:
        form = CheckoutForm(request=request)

    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})

def success(request, order_id):
    # In a real app, verify request.user owns this order
    return render(request, 'orders/success.html', {'order_id': order_id})
