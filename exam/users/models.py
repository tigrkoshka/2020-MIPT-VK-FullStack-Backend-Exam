from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	prep = models.BooleanField(verbose_name="Преподаватель")
	
	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'
