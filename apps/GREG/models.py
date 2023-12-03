from django import forms
from django.core.validators import int_list_validator
from django.db import models


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class Dars(models.Model):
    def __str__(self):
        return 'dars'
    
class Schedule (models.Model):
    rating = models.FloatField() #could use ManytoManyField which creates schedule-class table 
    classes = models.ManyToManyField('ClassObj', related_name='schedules')

    def __str__(self):
        return self.rating
    
class ClassObj (models.Model):
    dars = models.ForeignKey(Dars,related_name= 'classes', on_delete=models.CASCADE )
    units = models.CharField(max_length=4, default='4.0')
    subjectArea = models.CharField(max_length= 15)
    rating = models.FloatField(null=True)
    gradeDistributions = models.CharField(validators=[int_list_validator], max_length=12, null = True) 
    hotseatGraph = models.CharField(max_length=100, null=True, blank=True)
    classId = models.CharField(max_length=25) # double check the max length
    name = models.CharField(max_length= 150)
    # schedules= models.ManyToManyField(Schedule, related_name='classes', null=True)
    def __str__(self):
        return self.name

class Requirement(models.Model):
    dars = models.ForeignKey(Dars,related_name= 'requirements', on_delete=models.CASCADE )
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name

class SubRequirement(models.Model):
    name = models.CharField(max_length= 150)
    units = models.IntegerField( null=True)
    count = models.IntegerField(null=True)
    subrequirements = models.ForeignKey(Requirement, related_name='subrequirements', on_delete=models.CASCADE, null=True)
    classes = models.CharField(max_length=200, blank=True, default='')
    def __str__(self) -> str:
        return self.name

class Professor (models.Model):
    dars = models.ForeignKey(Dars,related_name= 'professors', on_delete=models.CASCADE )
    rating = models.FloatField(null=True)
    name = models.CharField(max_length=90, null=True)

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


class UserFilters(models.Model):
    priorityClasses = models.CharField(max_length=500, null=True, blank=True)
    ignoreClasses = models.CharField(max_length=500, null=True, blank=True)
    priorityRequirements = models.CharField(max_length=500, null=True, blank=True)
    ignoreRequirements = models.CharField(max_length=500, null=True, blank=True)
    # Assuming preferredSubjects corresponds to 'subject' in the Python class
    preferredSubjects = models.CharField(max_length=500, null=True, blank=True)
    earliestStartTime = models.CharField(max_length=10, null=True, blank=True, default='6am')
    latestEndTime = models.CharField(max_length=10, null=True, blank=True, default='11pm')
    preferredDays = models.CharField(max_length=500, null=True, blank=True, default="MTWRF")
    minClassRating = models.FloatField(null=True, blank=True)
    maxUnits = models.IntegerField(null=True, blank=True, default=12)
    minUnits = models.IntegerField(null=True, blank=True, default=2)
    minNumClasses = models.IntegerField(null=True, blank=True, default=1)
    maxNumClasses = models.IntegerField(null=True, blank=True, default=4)