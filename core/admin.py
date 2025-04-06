from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.models.farm import Farm
from core.models.user import User
from core.models.role import Role
from core.models.team import TeamMember
from core.models.audit import UserLog
from core.models.invite import InviteToken
from core.models.permissions import Permission


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    filter_horizontal = ("permissions",)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ["code", "label"]
    search_fields = ["code", "label"]




@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'farm', 'ip_address', 'created_at']
    list_filter = ['action', 'created_at', 'farm']
    search_fields = ['user__email', 'ip_address', 'user_agent']


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "location", "is_active", "created_at")
    search_fields = ("name", "slug", "location")
    list_filter = ("is_active",)
    ordering = ("-created_at",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "full_name", "is_active", "is_staff", "created_at")
    list_filter = ("is_staff", "is_active", "created_at")
    ordering = ("-created_at",)
    search_fields = ("email", "full_name")

    readonly_fields = ("created_at", "updated_at", "last_login")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("full_name", "phone")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2", "is_staff", "is_active"),
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "farm", "role", "is_admin", "created_at")
    list_filter = ("role", "farm", "is_admin")
    search_fields = ("user__email", "farm__name", "role__name")
    autocomplete_fields = ("user", "farm", "role")
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.user.active_farm:
            obj.user.active_farm = obj.farm
            obj.user.save()

@admin.register(InviteToken)
class InviteTokenAdmin(admin.ModelAdmin):
    list_display = ['email', 'farm','token', 'role', 'is_admin', 'used', 'expires_at']
    list_filter = ['farm', 'used', 'expires_at']
    search_fields = ['email']
