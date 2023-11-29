from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

#from rest_framework import viewsets
from .serlializer import ScheduleSerializer
from .models import Schedule
# Create your views here.

def greg_endpoint(request):
  return HttpResponse("GREG is live!")

class ScheduleList(APIView):
  def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Schedule.objects.filter(user = request.user.id)
        serializer = ScheduleSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)