from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import UpdateUserForm

UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    ordering = ["-id"]
    list_display = ("mobile_number", "otp_last_login", "is_active")
    form = UpdateUserForm
    fieldsets = (
        (
            _("General Info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "mobile_number",
                    "otp_last_login",
                    "password",
                )
            },
        ),
    )
