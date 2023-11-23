class SubRequirement:
    def __init__(self, name:str = None, classes: list[str] = None, units: int = None, count: int = None):
        self.name = name
        self.classes = classes
        self.units = units
        self.count = count

class Requirement:
    def __init__(self, name: str = None, subrequirements: list[SubRequirement] = None):
        self.name = name
        self.subrequirements = subrequirements

class Time:
    def __init__(self, days: str = None, hours: str = None):
        self.days = days
        self.hours = hours

class Professor:
    def __init__(self, name: str = None, rating: float = None):
        self.name = name
        self.rating = rating

class DiscussionSection:
    def __init__(self, id: str = None, times: list[Time] = None):
        self.id = id
        self.times = times

class Lecture:
    def __init__(self, id: str = None, times: list[Time] = None, discussions: list[DiscussionSection] = None, professors: list[str] = None):
        self.id = id
        self.times = times
        self.discussions = discussions
        self.professors = professors

class ClassObject:
    def __init__(self, id: str = None, units: int = None, subjectArea: str = None, rating: float = None, gradeDistribution: list[int] = None, hotseatGraph: str = None, lectures: list[Lecture] = None, name: str = None):
        self.id = id
        self.units = units
        self.subjectArea = subjectArea
        self.rating = rating
        self.gradeDistribution = gradeDistribution
        self.hosteatGraph = hotseatGraph
        self.lectures = lectures
        self.name = name

class Dars:
    def __init__(self, requirements: list[Requirement] = None, classes: list[ClassObject] = None, professors: list[Professor] = None):
        self.requirements = requirements
        self.classes = classes
        self.professors = professors

class RegistrarData:
    def __init__(self, classId: str = None, className: str = None, units: int = None, subjectArea: str = None, lectures: list[Lecture] = None):
        self.classId = classId
        self.className = className
        self.units = units
        self.subjectArea = subjectArea
        self.lectures = lectures