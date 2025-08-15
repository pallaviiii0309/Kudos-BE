from django.contrib import admin
from .models import Organization, User, Kudo
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(Organization)
class OrgAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Org Info", {"fields": ("organization", "display_name")}),
    )
    list_display = ("id", "username", "display_name", "organization", "is_staff", "is_superuser")

@admin.register(Kudo)
class KudoAdmin(admin.ModelAdmin):
    list_display = ("id", "from_user", "to_user", "year", "week", "created_at")
    list_filter = ("year", "week", "from_user__organization")
    search_fields = ("message", "from_user__username", "to_user__username")
