from __future__ import annotations

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.urls import reverse


class UserManager(BaseUserManager):
    def create_user(
        self, email: str, password: str | None = None, **other_fields
    ) -> User:

        user = User(email=email, **other_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):

    # remove default fields
    username = None
    first_name = None
    last_name = None

    email: str = models.EmailField("Email Address", unique=True)
    name: str = models.CharField(max_length=60)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set')

    def get_absolute_url(self) -> str:
        return reverse("profile", args=[self.id])

    def get_full_name(self) -> str:
        return self.name

    def get_short_name(self) -> str:
        return self.name