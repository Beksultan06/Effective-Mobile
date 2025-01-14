from django.contrib import admin
from app.cafe.models import Order
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "table_number", "total_price", "status"]
    list_filter = ['id', 'table_number', "status"]
    search_fields = ['id', 'table_number', "status"]
    list_editable = ['status']