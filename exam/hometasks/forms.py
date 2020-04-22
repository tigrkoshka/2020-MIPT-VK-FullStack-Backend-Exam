from django import forms

from hometasks.models import *
from users.models import *

from django import forms
from hometasks.models import Hometask
from groups.models import UserGroup
import uuid
import magic


class AttachmentForm(forms.ModelForm):
	group_id = forms.IntegerField(required=True)
	user_id = forms.IntegerField(required=True)
	
	def __init__(self, *args, **kwargs):
		self._member = None
		super(AttachmentForm, self).__init__(*args, **kwargs)
	
	def clean_file(self):
		file = self.cleaned_data['file']
		if len(file.name) > 100:
			self.add_error('file', 'To long filename')
		return file
	
	def clean(self):
		cleaned_data = super(AttachmentForm, self).clean()
		group_id = cleaned_data['group_id']
		user_id = cleaned_data['user_id']
		try:
			self._member = UserGroup.objects.get(user_id=user_id, group_id=group_id)
		except UserGroup.DoesNotExist:
			self.add_error('group_id', 'Invalid')
		return cleaned_data
	
	def save(self, *args, **kwargs):
		user = self._member.user
		group = self._member.group
		description = self.cleaned_data['description']
		file = self.cleaned_data['file']
		attachment = Hometask(group=group, description=description)
		attachment.type = magic.from_buffer(file.read(), mime=True)
		attachment.file.save(f'{group.id}/{uuid.uuid4().hex}', file)
		attachment.name = file.name
		attachment.save()
		return attachment
	
	class Meta:
		model = Hometask
		fields = ['file', 'description']


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
