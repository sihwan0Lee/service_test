from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER = (
    ('M', '남성(Male)'),
    ('F', '여성(Female)'),
)


class User(AbstractUser):
    nickname = models.CharField(
        max_length=45, unique=True, verbose_name='회원이름')
    email = models.EmailField(
        max_length=200, unique=True, verbose_name='이메일')
    password = models.CharField(max_length=100, verbose_name='비밀번호')
    phone_number = models.CharField(
        max_length=50, unique=True,  verbose_name='전화번호')
    address = models.CharField(max_length=200, verbose_name='주소', blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER, verbose_name='성별', blank=True)
    register_date = models.DateField(auto_now_add=True, verbose_name='등록일')
    level = models.CharField(max_length=8, verbose_name='등급', choices=(
        ('admin', 'admin'), ('user', 'user')), default='user')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
        verbose_name = '회원'
        verbose_name_plural = '회원'
