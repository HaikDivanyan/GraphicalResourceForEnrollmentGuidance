from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ( upload_file)

router = DefaultRouter()
#router.register('files', FilesViewSet, basename='files')


urlpatterns = [
    path('dars/', upload_file),
   # path('schedules/', )
]