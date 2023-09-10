from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    email = models.EmailField(unique=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    ordering = ('created',)


    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    surname = models.CharField(max_length=120, blank=True)

    def __str__(self) -> str:
        return self.user.get_full_name()


class Address(models.Model):
    user = models.OneToOneField(User, related_name="address", on_delete=models.CASCADE)
    country = models.CharField(max_length=80, blank=True)
    region = models.CharField(max_length=80, blank=True)
    city = models.CharField(max_length=80, blank=True)
    address = models.CharField(max_length=40, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)

    def __str__(self) -> str:
        return self.user.get_full_name()


def create_profile_and_address(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Address.objects.create(user=instance)

post_save.connect(create_profile_and_address, sender=User)