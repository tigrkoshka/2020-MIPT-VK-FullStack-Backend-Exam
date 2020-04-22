import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from hometasks.forms import *


@csrf_exempt
@require_POST
def set_status(request):
	form = SetStatusForm(json.loads(request.body))
	if form.is_valid():
		form.save()
		
		return JsonResponse({
			'msg': 'Статус успешно установлен'
		})
	else:
		return JsonResponse({'errors': form.errors}, status=400)
