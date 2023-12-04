import json
from itertools import combinations

# from ..models import ClassObj, Dars
from .DataController import DataController
from .ScheduleRanker import ScheduleRanker
from .ScrapingDataStructures import *
from .Utils import ScheduleObject, UserFilters


class ScheduleGenerator:
    def __init__(self, dars: Dars, user_filters: UserFilters):
        self.schedules = []
        self.dars = dars
        self.filters = user_filters
        self.priority_schedule = []
        self.filtered_classes = []
        self.preprocess_data()
        self.ranker = ScheduleRanker(self.dars, self.filters)
    
    def preprocess_data(self):
        # assuming priority classes cannot have time conflicts
        # assuming min_units < sum(priority class units) < max_units
        # assuming min_classes < sum(priority class units) < max_classes
        
        self.priority_schedule = []
        ignore_classes = []

        if self.filters.priority_classes:
            self.priority_schedule = [cls for cls in self.dars.classes if cls.id in self.filters.priority_classes]
        if self.filters.ignore_classes:
            ignore_classes = [cls for cls in self.dars.classes if cls.id in self.filters.ignore_classes]

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

        ignore_reqs = []
        if self.filters.ignore_reqs:
            for req in self.dars.requirements:
                for subreq in req.subrequirements:
                    if subreq.name in self.filters.ignore_reqs:
                        for cls_str in subreq.classes:
                            ignore_reqs.append(cls_str)

        filtered_classes = []
        for cls in self.dars.classes:
            if (cls.lectures and
            cls not in self.priority_schedule and
            cls not in ignore_classes and
            cls.id not in ignore_reqs):
                filtered_classes.append(cls)
        
        self.filtered_classes = filtered_classes

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

        # edge case: when len(priority classes) == len(max classes)
        if len(self.priority_schedule) == self.filters.max_num_classes:
            return [tuple(self.priority_schedule)]

        for r in range(self.filters.min_num_classes + len(self.priority_schedule), self.filters.max_num_classes + 1):
            for combo in combinations(self.filtered_classes, r):
                combo += tuple([cls for cls in self.priority_schedule])
                total_units = sum(cls.units for cls in combo)

                if self.filters.min_units <= total_units <= self.filters.max_units:
                    valid_combinations.append(combo)

        return valid_combinations

    def calculate_schedule_rating(self, schedule):
        h = self.ranker.rank(schedule)
        return h

    def sort_schedules(self):
        self.schedules.sort(key=lambda x: x.rating, reverse=True)

def main(dars: Dars, filters: UserFilters):
    # d = DataController()
    # with open("scraping test scripts/dar.html") as f:
    #     a = d.parseDar(f.read())

    print(filters)

    # com_sci_elective_subreq = "TWENTY UNITS OF AT LEAST 5 COMPUTER SCIENCE ELECTIVESFROM COMPUTER SCIENCE 111 THROUGH 188"


    # filters = UserFilters(earliest_start_time='7am', latest_end_time='6pm', min_num_classes=0, max_num_classes=4,
    #                     min_units=1, max_units=15, priority_reqs=[com_sci_elective_subreq], ignore_reqs=[], preferred_days="MTWR")

    # for req in dars.requirements:
    #     print("REQ")
    #     print(req.name)
    #     for subreq in req.subrequirements:
    #         print("SUBREQ")
    #         print(subreq.name)
    #         for cls in subreq.classes:
    #             print(cls)

    # filters.max_num_classes = 3
    generator = ScheduleGenerator(dars, filters)
    generator.generateSchedules()
    generator.sort_schedules()


    generator.schedules = generator.schedules[:5]

    schedule_dicts = [schedule.to_dict() for schedule in generator.schedules]

    # print(len(generator.schedules))
    # print("DONE")

    json_data = json.dumps(schedule_dicts)
    return json_data