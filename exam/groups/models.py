from django.db import models

from users.models import User


class Group(models.Model):
	name = models.CharField(blank=True, verbose_name="Название группы")
	
	class Meta:
		verbose_name = 'Группа'
		verbose_name_plural = 'Группы'
	

class UserGroup(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Студент')
	group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
	
	class Meta:
		verbose_name = 'Член группы'
		verbose_name_plural = 'Члены группы'
