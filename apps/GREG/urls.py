from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import haik, upload_file

router = DefaultRouter()
#router.register('files', FilesViewSet, basename='files')


urlpatterns = [
    path('dars/', upload_file),
    path('', haik)
   # path('schedules/', )
]