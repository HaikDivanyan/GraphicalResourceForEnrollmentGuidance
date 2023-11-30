from datetime import datetime
from itertools import combinations

import ScrapingDataStructures
from DataController import DataController
from ScheduleRanker import ScheduleRanker
from Utils import ClassObject, UserFilters


class ScheduleObject:
    def __init__(self, classes: ClassObject, rating: int):
        self.classes = classes
        self.rating = rating
    
    def __str__(self) -> str:
        class_info = '\n'.join([cls.name for cls in self.classes])
        return f"Schedule Rating: {self.rating}\nClasses:\n{class_info}"

class ScheduleGenerator:
    def __init__(self, dars: ScrapingDataStructures.Dars, user_filters: UserFilters):
        self.schedules = []
        self.dars = dars
        self.filters = user_filters
        self.preprocess_data()
        self.filtered_classes = [cls for cls in self.dars.classes if cls.lectures]
    
    def preprocess_data(self):
        incompatible_lectures = []
        for cls in self.dars.classes:
            lectures = cls.lectures
            for lecture in lectures:
                for time in lecture.times:
                    if not time.is_within_time_range(self.filters.earliest_start_time, self.filters.latest_end_time) \
                        or not time.is_on_preferred_days(self.filters.preferred_days):
                        incompatible_lectures.append(lecture)
                        break

        for lecture in incompatible_lectures:
            for cls in self.dars.classes:
                if lecture in cls.lectures:
                    cls.lectures.remove(lecture)
                if len(cls.lectures) == 0:
                    self.dars.classes.remove(cls)

    def check_time_conflict(self, schedule: ScheduleObject):
        all_times = []
        for cls in schedule.classes:
            for lecture in cls.lectures:
                for time in lecture.times:
                    all_times.append(time)

        for time1 in all_times:
            for time2 in all_times:
                if time1 != time2 and time1.overlaps_with(time2):
                    return True
        return False

    def generateSchedules(self):
        for combination in self.generate_combinations():
            schedule = ScheduleObject(combination, self.calculate_schedule_rating(combination))
            if not self.check_time_conflict(schedule):
                self.schedules.append(schedule)

        return self.schedules

    def generate_combinations(self):
        valid_combinations = []

        for r in range(self.filters.min_num_classes, self.filters.max_num_classes + 1):
            for combo in combinations(self.filtered_classes, r):
                total_units = sum(cls.units for cls in combo)

                if self.filters.min_units <= total_units <= self.filters.max_units:
                    valid_combinations.append(combo)

        return valid_combinations

    def calculate_schedule_rating(self, schedule):
        return ScheduleRanker.rank(schedule)

    def sort_schedules(self):
        self.schedules.sort(key=lambda x: x.rating, reverse=True)
        


if __name__ == "__main__":
    d = DataController()
    with open("../scraping test scripts/dar.html") as f:
        a = d.parseDar(f.read())

    filters = UserFilters(earliest_start_time='7am', latest_end_time='6pm', preferred_days=['TR'], min_num_classes=2, max_num_classes=4,
                        min_units=0, max_units=15)
    generator = ScheduleGenerator(dars=a, user_filters=filters)
    generator.generateSchedules()
    generator.sort_schedules()
    for s in generator.schedules:
        print(s)
        print('\n')
