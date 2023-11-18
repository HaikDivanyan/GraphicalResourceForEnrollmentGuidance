class SubRequirement:
    def __init__(self, name:str = None, classes: list[tuple[str, str]] = [], units: int = None, count: int = None):
        self.name = name
        self.classes = classes
        self.units = units
        self.count = count

class Requirement:
    def __init__(self, name: str = None, subrequirements: list[SubRequirement] = []):
        self.name = name
        self.subrequirements = subrequirements

class Time:
    def __init__(self, days: str = None, hours: str = None):
        self.days = days
        self.hours = hours

class Professor:
    def __init__(self, name: str = None, rating: float = None):
        self.name = name
        self.rating = float

class DiscussionSection:
    def __init__(self, id: str = None, time: Time = None):
        self.id = id
        self.time = Time

class Lecture:
    def __init__(self, id: str = None, time: Time = None, discussions: list[DiscussionSection] = None, professor: Professor = None):
        self.id = id
        self.time = time
        self.discussions = discussions
        self.professor = professor

class ClassObject:
    def __init__(self, id: str = None, units: int = None, subjectArea: str = None, rating: float = None, gradeDistribution: list[int] = None, hotseatGraph: str = None, lectures: list[Lecture] = None):
        self.id = id
        self.units = units
        self.subjectArea = subjectArea
        self.rating = rating
        self.gradeDistribution = gradeDistribution
        self.hosteatGraph = hotseatGraph
        self.lectures = lectures

class Dars:
    def __init__(self, requirements: list[Requirement] = None, classes: list[ClassObject] = None, professors: list[Professor] = None):
        self.requirements = requirements
        self.classes = classes
        self.professors = professors
