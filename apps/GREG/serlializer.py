from rest_framework import serializers
from .models import *

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = [ "name", "rating"]


class SubRequirementSerializer (serializers.ModelSerializer):
    class Meta:
        model = SubRequirement
        fields = ['name', 'units', 'count', 'classes']

class RequirementSerializer(serializers.ModelSerializer):
    subrequirements = SubRequirementSerializer(many=True)
    class Meta:
        model = Requirement
        fields = ['name', 'subrequirements']

class TimeSerializer (serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ['hours', 'days']

class DiscussionSerializer(serializers.ModelSerializer):
       discussionTimes = TimeSerializer(many=True)
       class Meta:
        model = DiscussionSection
        fields = ['discussionId', 'discussionTimes']

class LectureSerializer (serializers.ModelSerializer):
      times = TimeSerializer(many=True)
      discussions = DiscussionSerializer(many= True)
      class Meta:
        model = Lecture
        fields = ['classId', 'professors', 'times', 'discussions']

class ClassSerializer (serializers.ModelSerializer):
    lectures = LectureSerializer(many=True)
    class Meta:
        model = ClassObj
        fields = ['name', 'units', 'rating', 'subjectArea', 'gradeDistributions', 'hotseatGraph', 'classId', 'lectures']

class DarsSerializer (serializers.ModelSerializer):
    professors = ProfessorSerializer(many=True)
    requirements = RequirementSerializer(many=True)
    classes = ClassSerializer(many=True)
    class Meta:
        model = Dars
        fields = ['professors', 'requirements', 'classes']
