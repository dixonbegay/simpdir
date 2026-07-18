# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import LDAPuser

# admin.site.register(LDAPuser, UserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import LDAPuser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = LDAPuser
    # readonly_fields = [field.name for field in LDAPuser._meta.get_fields()]
    readonly_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "groups",
        "department",
        "telephoneNumber",
        "mobile",
        "description",
        "title",
    ]
    list_display_links = ["username"]
    search_fields = ("username", "first_name", "last_name", "department")
    ordering = ("username", "first_name", "last_name", "department")
    # inlines = (UserProfileInline,)
    list_display = (
        "username",
        "first_name",
        "last_name",
        "department",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    list_filter = (
        "username",
        "first_name",
        "last_name",
        "department",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    fieldsets = (
        (None, {"fields": ("username",)}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "department",
                    "telephoneNumber",
                    "mobile",
                    "title",
                    "description",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "is_staff", "is_active", "department"),
            },
        ),
    )


admin.site.register(LDAPuser, CustomUserAdmin)
