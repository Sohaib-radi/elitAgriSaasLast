from django.db import models
from ..models.base import BaseModel
from ..models.farm import Farm
from ..models.role import Role
from ..models.user import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from core.models.base import FarmLinkedModel
class TeamMember(BaseModel, FarmLinkedModel):
    # farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='team_members', verbose_name=_("Farm"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_assignments', verbose_name=_("User"))
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Role"))
    is_admin = models.BooleanField(default=False, verbose_name=_("Is Farm Admin"))

    #  Temporary Access Support
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Expires At"),
                                      help_text=_("If set, the user’s access to the farm will expire at this time."))
    class Meta:
        unique_together = ('farm', 'user')
        verbose_name = _("Team Member")
        verbose_name_plural = _("Team Members")

    def __str__(self):
        return f"{self.user.full_name} at {self.farm.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.user.active_farm:
            self.user.active_farm = self.farm
            self.user.save()
        
    def is_expired(self):
        """
         Checks if this team member's access has expired.
        """
        return self.expires_at and timezone.now() > self.expires_at
