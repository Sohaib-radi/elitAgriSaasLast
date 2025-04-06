from core.models.audit import UserLog

def log_user_action(request, user, action, farm=None):
    ip = request.META.get('REMOTE_ADDR')
    agent = request.META.get('HTTP_USER_AGENT', '')[:500]
    UserLog.objects.create(
        user=user,
        action=action,
        farm=farm,
        ip_address=ip,
        user_agent=agent
    )
