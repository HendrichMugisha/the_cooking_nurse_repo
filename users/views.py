from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum

from orders.models import Order
from catalog.models import Product, ProductVariant, Category
from classes.models import Course, ClassSession
from portfolio.models import SiteSettings, NewsletterSubscriber
from .forms import ProductForm, ProductVariantFormSet, CourseForm, ClassSessionFormSet

User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('users:staff_dashboard')
        return redirect('users:dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            next_url = request.GET.get('next')
            if not next_url:
                next_url = 'users:staff_dashboard' if user.is_staff else 'users:dashboard'
            return redirect(next_url)
    else:
        form = AuthenticationForm()
        
    return render(request, 'users/login.html', {'form': form})

def signup_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('users:staff_dashboard')
        return redirect('users:dashboard')
        
    from .forms import CustomUserCreationForm
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"Welcome, {user.first_name or user.email}! Your account has been created.")
            return redirect('users:dashboard')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'users/signup.html', {'form': form})

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
    Unified hub for global management. Renders tables, summaries, and stats.
    Forms for settings are directly processed here.
    """
    settings = SiteSettings.get_settings()
    from classes.models import StudioRentalPricing
    pricing = StudioRentalPricing.load()
    
    from .forms import SiteSettingsForm, StudioRentalPricingForm
    settings_form = SiteSettingsForm(instance=settings)
    pricing_form = StudioRentalPricingForm(instance=pricing)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Support both explicit action and direct key matching (for tests / quick updates)
        is_inventory_post = (action == 'update_inventory') or any(k.startswith('variant_') for k in request.POST.keys())
        
        if is_inventory_post:
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
            return redirect('/users/staff-dashboard/?tab=tab-inventory')
            
        elif action == 'update_settings':
            import traceback as tb
            import sys
            try:
                print("\n[DEBUG] ==== update_settings POST received ====", file=sys.stderr)
                print(f"[DEBUG] FILES keys: {list(request.FILES.keys())}", file=sys.stderr)
                print(f"[DEBUG] Building SiteSettingsForm...", file=sys.stderr)
                settings_form = SiteSettingsForm(request.POST, request.FILES, instance=settings)
                pricing_form = StudioRentalPricingForm(request.POST, instance=pricing)
                print(f"[DEBUG] Running settings_form.is_valid()...", file=sys.stderr)
                settings_valid = settings_form.is_valid()
                print(f"[DEBUG] settings_form.is_valid() = {settings_valid}", file=sys.stderr)
                if not settings_valid:
                    print(f"[DEBUG] settings_form errors: {settings_form.errors}", file=sys.stderr)
                pricing_valid = pricing_form.is_valid()
                print(f"[DEBUG] pricing_form.is_valid() = {pricing_valid}", file=sys.stderr)
                if settings_valid and pricing_valid:
                    print(f"[DEBUG] Calling settings_form.save()...", file=sys.stderr)
                    settings_form.save()
                    print(f"[DEBUG] settings_form.save() succeeded. Calling pricing_form.save()...", file=sys.stderr)
                    pricing_form.save()
                    print(f"[DEBUG] All saves succeeded!", file=sys.stderr)
                    messages.success(request, "Site settings and studio pricing updated successfully!")
                    return redirect('/users/staff-dashboard/?tab=tab-site')
                else:
                    messages.error(request, "Failed to update settings. Please check the form errors.")
            except Exception as e:
                print("\n[DEBUG] !!!!!!!!!! CRASH IN update_settings !!!!!!!!!!!", file=sys.stderr)
                print(f"[DEBUG] Error type: {type(e).__name__}", file=sys.stderr)
                print(f"[DEBUG] Error message: {str(e)}", file=sys.stderr)
                tb.print_exc(file=sys.stderr)
                print("[DEBUG] !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", file=sys.stderr)
                raise

        elif action == 'studio_booking_status':
            booking_id = request.POST.get('booking_id')
            new_status = request.POST.get('status')
            from classes.models import StudioBooking
            booking = get_object_or_404(StudioBooking, id=booking_id)
            if new_status in ['pending', 'approved', 'cancelled', 'paid']:
                booking.status = new_status
                booking.save()
                messages.success(request, f"Studio booking #{booking.id} status updated to {booking.get_status_display()}!")
            else:
                messages.error(request, "Invalid status transition.")
            return redirect('/users/staff-dashboard/?tab=tab-rentals')

    # Fetch data lists
    products = Product.objects.all().prefetch_related('categories', 'variants').order_by('-created_at')
    courses = Course.objects.all().prefetch_related('sessions').order_by('-id')
    all_orders = Order.objects.all().select_related('user').order_by('-created_at')
    users = User.objects.all().order_by('-date_joined')
    subscribers = NewsletterSubscriber.objects.all().order_by('-subscribed_at')
    
    from classes.models import StudioBooking
    studio_bookings = StudioBooking.objects.all().order_by('-created_at')
    
    # Calculate stats
    total_rev = Order.objects.filter(status__in=['paid', 'shipped', 'completed']).aggregate(total=Sum('total_amount'))['total'] or 0
    low_stock = ProductVariant.objects.filter(product__product_type='physical', stock__lte=5).count()
    upcoming_seats = ClassSession.objects.filter(course__is_active=True).order_by('date')
    
    context = {
        'products': products,
        'courses': courses,
        'all_orders': all_orders,
        'users': users,
        'subscribers': subscribers,
        'studio_bookings': studio_bookings,
        'settings': settings,
        'settings_form': settings_form,
        'pricing_form': pricing_form,
        'total_revenue': total_rev,
        'low_stock_count': low_stock,
        'upcoming_seats': upcoming_seats,
        'subscribers_count': subscribers.count(),
        'active_tab': request.GET.get('tab', 'tab-analytics')
    }
    return render(request, 'users/staff_dashboard.html', context)

# --- PRODUCT CRUD ---

@staff_member_required
def product_create_or_edit(request, pk=None):
    product = get_object_or_404(Product, pk=pk) if pk else None
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductVariantFormSet(request.POST, instance=product)
        if form.is_valid() and formset.is_valid():
            try:
                saved_product = form.save()
                formset.instance = saved_product
                formset.save()
                messages.success(request, f"Product '{saved_product.name}' saved successfully!")
                return redirect('/users/staff-dashboard/?tab=tab-inventory')
            except Exception as e:
                import traceback
                import sys
                print("\n" + "="*50, file=sys.stderr)
                print("CRITICAL ERROR DURING PRODUCT UPLOAD:", file=sys.stderr)
                traceback.print_exc()
                print("="*50 + "\n", file=sys.stderr)
                messages.error(request, f"System error during product upload: {str(e)}. Check Render Logs.")
        else:
            messages.error(request, "Failed to save product. Please check the errors below.")
    else:
        form = ProductForm(instance=product)
        formset = ProductVariantFormSet(instance=product)
        
    return render(request, 'users/product_form.html', {
        'form': form,
        'formset': formset,
        'product': product
    })

@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f"Product '{product.name}' and all its variants have been deleted.")
        return redirect('/users/staff-dashboard/?tab=tab-inventory')
    return render(request, 'users/confirm_delete.html', {
        'object': product,
        'cancel_url': '/users/staff-dashboard/?tab=tab-inventory',
        'type': 'Product'
    })

# --- CATEGORY CRUD ---

@staff_member_required
def category_create_or_edit(request, pk=None):
    from .forms import CategoryForm
    category = get_object_or_404(Category, pk=pk) if pk else None
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            saved_category = form.save()
            messages.success(request, f"Category '{saved_category.name}' saved successfully!")
            return redirect('/users/staff-dashboard/?tab=tab-inventory')
        else:
            messages.error(request, "Failed to save category. Please check the errors below.")
    else:
        form = CategoryForm(instance=category)
        
    return render(request, 'users/category_form.html', {
        'form': form,
        'category': category
    })

@staff_member_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, f"Category '{category.name}' has been deleted.")
        return redirect('/users/staff-dashboard/?tab=tab-inventory')
    return render(request, 'users/confirm_delete.html', {
        'object': category,
        'cancel_url': '/users/staff-dashboard/?tab=tab-inventory',
        'type': 'Category'
    })

# --- COURSE CRUD ---

@staff_member_required
def course_create_or_edit(request, pk=None):
    course = get_object_or_404(Course, pk=pk) if pk else None
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        formset = ClassSessionFormSet(request.POST, instance=course)
        if form.is_valid() and formset.is_valid():
            saved_course = form.save()
            formset.instance = saved_course
            formset.save()
            messages.success(request, f"Course '{saved_course.title}' saved successfully!")
            return redirect('/users/staff-dashboard/?tab=tab-classes')
        else:
            messages.error(request, "Failed to save course. Please check the errors below.")
    else:
        form = CourseForm(instance=course)
        formset = ClassSessionFormSet(instance=course)
        
    return render(request, 'users/course_form.html', {
        'form': form,
        'formset': formset,
        'course': course
    })

@staff_member_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, f"Course '{course.title}' and all its class sessions have been deleted.")
        return redirect('/users/staff-dashboard/?tab=tab-classes')
    return render(request, 'users/confirm_delete.html', {
        'object': course,
        'cancel_url': '/users/staff-dashboard/?tab=tab-classes',
        'type': 'Course'
    })

# --- ORDER CRUD ---

@staff_member_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {order.get_status_display()}!")
        return redirect('users:order_detail', pk=order.pk)
    return render(request, 'users/order_detail.html', {'order': order})

# --- USER MANAGEMENT ---

@staff_member_required
def toggle_user_staff(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "You cannot revoke your own staff privileges.")
    else:
        user.is_staff = not user.is_staff
        user.save()
        role = "Staff" if user.is_staff else "Customer"
        messages.success(request, f"User {user.email} updated to {role}.")
    return redirect('/users/staff-dashboard/?tab=tab-users')

@staff_member_required
def toggle_user_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "You cannot deactivate your own account.")
    else:
        user.is_active = not user.is_active
        user.save()
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f"User {user.email} account has been {status}.")
    return redirect('/users/staff-dashboard/?tab=tab-users')

# --- NEWSLETTER MANAGEMENT ---

@staff_member_required
def newsletter_subscriber_delete(request, pk):
    sub = get_object_or_404(NewsletterSubscriber, pk=pk)
    sub.delete()
    messages.success(request, f"Removed '{sub.email}' from newsletter subscribers.")
    return redirect('/users/staff-dashboard/?tab=tab-newsletter')
