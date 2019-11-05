from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class MyAccountManager(BaseUserManager):

    def create_user(self, username, email,  password=None):
        if not username:
            raise ValueError("User must have username")
        if not email:
            raise ValueError("User must have email")


        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


ROLE_CHOICES = (
    ('Customer', 'Customer'),
    ('Operator', 'Operator'),
    ('Manager', 'Manager'),
)

class Account(AbstractBaseUser):

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Customer')

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    hires_in_progress = models.IntegerField(default=0)
    wallet_balance = models.FloatField(default=0.00)
    amount_owed = models.FloatField(default=0.00)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

