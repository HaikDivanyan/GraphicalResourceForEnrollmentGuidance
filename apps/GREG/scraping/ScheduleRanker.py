from datetime import timedelta

from ..models import ClassObj, Dars
from .Utils import ScheduleObject, UserFilters, format_time_str


class ScheduleRanker:
    def __init__(self, dars: Dars, filters: UserFilters):
        self.dars = dars
        self.filters = filters

    def rank(self, schedule):
        ranking = 0
        for cls in schedule:
            if cls.rating:
                ranking += cls.rating
            if self.is_priority_subreq(cls):
                ranking += 10
            if self.filters.subject and cls.subjectArea in self.filters.subject:
                ranking += 10

        time_gap = self.calculate_time_gap_bonus(schedule)
        ranking += time_gap

        class_consolidation_bonus = self.calculate_class_consolidation_bonus(schedule)
        ranking += class_consolidation_bonus

        return ranking

    def calculate_time_gap_bonus(self, schedule):
        if len(schedule) == 1:
            return 0
        
        day_gaps = {}
        for cls in schedule:
            for lecture in cls.lectures:
                for time in lecture.times:
                    start_time, end_time = [format_time_str(t) for t in time.hours.split('-')]
                    day_gaps.setdefault(time.days, []).append((start_time, end_time))

        total_bonus = 0
        for day, times in day_gaps.items():
            times.sort()
            daily_gaps = [times[i+1][0] - times[i][1] for i in range(len(times)-1)]
            if daily_gaps:
                avg_gap = sum(daily_gaps, timedelta()) / len(daily_gaps)

                # Assign bonuses based on average gap
                if avg_gap <= timedelta(minutes=30):
                    total_bonus += 3
                elif avg_gap <= timedelta(hours=1):
                    total_bonus += 2
                elif avg_gap <= timedelta(hours=2):
                    total_bonus += 1
                # Over 2 hours gap gets no additional bonus

        return total_bonus

    def calculate_class_consolidation_bonus(self, schedule: ScheduleObject):
        days_with_classes = set()
        for cls in schedule:
            for lecture in cls.lectures:
                for time in lecture.times:
                    days_with_classes.update(time.days)

        # Calculate the bonus based on the number of unique days
        num_unique_days = len(days_with_classes)
        num_classes = len(schedule)

        bonus = (num_classes / num_unique_days) if num_unique_days > 0 else 0
        return bonus

    def is_priority_subreq(self, cls: ClassObj):
        if not self.filters.priority_reqs:
            return False
        for req in self.dars.requirements:
            for subreq in req.subrequirements:
                if subreq.name in self.filters.priority_reqs:
                    for c in subreq.classes:
                        if cls.id == c:
                            return True
        return False