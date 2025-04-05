from core.models.team import TeamMember
from django.utils import timezone

def has_permission(user, permission_code):
    """
    🔐 Checks if the user's role in their active farm includes the given permission code.
    Now uses the Role.permissions ManyToManyField.
    """
    farm = getattr(user, "active_farm", None)
    if not user.is_authenticated or not farm:
        return False

    try:
        member = TeamMember.objects.get(user=user, farm=farm)
    except TeamMember.DoesNotExist:
        return False

    # ⛔ Block if expired
    if member.expires_at and timezone.now() > member.expires_at:
        return False

    role = member.role
    if not role:
        return False

    return role.permissions.filter(code=permission_code).exists()
