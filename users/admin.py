from django.contrib import admin
from .models import User, Specific


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "is_staff", "is_master"]
    fields = ["username", "first_name", "last_name", "email"]
    list_per_page = 10
    list_filter = ["is_staff", "is_master", "specific__skills"]

    def get_list_filter(self, request):
        return super().get_list_filter(request)


@admin.register(Specific)
class SpecificAdmin(admin.ModelAdmin):
    pass
