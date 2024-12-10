from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import os
import uuid
from uuid import uuid4

def avatar_image_file_path(instance, filename):
    """Generate file path for new avatar image"""
    ext = os.path.splitext(filename)[-1].lstrip(".")  # 去掉扩展名中的点
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("uploads", "avatar", filename)

class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError("User must have an email address")

        # # 限制允许的字段
        # allowed_fields = {"name", "bio", "is_active", "is_staff"}
        # extra_fields = {k: v for k, v in extra_fields.items() if k in allowed_fields}

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a new superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # 新增字段
    bio = models.CharField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_image_file_path, blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)  # 用户的关注关系
    joined_at = models.DateTimeField(auto_now_add=True)
    last_login_time = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
