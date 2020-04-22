import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from hometasks.forms import *

import boto3
from hometasks.forms import AttachmentForm
from hometasks.models import Hometask
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Hometask.objects.all()

    @action(methods=['get'], detail=False, url_path='group/(?P<group_id>[^/.]+)/attachment/(?P<attachment_id>[^/.]+)')
    def get_attachment(self, request, group_id=None, attachment_id=None):
        try:
            queryset = self.get_queryset()
            attachment = queryset.get(id=attachment_id, group_id=group_id)
        except Hometask.DoesNotExist:
            return Response({'error': 'No such doc'}, status.HTTP_400_BAD_REQUEST)

        session = boto3.session.Session()
        s3_client = session.client(
            service_name='s3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': 'track_vaganov',
                'Key': Hometask.file.name,
            },
            ExpiresIn=3600)

        response = Response({'attachment': url}, status.HTTP_200_OK)
        return response

    @action(methods=['post'], detail=False, url_path='save')
    def attachment_save(self, request):
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return Response({'status': 'Attachment successfully loaded.'}, status.HTTP_200_OK)
        else:
            return Response({'errors': form.errors}, status.HTTP_400_BAD_REQUEST)


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
