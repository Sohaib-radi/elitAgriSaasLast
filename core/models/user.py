from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from ..models.base import BaseModel
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.update(is_staff=True, is_superuser=True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    # ✅ Core Auth Fields
    email = models.EmailField(unique=True, verbose_name=_("Email Address"))
    full_name = models.CharField(max_length=255, verbose_name=_("Full Name"))  # maps to `name` in frontend
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone Number"))  # maps to `phoneNumber`
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))  # maps to `isVerified` in frontend
    is_staff = models.BooleanField(default=False, verbose_name=_("Is Staff"))

    # ✅ Farm Context
    active_farm = models.ForeignKey("core.Farm", null=True, blank=True, on_delete=models.SET_NULL)

    # ✅ Extra Fields (from frontend)
    city = models.CharField(max_length=100, blank=True, verbose_name=_("City"))
    state = models.CharField(max_length=100, blank=True, verbose_name=_("State"))
    status = models.CharField(max_length=50, blank=True, verbose_name=_("Status"))  # e.g., active, suspended, pending
    address = models.CharField(max_length=255, blank=True, verbose_name=_("Address"))
    country = models.CharField(max_length=100, blank=True, verbose_name=_("Country"))
    zip_code = models.CharField(max_length=20, blank=True, verbose_name=_("Zip Code"))
    company = models.CharField(max_length=100, blank=True, verbose_name=_("Company"))
    avatar_url = models.URLField(blank=True, null=True, verbose_name=_("Avatar URL"))
    is_verified = models.BooleanField(default=False, verbose_name=_("Is Verified"))

    # ✅ Auth Management
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_groups',
        blank=True,
        verbose_name="Groups"
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_permissions',
        blank=True,
        verbose_name="User Permissions"
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email
