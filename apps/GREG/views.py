from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response

from .models import *
from .scraping.DataController import DataController
# Create your views here.
from .scraping.ScheduleGenerator import main
from .scraping.Utils import UserFilters as PythonUserFilters
#from rest_framework import viewsets
from .serlializer import *

dataControler = DataController()
@api_view(['GET', 'POST'])
def haik(request):
  d = DataController()
  with open("scraping test scripts/dar.html") as f:
      a = d.parseDar(f.read())
  serialized_schedules = main(a, PythonUserFilters())
  return Response("meow")

@api_view(['GET', 'POST'])
def schedules_api(request):
  if request.method == "POST":
    filter = filter_parser(request.data)
    schedules = main(filter, schedules)
    return Response(schedules, status=status.HTTP_200_OK)
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
  filter = PythonUserFilters(priority_classes= data.get('priorityClasses'), 
                      ignore_classes = data.get('ignoreClasses'), 
                      priority_reqs = data.get('priorityRequirements'),
                      subject = data.get('preferredSubjects'),
                      earliest_start_time = data.get('earliestStartTime'),
                      latest_end_time = data.get('latestEndTime'),
                      preferred_days = data.get('preferredDays'),
                      min_class_rating= data.get('minClassRating'),
                      max_units = data.get('maxUnits'),
                      min_units = data.get('minUnits'),
                      min_num_classes = data.get('minNumClasses'),
                      max_num_classes =data.get('maxNumClasses'))
  return filter
  

    