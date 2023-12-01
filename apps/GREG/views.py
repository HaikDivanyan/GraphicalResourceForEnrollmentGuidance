from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import viewsets
from rest_framework.response import Response
 
#from rest_framework import viewsets
from .serlializer import ScheduleSerializer, ProfessorSerializer
from .models import *
# Create your views here.

from .scraping.DataController import DataController
dataControler = DataController()



#   def get(self, request, *args, **kwargs):
#         '''
#         List all the todo items for given requested user
#         '''
#         with open("scraping test scripts/dar.html") as f:
#           dars = dataControler.parseDar(f.read())
#         for professor in dars.professors:
#           p = Professor(name= professor.name, rating = professor.rating)
#           p.save()
#         professors = Professor.objects.all()
#         serializer = ProfessorSerializer(professors, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

  
#   #return Response(serializer.data)
def darspars(request):
  if request.method == 'GET':
    with open("scraping test scripts/dar.html") as f:
      dars = dataControler.parseDar(f.read())
    for professor in dars.professors:
      p = Professor(name= professor.name, rating = professor.rating)
      p.save()
    for cls in dars.classes:
      c = ClassObj(name= cls.name, units = cls.units, rating = cls.rating, subjectArea = cls.subjectArea, hotseatGraph= cls.hosteatGraph,gradeDistributions= cls.gradeDistributions, classId=cls.id)
      c.save()
      for lect in cls.lectures:
        l = Lecture(classId = lect.id, classObj=c, professors= lect.professors)
        l.save()
        for disc in lect.discussions:
           section = DiscussionSection(discussionId = disc.id, lectures = l )
           section.save()
           for time in disc.times:
              tm = Time(days= time.days, hours= time.hours, discussionTime= section)
              tm.save()
        for time in lect.times:
              tmc = Time( days= time.days, hours= time.hours, lectureTime = l)
              print(tmc)
              tmc.save()
        dars.requirements
    return HttpResponse("GREG")
      
# class ClassListView (viewsets.ModelViewSet):
#     queryset = Professor.objects
#     serializer_class = ProfessorSerializer
    
#   # for cls in dars.classes:
#   #    cls = ClassObj
    
