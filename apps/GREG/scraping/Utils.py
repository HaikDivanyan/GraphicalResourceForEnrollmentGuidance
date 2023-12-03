from datetime import datetime


class ScheduleObject:
    def __init__(self, classes, rating: int):
        self.classes = classes
        self.rating = rating

    def to_dict(self):
        return {
            "classes": [cls.to_dict() for cls in self.classes],
            "rating": self.rating,
        }
    
    def __str__(self) -> str:
        class_info = '\n'.join([cls.name for cls in self.classes])
        return f"Schedule Rating: {self.rating}\nClasses:\n{class_info}"

class UserFilters:
    def __init__(self, 
                preferred_days="MTWRF", latest_end_time='11pm', earliest_start_time='6am',
                max_units=12, min_units=2, min_num_classes=1, max_num_classes=4,
                priority_classes=None, ignore_classes=None, priority_reqs=None, ignore_reqs=None,
                min_class_rating = 0, subject=None):
        self.priority_classes = priority_classes
        self.ignore_classes = ignore_classes
        self.priority_reqs = priority_reqs
        self.ignore_reqs = ignore_reqs
        self.subject = subject
        self.preferred_days = preferred_days
        self.latest_end_time = latest_end_time
        self.earliest_start_time = earliest_start_time
        self.max_units = max_units
        self.min_units = min_units
        self.min_num_classes = min_num_classes
        self.max_num_classes = max_num_classes
        self.min_class_rating = min_class_rating
    
    def __str__(self) -> str:
        return f"preferred days: {self.preferred_days}\nearliest_start_time: {self.earliest_start_time}\nlatest_end_time: {self.latest_end_time}"

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