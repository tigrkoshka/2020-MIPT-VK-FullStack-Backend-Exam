from django.urls import path, include
from rest_framework.routers import DefaultRouter

from hometasks.views import *

router = DefaultRouter()
router.register(r'attachment', AttachmentViewSet, basename='attachment')

urlpatterns = [
	path('attachment/', include(router.urls)),
	path('set_status/', set_status)
]
