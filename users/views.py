from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from orders.models import Order
from catalog.models import ProductVariant
from classes.models import ClassSession
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'users:dashboard')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
        
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('portfolio:home')

@login_required
def customer_dashboard(request):
    # Fetch orders belonging to the user
    orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items__product_variant', 'items__online_course', 'items__class_session')
    return render(request, 'users/dashboard.html', {'orders': orders})

@staff_member_required
def staff_dashboard(request):
    """
    A custom, easy-to-use inventory management screen for the client.
    """
    if request.method == 'POST':
        # Rapid Inventory Updater
        for key, value in request.POST.items():
            if key.startswith('variant_'):
                variant_id = key.split('_')[1]
                try:
                    variant = ProductVariant.objects.get(id=variant_id)
                    variant.stock = int(value)
                    variant.save()
                except (ProductVariant.DoesNotExist, ValueError):
                    continue
        messages.success(request, "Inventory updated successfully!")
        return redirect('users:staff_dashboard')

    variants = ProductVariant.objects.all().select_related('product')
    sessions = ClassSession.objects.filter(course__is_active=True).order_by('date')
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    
    context = {
        'variants': variants,
        'sessions': sessions,
        'recent_orders': recent_orders,
    }
    return render(request, 'users/staff_dashboard.html', context)
