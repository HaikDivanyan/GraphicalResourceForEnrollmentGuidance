from django.db import models
from django.core.validators import int_list_validator
from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
# models are not final and need to change depend on the clinet and scraping requirments
# creating a schedule model 

class ClassObj (models.Model):
    units = models.CharField(max_length=4, default='4.0')
    subjectArea = models.CharField(max_length= 15)
    rating = models.FloatField(null=True)
    gradeDistributions = models.CharField(validators=[int_list_validator], max_length=12, null = True) 
    hotseatGraph = models.CharField(max_length=100, null=True, blank=True)
    classId = models.CharField(max_length=25) # double check the max length
    name = models.CharField(max_length= 150)
    def __str__(self):
        return self.name

class Requirement(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name

class SubRequirement(models.Model):
    name = models.CharField(max_length= 150)
    units = models.IntegerField()
    count = models.IntegerField()
    subrequirements = models.ForeignKey(Requirement, related_name='subrequirements', on_delete=models.CASCADE)
    classes = models.CharField(max_length=200, blank=True, default='')
    def __str__(self) -> str:
        return self.name

class Schedule (models.Model):
    rating = models.FloatField() #could use ManytoManyField which creates schedule-class table 
    # classes = ArrayField(model_container=ClassObj)

    def __str__(self):
        return self.rating

class Professor (models.Model):
    rating = models.FloatField(null=True)
    name = models.CharField(max_length=90)

    def __str__(self):
        return self.name
class RegistrarData(models.Model):
    classId = models.CharField(max_length=20)
    className = models.CharField(max_length=100)
    units = models.CharField(max_length=4, default='4.0')
    subjectArea = models.CharField(max_length= 15)

    def __str__(self) -> str:
        return self.classId
    
class Lecture (models.Model):
    classId = models.CharField(max_length=50)
    classObj = models.ForeignKey(ClassObj, null=True, related_name='lectures', blank=True, on_delete=models.CASCADE)
    professors = models.CharField(max_length=200)
    def __str__ (self):
        return self.classId


class DiscussionSection(models.Model):
    discussionId = models.CharField(max_length=20, default='0')
    lectures = models.ForeignKey(Lecture, related_name='discussions', null=True, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.discussionId

class Time (models.Model):
    days = models.CharField(max_length=20)
    hours = models.CharField(max_length=20)
    lectureTime = models.ForeignKey(Lecture, related_name='times', null=True, on_delete=models.CASCADE, blank=True)
    discussionTime = models.ForeignKey(DiscussionSection, related_name='discussionTimes', null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.days 


# class UserFilters (models.Model):
#     # priorityClasses = ArrayField(model_container=ClassObj)
#     # ignoreClasses = ArrayField(model_container=ClassObj)
#     # user can choose multiple subject areas, shouldn't this be a list? 
#     # subjectArea = models(models.CharField(max_length=10, blank=True),size=8) 
#     subjectArea = models.CharField(max_length=100)
#     earliestStartTime = models.ManyToManyField(Time)
#     latestEndTime = models.ManyToManyField(Time)
#     preferreDays =  models.ManyToManyField(Time)
#     minClassRating = models.FloatField()
#     maxUnites = models.IntegerField(default=12)
#     numClasses = models.IntegerField(default=3)