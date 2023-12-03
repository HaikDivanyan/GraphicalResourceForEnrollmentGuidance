from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response

from .models import *
from .scraping.DataController import DataController
# Create your views here.
from .scraping.ScheduleGenerator import main
#from rest_framework import viewsets
from .serlializer import *

dataControler = DataController()
@api_view(['GET', 'POST'])
def haik(request):
  serialized_schedules = main()
  return Response("meow")

@api_view(['GET', 'POST'])
def schedules_api(request):
  if request.method == "POST":
    filter_parser(request.data)
    #  #need function that returns the list of Schedule objects need to be sent 
    schedules = Schedule.objects.all()
    scheduleSerializer = ScheduleSerializer(schedules, many=True)
    return Response(scheduleSerializer.data, status=status.HTTP_200_OK)
  return Response("Expected POST Request")

@api_view(['GET', 'POST'])
def upload_file(request):
  if request.method == "POST":
    form = UploadFileForm(request.POST, request.FILES)
    dars = darspars(request.FILES["file"])
    serializer = DarsSerializer(dars)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
 
def filter_parser (data):
  filter = UserFilters(  priorityClasses = data.get('priorityClasses'), 
                      ignoreClasses = data.get('ignoreClasses'), 
                      priorityRequirements = data.get('priorityRequirements'),
                      preferredSubjects = data.get('preferredSubjects'),
                      earliestStartTime = data.get('earliestStartTime'),
                      latestEndTime = data.get('latestEndTime'),
                      preferredDays = data.get('preferredDays'),
                      minClassRating = data.get('minClassRating'),
                      maxUnits = data.get('maxUnits'),
                      minUnits = data.get('minUnits'),
                      minNumClasses = data.get('minNumClasses'),
                      maxNumClasses =data.get('maxNumClasses'),)
  filter.save()
  

    