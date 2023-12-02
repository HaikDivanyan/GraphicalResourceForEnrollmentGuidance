from datetime import datetime

from .Utils import ensure_time_format, format_time_str


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

    def __str__(self) -> str:
        return f"{self.days} {self.hours}"
    
    def overlaps_with(self, other_time):
        if set(self.days).isdisjoint(set(other_time.days)):
            return False  # The days do not overlap, so times cannot overlap

        # Parse the hours and check if the times overlap
        self_start, self_end = [format_time_str(t) for t in self.hours.split('-')]
        other_start, other_end = [format_time_str(t) for t in other_time.hours.split('-')]

        # Check for overlap
        return (self_start < other_end and self_end > other_start) or \
            (other_start < self_end and other_end > self_start)

    def is_within_time_range(self, start_time, end_time):
        # Ensure the input times are in the correct format
        start_time = ensure_time_format(start_time)
        end_time = ensure_time_format(end_time)
        
        # Parse the hours string into start and end times
        class_start_time, class_end_time = self.hours.split('-')
        class_start_time = ensure_time_format(class_start_time)
        class_end_time = ensure_time_format(class_end_time)
        
        # Convert to datetime objects for comparison
        class_start_time = datetime.strptime(class_start_time, '%I:%M%p')
        class_end_time = datetime.strptime(class_end_time, '%I:%M%p')
        start_time = datetime.strptime(start_time, '%I:%M%p')
        end_time = datetime.strptime(end_time, '%I:%M%p')

        # Check if the class times are within the user's acceptable time range
        return start_time <= class_start_time and class_end_time <= end_time

    def is_on_preferred_days(self, preferred_days):
        # Convert both sets of days to expanded lists
        class_days = list(self.days)
        preferred_days_list = list(preferred_days)

        # Check if the class days intersect with the preferred days
        return any(day in preferred_days_list for day in class_days)

class Professor:
    def __init__(self, name: str = None, rating: float = None):
        self.name = name
        self.rating = rating
    
    def __str__(self) -> str:
        return f"Professor: {self.name}, Rating: {self.rating}"

class DiscussionSection:
    def __init__(self, id: str = None, times: list[Time] = None):
        self.id = id
        self.times = times
    
    def __str__(self) -> str:
        times_str = ', '.join(str(time) for time in self.times)
        return f"Discussion Section ID: {self.id}, Times: [{times_str}]"

class Lecture:
    def __init__(self, id: str = None, times: list[Time] = None, discussions: list[DiscussionSection] = None, professors: list[str] = None):
        self.id = id
        self.times = times
        self.discussions = discussions
        self.professors = professors

    def __str__(self) -> str:
        times_str = ', '.join(str(time) for time in self.times)
        discussions_str = '\n    '.join(str(discussion) for discussion in self.discussions)
        professors_str = ', '.join(self.professors)
        # return f"Lecture ID: {self.id}\n    Times: {times_str}\n    Discussions:\n    {discussions_str}\n    Professors: {professors_str}"
        return f"Lecture ID: {self.id}\n    Times: {times_str}\n    Professors: {professors_str}"

class ClassObject:
    def __init__(self, id: str = None, units: int = None, subjectArea: str = None, rating: float = None, gradeDistributions: dict[list[int]] = None, hotseatGraph: str = None, lectures: list[Lecture] = None, name: str = None):
        self.id = id
        self.units = units
        self.subjectArea = subjectArea
        self.rating = rating
        self.gradeDistributions = gradeDistributions
        self.hosteatGraph = hotseatGraph
        self.lectures = lectures
        self.name = name
    
    def __str__(self) -> str:
        lectures_str = '\n'.join(str(lecture) for lecture in self.lectures)
        # grade_dist_str = ', '.join(f"{k}: {v}" for k, v in self.gradeDistributions.items())
        grade_dist_str = 'idk how to do this rn'
        return (
            f"Class ID: {self.id}\n"
            f"Name: {self.name}\n"
            f"Units: {self.units}\n"
            f"Subject Area: {self.subjectArea}\n"
            f"Rating: {self.rating}\n"
            f"Grade Distributions: {grade_dist_str}\n"
            f"Lectures:\n{lectures_str}"
        )

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