from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.customer_dashboard, name='dashboard'),
    
    # Custom Staff Panel CRUD URIs
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    
    # Products
    path('staff-dashboard/products/add/', views.product_create_or_edit, name='product_add'),
    path('staff-dashboard/products/<int:pk>/edit/', views.product_create_or_edit, name='product_edit'),
    path('staff-dashboard/products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Categories
    path('staff-dashboard/categories/add/', views.category_create_or_edit, name='category_add'),
    path('staff-dashboard/categories/<int:pk>/edit/', views.category_create_or_edit, name='category_edit'),
    path('staff-dashboard/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Courses
    path('staff-dashboard/courses/add/', views.course_create_or_edit, name='course_add'),
    path('staff-dashboard/courses/<int:pk>/edit/', views.course_create_or_edit, name='course_edit'),
    path('staff-dashboard/courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    
    # Orders
    path('staff-dashboard/orders/<int:pk>/', views.order_detail, name='order_detail'),
    
    # Users
    path('staff-dashboard/users/<int:pk>/toggle-staff/', views.toggle_user_staff, name='toggle_user_staff'),
    path('staff-dashboard/users/<int:pk>/toggle-active/', views.toggle_user_active, name='toggle_user_active'),
    
    # Newsletters
    path('staff-dashboard/newsletter/<int:pk>/delete/', views.newsletter_subscriber_delete, name='newsletter_delete'),
]
