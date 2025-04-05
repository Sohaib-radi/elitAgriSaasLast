from rest_framework.permissions import IsAuthenticated
from core.permissions.permissions import IsNotExpired
from .registry import PERMISSION_MAP

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
        if action in ["list", "retrieve"]:
            custom_permissions = PERMISSION_MAP.get(module, {}).get("read", [])
        else:
            custom_permissions = PERMISSION_MAP.get(module, {}).get("write", [])

        return base_permissions + (custom_permissions or super().get_permissions())
