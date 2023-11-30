from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

#from rest_framework import viewsets
from .serlializer import ScheduleSerializer
from .models import Schedule, Professor, ClassObj
# Create your views here.

from .scraping.DataController import DataController


class ScheduleList(APIView):
  queryset = Schedule.objects.all() 
      
    # specify serializer to be used 
  serializer_class = ScheduleSerializer 

  def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Schedule.objects
        serializer = ScheduleSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

dataControler = DataController()
def v(request):
  with open("scraping test scripts/dar.html") as f:
    dars = dataControler.parseDar(f.read())
  for professor in dars.professors:
     p = Professor(name= professor.name, rating = professor.rating)
     p.save()
     print(p)
  return HttpResponse('GREG')
class ClassListView (APIView):
    
    def darspars():
      return "shit"
      # d = DataController()
      # with open("../scraping test scripts/dar.html") as f:
      #   dar = d.parseDar(f.read())
      # for professor in dar.professors:
      #    Professor(name= professor.name, rating=float(professor.rating)).save()
      # # for c in dar.classes:
      # #    ClassObj(name= c.name, rating=float(c.rating) , id= c.id, units= c.units , subjectArea=c.subjectArea, hotseatGraph= c.hosteatGraph, gradeDistributions = c.gradeDistributions ).save()
      