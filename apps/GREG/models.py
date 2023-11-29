from django.db import models
from django.core.validators import int_list_validator

# models are not final and need to change depend on the clinet and scraping requirments
# creating a schedule model 


class ClassObj (models.Model):
    uints = models.IntegerField()
    subjectArea = models.CharField(max_length= 50)
    rating = models.FloatField()
    gradeDistribution = models.CharField(validators=[int_list_validator], max_length=100) # list of Int ? 
    hotSeat = models.CharField(max_length=100)
    classId = models.CharField(max_length=50) # double check the max length

class Schedule (models.Model):
    rating = models.FloatField() #could use ManytoManyField which creates schedule-class table 
    classes = models.ArrayField(model_container=ClassObj)

#how does this work? sample needed 
class Time (models.Model):
    days = models.CharField(max_length=20)
    hours = models.CharField(max_length=20)
    def __init__(self, days: str = None, hours: str = None):
        self.days = days
        self.hours = hours

class UserFilters (models.Model):
    priorityClasses = models.ArrayField(model_container=ClassObj)
    ignoreClasses = models.ArrayField(model_container=ClassObj)
    # user can choose multiple subject areas, shouldn't this be a list? 
    # subjectArea = models(models.CharField(max_length=10, blank=True),size=8) 
    subjectArea = models.CharField(max_length=100)
    earliestStartTime = models.ManyToManyField(Time)
    latestEndTime = models.ManyToManyField(Time)
    preferreDays =  models.ManyToManyField(Time)
    minClassRating = models.FloatField()
    maxUnites = models.IntegerField(default=12)
    numClasses = models.IntegerField(default=3)

