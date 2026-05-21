from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_variant', 'online_course', 'class_session', 'quantity', 'price_at_time']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'id']
    readonly_fields = ['user', 'total_amount', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
