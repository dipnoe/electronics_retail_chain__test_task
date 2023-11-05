from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User Model for Authentication and User Management.

    Fields:
    - email: An email field used for user authentication and must be unique.
    - first_name: A character field for the user's first name (maximum length: 50 characters).
    - last_name: A character field for the user's last name (maximum length: 50 characters).
    - role: A character field that represents the user's role. It uses the 'UserRole' choices.
    - is_active: A boolean field indicating whether the user is active.

    Choices:
    - UserRole: A class that defines user roles. Currently, it includes a single role 'employee'.
    """
    class UserRole(models.TextChoices):
        EMPLOYEE = 'EMP', _('employee')

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=3, choices=UserRole.choices)
    is_active = models.BooleanField(verbose_name='активный')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
