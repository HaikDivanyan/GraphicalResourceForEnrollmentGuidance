from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .scraping.DataController import DataController
# Create your views here.
from .scraping.ScheduleGenerator import main
#from rest_framework import viewsets
from .serlializer import *

dataControler = DataController()
@api_view(['GET', 'POST'])
def haik(request):
  main()
  return Response("meow")

@api_view(['GET', 'POST'])
def upload_file(request):
  if request.method == "POST":
    form = UploadFileForm(request.POST, request.FILES)
    dars = darspars(request.FILES["file"])
    serializer = DarsSerializer(dars)
    return Response(serializer.data)

def darspars(f) -> Dars:
  dars = dataControler.parseDar(f.read())
  darsObj = Dars()
  darsObj.save()
  for professor in dars.professors:
    p = Professor(name= professor.name, rating = professor.rating, dars= darsObj)
    p.save()

  for cls in dars.classes:
    c = ClassObj(name= cls.name, units = cls.units, rating = cls.rating, subjectArea = cls.subjectArea, hotseatGraph= cls.hosteatGraph,gradeDistributions= cls.gradeDistributions, classId=cls.id, dars= darsObj)
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
            tmc.save()

  for req in dars.requirements:
    r = Requirement(name = req.name, dars= darsObj)
    r.save()
    for sub in req.subrequirements:
       su = SubRequirement(name = sub.name, units = sub.units , count=sub.count, classes = sub.classes, subrequirements = r)
       su.save()
  return darsObj
 
  # professors = Professor.objects.all()
  # profserializer = ProfessorSerializer(professors, many=True)
  # requirements = Requirement.objects.all()
  # reqSerializer = RequirementSerializer(requirements, many = True)
  # classes = ClassObj.objects.all()
  # clasSerializer = ClassSerializer(classes, many=True)
  # response = {'professors': profserializer.data , 'requirements': reqSerializer.data, 'classes': clasSerializer.data}
  

    
