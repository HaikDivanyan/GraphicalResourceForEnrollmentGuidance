from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import viewsets

#from rest_framework import viewsets
from .serlializer import *
from .models import *
# Create your views here.
from .scraping.DataController import DataController
dataControler = DataController()


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
          darspars(request.FILES["file"])
        
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
@api_view(['GET', 'POST'])
def darspars(f):
  with open("scraping test scripts/dar.html") as fil:
    dars = dataControler.parseDar(fil.read())
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
            tmc.save()

  for req in dars.requirements:
    r = Requirement(name = req.name)
    r.save()
    for sub in req.subrequirements:
       su = SubRequirement(name = sub.name, units = sub.units , count=sub.count, classes = sub.classes, subrequirements = r)
       su.save()

  professors = Professor.objects.all()
  profserializer = ProfessorSerializer(professors, many=True)
  requirements = Requirement.objects.all()
  reqSerializer = RequirementSerializer(requirements, many = True)
  classes = ClassObj.objects.all()
  clasSerializer = ClassSerializer(classes, many=True)
  response = {'professors': profserializer.data , 'requirements': reqSerializer.data, 'classes': clasSerializer.data}

  return Response(response)

    
