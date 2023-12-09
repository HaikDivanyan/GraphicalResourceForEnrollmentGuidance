"""
This module provides functionality for generating and ranking possible class schedules based on user preferences and constraints.
"""
import json
from itertools import combinations

from .DataController import DataController
from .ScheduleRanker import ScheduleRanker
from .ScrapingDataStructures import *
from .Utils import ScheduleObject, UserFilters

DEBUG = False

class ScheduleGenerator:
    """
    ScheduleGenerator is responsible for generating all possible class schedules
    that fit the given criteria outlined in Dars and UserFilters.
    """
    def __init__(self, dars: Dars, user_filters: UserFilters):
        """
        Initializes the ScheduleGenerator with DARS data and user-specified filters.
        
        :param dars: An instance of Dars containing class and requirement information.
        :param user_filters: An instance of UserFilters containing user preferences.
        """
        self.schedules = []
        self.dars = dars
        self.filters = user_filters
        self.priority_schedule = []
        self.filtered_classes = []
        self.preprocess_data()
        self.ranker = ScheduleRanker(self.dars, self.filters)
    
    def preprocess_data(self):
        """
        Preprocesses the DARS data to apply filters and prioritize classes before schedule generation.
        """
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
                if self.filters.min_class_rating > 0:
                    if cls.rating and cls.rating >= self.filters.min_class_rating:
                        filtered_classes.append(cls)
                else:
                    filtered_classes.append(cls)

        for cls in filtered_classes:
            cls.lectures = [cls.lectures[0]]
        self.filtered_classes = filtered_classes

    def check_time_conflict(self, schedule: ScheduleObject):
        """
        Checks a given schedule for any time conflicts between classes.
        
        :param schedule: A ScheduleObject representing a potential schedule.
        :return: Boolean value indicating whether a time conflict exists.
        """
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
        """
        Generates all possible schedules based on filtered and prioritized class data.
        
        :return: A list of ScheduleObjects representing all valid schedules.
        """
        for combination in self.generate_combinations():
            schedule = ScheduleObject(combination, self.calculate_schedule_rating(combination))
            if not self.check_time_conflict(schedule):
                self.schedules.append(schedule)

        return self.schedules

    def generate_combinations(self):
        """
        Generates all valid combinations of classes that meet the filtering criteria.
        
        :return: A list of tuples, each representing a valid class combination.
        """
        valid_combinations = []

        # edge case: when len(priority classes) == len(max classes)
        if len(self.priority_schedule) == self.filters.max_num_classes:
            return [tuple(self.priority_schedule)]

        for r in range(self.filters.min_num_classes + len(self.priority_schedule), self.filters.max_num_classes):
            for combo in combinations(self.filtered_classes, r):
                combo += tuple([cls for cls in self.priority_schedule])
                total_units = sum(cls.units for cls in combo)

                if self.filters.min_units <= total_units <= self.filters.max_units:
                    valid_combinations.append(combo)

        return valid_combinations

    def calculate_schedule_rating(self, schedule):
        """
        Calculates the rating for a given schedule based on various metrics.
        
        :param schedule: A tuple of ClassObjects representing a schedule.
        :return: A numerical rating for the schedule.
        """
        h = self.ranker.rank(schedule)
        return h

    def sort_schedules(self):
        """
        Sorts the generated schedules in place by their ratings in descending order.
        """
        self.schedules.sort(key=lambda x: x.rating, reverse=True)

def main(dars: Dars, filters: UserFilters):
    """
    Main function to generate and sort schedules given DARS data and user filters.
    
    :param dars: An instance of Dars containing class and requirement information.
    :param filters: An instance of UserFilters containing user preferences.
    :return: JSON string of the sorted schedules.
    """
    filters.earliest_start_time = "9am"
    filters.latest_end_time = "8pm"
    generator = ScheduleGenerator(dars, filters)
    generator.generateSchedules()
    generator.sort_schedules()

    schedule_dicts = [schedule.to_dict() for schedule in generator.schedules]

    if DEBUG:
        run_tests(schedule_dicts, filters)

    json_data = json.dumps(schedule_dicts)
    return json_data

def run_tests(schedule_dicts, filters):
    """
    Runs a series of tests on the generated schedules to ensure they meet specified criteria.
    
    :param schedule_dicts: A list of dictionaries, each representing a schedule.
    :param filters: An instance of UserFilters containing user preferences.
    """
    # write tests to ensure that the schedules are sorted correctly
    for i in range(len(schedule_dicts) - 1):
        assert schedule_dicts[i]['rating'] >= schedule_dicts[i+1]['rating']
    
    # write tests to ensure that the schedules do not have time conflicts
    for schedule in schedule_dicts:
        for cls in schedule['classes']:
            for lecture in cls['lectures']:
                for time in lecture['times']:
                    assert time['start_time'] < time['end_time']
                    assert time['start_time'] >= filters.earliest_start_time
                    assert time['end_time'] <= filters.latest_end_time
                    assert time['days'] in filters.preferred_days

    # write tests to ensure if a user specifies a priority class, then that class is in the schedule
    for schedule in schedule_dicts:
        if filters.priority_classes:
            priority_classes = [cls for cls in schedule['classes'] if cls['id'] in filters.priority_classes]
            assert priority_classes

    # write tests to ensure that the schedule has the correct number of classes
    for schedule in schedule_dicts:
        assert filters.min_num_classes <= len(schedule['classes']) <= filters.max_num_classes
    
    # write tests to ensure that the schedule has the correct number of units
    for schedule in schedule_dicts:
        total_units = sum(cls['units'] for cls in schedule['classes'])
        assert filters.min_units <= total_units <= filters.max_units