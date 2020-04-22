from django import forms

from hometasks.models import *
from users.models import *


class SetStatusForm(forms.Form):
	user_id = forms.IntegerField()
	hometask_id = forms.IntegerField()
	status = forms.CharField()
	
	def clean_user_id(self):
		try:
			User.objects.get(id=self.cleaned_data['user_id'])
		except User.DoesNotExist:
			self.add_error('user_id', 'no such user')
			return
		return self.cleaned_data['user_id']
	
	def clean_hometask_id(self):
		try:
			Hometask.objects.get(id=self.cleaned_data['hometask_id'])
		except User.DoesNotExist:
			self.add_error('hometask_id', 'no such hometask')
			return
		return self.cleaned_data['hometask_id']
	
	def clean_status(self):
		if self.cleaned_data['status'].lower() == 'assigned':
			return 'A'
		elif self.cleaned_data['status'].lower() == 'done':
			return 'D'
		elif self.cleaned_data['status'].lower() == 'change_required':
			return 'C'
		elif self.cleaned_data['status'].lower() == 'success':
			return 'S'
		elif self.cleaned_data['status'].lower() not in ['A', 'D', 'C', 'S']:
			self.add_error('status', 'invalid status')
			return
		
	def save(self):
		user = User.objects.get(id=self.cleaned_data['user_id'])
		hometask = Hometask.objects.get(id=self.cleaned_data['hometask_id'])
		UserHometask.objects.filter(user=user, hometask=hometask).update(status=self.cleaned_data['status'])
