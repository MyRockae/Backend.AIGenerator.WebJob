from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and save a regular User with the given email, username, and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        if not username:
            raise ValueError('The Username must be set')
            
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=64, blank=True, null=True)
    reset_password_token = models.CharField(max_length=64, blank=True, null=True)
    token_expires_at = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def generate_verification_token(self):
        self.verification_token = get_random_string(length=64)
        self.token_expires_at = timezone.now() + timezone.timedelta(hours=24)
        self.save(update_fields=['verification_token', 'token_expires_at'])

    def generate_reset_token(self):
        self.reset_password_token = get_random_string(length=64)
        self.token_expires_at = timezone.now() + timezone.timedelta(hours=1)
        self.save(update_fields=['reset_password_token', 'token_expires_at'])

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        """
        Override the save method so that if the user_id is not set,
        we assign it after the user is saved and a primary key is available.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # Only update the user_id if the instance is new and user_id is not already set.
        if is_new and not self.user_id:
            prefix = "ADM" if self.is_superuser else "USR"
            self.user_id = f"{prefix}{self.pk}"
            # Update the database directly to avoid recursive saving
            User.objects.filter(pk=self.pk).update(user_id=self.user_id)
    
    class Meta:
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = 'Users'