class ScheduleRanker:
    @staticmethod
    def rank(schedule):
        ranking = 0
        for cls in schedule:
            ranking += cls.rating
        return ranking  # return the ranking instead of setting it directly