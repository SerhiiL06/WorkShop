from django.contrib import admin
from .models import Category, Order


admin.site.register(Category)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "status", "master"]
