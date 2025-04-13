from rest_framework.permissions import BasePermission
from core.models.team import TeamMember
from django.utils import timezone
from core.utils.permissions import has_permission


class IsFarmOwnerOrReadOnly(BasePermission):
    """
    Allow owners to modify their own farm-linked records
    """

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "farm", None) == getattr(request.user, "active_farm", None)
    
class IsFarmAdmin(BasePermission):
    """
    Allows access only to users who are farm admins in their active farm.
    """
    def has_permission(self, request, view):
        user = request.user
        farm = user.active_farm
        print('User form is farm admin')
        print(user.id)
        print(farm.id)
        if not farm:
            return False

        return TeamMember.objects.filter(user=user, farm=farm, is_admin=True).exists()


class IsNotExpired(BasePermission):
    """
    Deny access if the user's active farm membership has expired.
    """

    def has_permission(self, request, view):
        user = request.user
        farm = getattr(user, "active_farm", None)

        if not user.is_authenticated or not farm:
            return False

        try:
            member = TeamMember.objects.get(user=user, farm=farm)
        except TeamMember.DoesNotExist:
            return False

        # Deny access if expired
        if member.expires_at and timezone.now() > member.expires_at:
            return False

        return True
    

"""
we can used in view:
====================

class AnimalListView(APIView):
    permission_classes = [IsAuthenticated, HasRolePermission("animals.view")]
    def get(self, request):
        ...

# Or we can use the decoratore in function

@permission_required("animals.view")
def my_view(request):
    ...

# Use has_permission(user, "animals.add") in code
# Protect DRF views with HasRolePermission("code")
# Send permission list to frontend (to show/hide buttons)


"""
class HasRolePermission(BasePermission):
    """
    DRF permission class to check if the user has a specific permission code.
    Use like: HasRolePermission("animals.view")
    """

    def __init__(self, permission_code):
        self.permission_code = permission_code

    def has_permission(self, request, view):
        return has_permission(request.user, self.permission_code)