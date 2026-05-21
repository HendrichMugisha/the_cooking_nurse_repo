from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.customer_dashboard, name='dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
]
