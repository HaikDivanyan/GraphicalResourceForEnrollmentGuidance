import json

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
    dars = dataControler.parseDar(request.FILES["file"].read())
    filterFile = request.POST.get('filters')
    filters = json.loads(filterFile)
    schedules = main(dars, filter_parser(filters))
    return Response(schedules, status=status.HTTP_200_OK)
  return Response("Expected POST Request")

@api_view(['GET', 'POST'])
def upload_file(request):
  if request.method == "POST":
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
 
def filter_parser(data):
    print(data)
    filter = PythonUserFilters(
        priority_classes=data.get('priorityClasses', None), 
        ignore_classes=data.get('ignoreClasses', None), 
        priority_reqs=data.get('priorityRequirements', None),
        subject=data.get('preferredSubjects', None),
        earliest_start_time=data.get('earliestStartTime', '6am'),
        latest_end_time=data.get('latestEndTime', '11pm'),
        preferred_days=data.get('preferredDays', "MTWRF"),
        min_class_rating=data.get('minClassRating', 0),
        max_units=data.get('maxUnits', 12),
        min_units=data.get('minUnits', 2),
        min_num_classes=data.get('minNumClasses', 1),
        max_num_classes=data.get('maxNumClasses', 4)
    )
    return filter  

def filter_parser(data):
    filter = PythonUserFilters(
        priority_classes=data.get('priorityClasses') if data.get('priorityClasses', None) is not None else None,
        ignore_classes=data.get('ignoreClasses') if data.get('ignoreClasses', None) is not None else None,
        priority_reqs=data.get('priorityRequirements') if data.get('priorityRequirements', None) is not None else None,
        ignore_reqs=data.get('ignoreRequirements') if data.get('ignoreRequirements', None) is not None else None,
        subject=data.get('preferredSubjects') if data.get('preferredSubjects', None) != [] else None,
        earliest_start_time=data.get('earliestStartTime') if data.get('earliestStartTime') != '' else '6am',
        latest_end_time=data.get('latestEndTime') if data.get('latestEndTime') != '' else '11pm',
        preferred_days=data.get('preferredDays') if data.get('preferredDays', None) != "" else "MTWRF" ,
        min_class_rating=float(data.get('minClassRating')),
        max_units=int(data.get('maxUnits', 12)) if data.get('maxUnits') != '' else 12,
        min_units=int(data.get('minUnits', 2)) if data.get('minUnits') != '' else 2,
        min_num_classes=int(data.get('minNumClasses', 1)) if data.get('minNumClasses') != '' else 1,
        max_num_classes=int(data.get('maxNumClasses', 4)) if data.get('maxNumClasses') != '' else 4
    )
    return filter

