from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserType(models.Model):
    USER_CHOICES = (
        ("manager", "운영자"),
        ("general", "일반 사용자"),
    )

    user_type = models.CharField("유저 유형", max_length=100, choices=USER_CHOICES)

    def __str__(self):
        return self.user_type


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """ createsuperuser 커맨드 전용 """
        user =  self.model(
            username=username,
            gender="undefined",
            **extra_fields
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    GENDER_CHOICES = (
        ("male", "남성"),
        ("female", "여성"),
        ("undefined", "미선택"),
    )

    user_type = models.ForeignKey(
        UserType, 
        on_delete=models.SET_NULL, 
        null=True
    )
    username = models.CharField(
        verbose_name="사용자 아이디", 
        max_length=12, 
        unique=True
    )
    password = models.CharField(
        verbose_name="비밀번호", 
        max_length=128
    )
    gender = models.CharField(
        verbose_name="성별", 
        max_length=20, 
        choices=GENDER_CHOICES, 
        default="undefined"
    )
    age = models.IntegerField("나이", default=0)
    joined_date = models.DateTimeField("가입일", auto_now_add=True)

    def __str__(self):
        return f"{self.username}"

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin