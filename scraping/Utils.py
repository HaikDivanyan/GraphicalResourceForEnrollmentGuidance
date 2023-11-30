import json
from datetime import datetime

# class UserFilters:
#     def __init__(self, json_data):
#         # Assuming json_data is a dictionary obtained from json.loads(js_object)
#         self.priority_classes = json_data.get('priorityClasses', [])
#         self.ignored_classes = json_data.get('ignoredClasses', [])
#         self.subject_requirements = json_data.get('subjectRequirements', [])
#         self.genreq = json_data.get('genreq', None)
#         self.preferred_days = json_data.get('preferredDays', [])
#         self.latest_end_time = json_data.get('latestEndTime', None)
#         self.earliest_start_time = json_data.get('earliestStartTime', None)
#         self.min_class_rating = json_data.get('minClassRating', None)
#         self.max_units = json_data.get('maxUnits', None)
#         self.min_units = json_data.get('minUnits', None)
#         self.min_num_classes = json_data.get('minNumClasses', None)
#         self.max_num_classes = json_data.get('maxNumClasses', None)

#     @classmethod
#     def from_json(cls, json_string):
#         json_data = json.loads(json_string)
#         return cls(json_data)

class UserFilters:
    def __init__(self, preferred_days=None, latest_end_time=None, earliest_start_time=None, max_units=None, min_units=None, min_num_classes=None, max_num_classes=None):
        self.preferred_days = preferred_days
        self.latest_end_time = latest_end_time
        self.earliest_start_time = earliest_start_time
        self.max_units = max_units
        self.min_units = min_units
        self.min_num_classes = min_num_classes
        self.max_num_classes = max_num_classes
    
    def __str__(self) -> str:
        return f"preferred days: {self.preferred_days}\nearliest_start_time: {self.earliest_start_time}\nlatest_end_time: {self.latest_end_time}"
    
class ClassObject:
    def __init__(self, id, units, subject_area, rating, grade_distribution, hotseat_graph):
        self.id = id
        self.units = units
        self.subject_area = subject_area
        self.rating = rating
        self.grade_distribution = grade_distribution
        self.hotseat_graph = hotseat_graph

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            id=data_dict.get('id'),
            units=data_dict.get('units'),
            subject_area=data_dict.get('subjectArea'),
            rating=data_dict.get('rating'),
            grade_distribution=data_dict.get('gradeDistribution'),
            hotseat_graph=data_dict.get('hotseatGraph')
        )

def ensure_time_format(time_str):
    """
    Ensure that the time string is in the format of '%I:%M%p'.
    If minutes are missing, they will be added as ':00'.
    Example: '7am' becomes '7:00am', '12:30pm' remains '12:30pm'.
    """
    try:
        # First, try to parse it in the expected format
        datetime.strptime(time_str, '%I:%M%p')
        # If parsing succeeds, the format is already correct
        return time_str
    except ValueError:
        try:
            # If the initial parse fails, try to parse it without minutes
            new_time = datetime.strptime(time_str, '%I%p')
            # If this succeeds, format it to include zero minutes
            return new_time.strftime('%I:%M%p').lstrip('0').lower()
        except ValueError:
            # If it still fails, the format is not recognized
            raise ValueError(f"Time data '{time_str}' is not in a recognized format.")
    
def format_time_str(time_str):
    try:
        # Try parsing with the hour and minute
        return datetime.strptime(time_str, '%I:%M%p')
    except ValueError:
        # If it fails, it means the string doesn't have minutes
        return datetime.strptime(time_str, '%I%p')