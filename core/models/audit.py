from django.db import models
from django.conf import settings
from core.constants.log_actions import LogActions
from core.models.base import FarmLinkedModel


class UserLog(FarmLinkedModel):
    ACTION_CHOICES = [
        (LogActions.LOGIN, 'Login'),
        (LogActions.LOGOUT, 'Logout'),
        (LogActions.SWITCH_FARM, 'Switched Farm'),
        (LogActions.AUTO_BIRTH_TRANSFER, 'Auto Transfer of Birth'),
        (LogActions.MANUAL_BIRTH_TRANSFER, 'Manual Transfer of Birth'),
        (LogActions.ANIMAL_CREATED, 'Animal Created'),
        (LogActions.ANIMAL_DELETED, 'Animal Deleted'),
        (LogActions.CURRENCY_ADDED, 'Currency Added'),
        (LogActions.CURRENCY_RATE_UPDATED, 'Currency Rate Updated'),
        (LogActions.ANIMAL_DEATH, 'Animal is Death'),
        (LogActions.VACCINE_ADDED, 'Vaccine Added'),
    ]


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=200, choices=ACTION_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.created_at}"
