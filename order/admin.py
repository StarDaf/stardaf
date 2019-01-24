from django.contrib import admin
from .models import Order, OrderItem

class OrderItemTable(admin.TabularInline):
    list_display = ['quantity', 'price']
    list_filter = ['quantity']
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'address', 'city', 'paid', 'created', 'updated')
    list_filter = ('address', 'city', 'created', 'updated')
    raw_id_fields = ('user',)
    inlines = [OrderItemTable]

admin.site.register(Order, OrderAdmin)
