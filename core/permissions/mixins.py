from rest_framework.permissions import IsAuthenticated
from core.permissions.permissions import IsNotExpired
from .registry import PERMISSION_MAP
from rest_framework.exceptions import PermissionDenied


class AutoPermissionMixin:
    """
    Automatically sets permission_classes based on action and PERMISSION_MAP.
    Injects global base permissions like IsAuthenticated and IsNotExpired.
    """

    def get_permissions(self):
        module = getattr(self, "permission_module", None)
        base_permissions = [IsAuthenticated(), IsNotExpired()]

        if not module:
            return base_permissions + super().get_permissions()

        action = getattr(self, "action", "read")
        module_perms = PERMISSION_MAP.get(module)

        if not module_perms:
            raise PermissionDenied(f"❌ No permissions configured for module '{module}'")

        if action in ["list", "retrieve"]:
            custom_permissions = module_perms.get("read")
        else:
            custom_permissions = module_perms.get("write")

        if custom_permissions is None:
            raise PermissionDenied(f"❌ No '{action}' permissions configured for module '{module}'")

        return base_permissions + custom_permissions
