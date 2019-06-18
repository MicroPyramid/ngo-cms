from django.db import models
from django.contrib.auth import models as auth_models


class UserManager(auth_models.BaseUserManager):

    def create_user(self, email):

        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=UserManager.normalize_email(email))
        user.is_staff = True
        user.is_active = True
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):

        user = self.model(email=UserManager.normalize_email(email))

        user = self.create_user(email)
        user.is_admin = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self.db)
        return user


class User(auth_models.AbstractBaseUser):

    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    TYPE = (
        ("user", "user"),
        ("Admin", "Admin"),
    )

    email = models.EmailField(unique=True)
    rpwd = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(("Gender"),
                              max_length=10, choices=GENDER, default="Unknown")
    join_date = models.DateTimeField(auto_now_add=True)
    mobile = models.CharField(max_length=15)
    user_type = models.CharField(
        ("UserType"), max_length=10, choices=TYPE, default="user")
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def get_ful_name(self):
        return self.email

    def is_staff(self):
        return self.is_staff

    def __str__(self):
        return self.first_name or self.email

    def has_perms(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    class Meta:
        db_table = "blog_auth_user"
