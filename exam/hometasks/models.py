from django.db import models

from groups.models import Group
from users.models import User


class Hometask(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Задание')
	description = models.TextField(blank=True, null=True, verbose_name="Описание")
	file = models.FileField(blank=True, null=True, verbose_name="Файл с заданием")
	
	class Meta:
		verbose_name = 'Задание'
		verbose_name_plural = 'Задания'


class UserHometask(models.Model):
	ASSIGNED = "A"
	DONE = "D"
	CHANGE_REQUIRED = "C"
	SUCCESS = "S"
	STATUS_CHOICES = [
		(ASSIGNED, "assigned"),
		(DONE, "done"),
		(CHANGE_REQUIRED, "change_required"),
		(SUCCESS, "success")
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Студент')
	hometask = models.ForeignKey(Hometask, on_delete=models.CASCADE, verbose_name='Задание')
	status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=ASSIGNED)
	
	class Meta:
		verbose_name = 'Статус задания'
		verbose_name_plural = 'Статусы задания'
