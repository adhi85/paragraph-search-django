from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# Custom user manager
class CustomUserManager(BaseUserManager):
    # Create a user with email and password
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Create a superuser with email and password
    def create_superuser(self, email, name, password=None):
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Custom user model
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # Use email as the username
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email


# Paragraph model with owner field
class Paragraph(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="para_owner",
        default=User,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Word(models.Model):
    text = models.CharField(max_length=100, db_index=True)  # Word text
    para = models.ForeignKey(
        Paragraph, on_delete=models.CASCADE
    )  # Paragraph foreign key

    class Meta:
        unique_together = ("text", "para")
