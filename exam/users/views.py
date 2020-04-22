from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed
from datetime import datetime
from .models import User


# Create your views here


# fields ['username', 'password', 'email', 'prep']
# curl --data "username=test1&password=password1&email=test1@mail.ru&prep=True" http://127.0.0.1:8000/users/create_user/
def create_user(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		prep = request.POST.get('prep')
		
		is_superuser = False
		is_staff = False
		is_active = True
		# first_name = request.POST.get('first_name')
		# last_name = request.POST.get('last_name')
		first_name = username
		last_name = username
		
		date_joined = datetime.now()
		
		user = User(username=username, password=password, email=email,
					prep=prep, is_superuser=is_superuser, is_staff=is_staff, is_active=is_active,
					last_name=last_name, first_name=first_name, date_joined=date_joined)
		user.save()
		return JsonResponse({'user': user.id})
	else:
		return HttpResponseNotAllowed(['POST'])


def user_list(request):
	if request.method == 'GET':
		users = User.objects.values('id', 'username', 'prep')
		return JsonResponse({'users': list(users)})
	else:
		return HttpResponseNotAllowed(['GET'])


def user_info(request):
	if request.method == 'GET':
		user_id = request.GET.get('user_id')
		user = User.objects.filter(id=user_id)
		return JsonResponse({'user': list(user)})
	else:
		return HttpResponseNotAllowed(['GET'])
