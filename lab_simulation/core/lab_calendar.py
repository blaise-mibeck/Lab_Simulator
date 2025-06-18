import datetime
import holidays

class LabCalendar:
    def __init__(self, country='US', state=None, work_hours_per_day=7, workdays=(0,1,2,3,4), holiday_list=None):
        self.work_hours_per_day = work_hours_per_day
        self.workdays = set(workdays)  # 0=Monday, 4=Friday
        self.holidays = set(holidays.country_holidays(country, state=state)) if holiday_list is None else set(holiday_list)

    def is_workday(self, date):
        return date.weekday() in self.workdays and date not in self.holidays

    def next_workday(self, date):
        next_day = date + datetime.timedelta(days=1)
        while not self.is_workday(next_day):
            next_day += datetime.timedelta(days=1)
        return next_day

    def add_work_minutes(self, start_datetime, minutes):
        dt = start_datetime
        minutes_left = minutes
        while minutes_left > 0:
            if not self.is_workday(dt.date()):
                dt = datetime.datetime.combine(self.next_workday(dt.date()), datetime.time(0,0))
                continue
            work_start = datetime.datetime.combine(dt.date(), datetime.time(9,0))
            work_end = work_start + datetime.timedelta(hours=self.work_hours_per_day)
            if dt < work_start:
                dt = work_start
            available_today = (work_end - dt).total_seconds() // 60
            if available_today <= 0:
                dt = datetime.datetime.combine(self.next_workday(dt.date()), datetime.time(9,0))
                continue
            work_this_day = min(minutes_left, available_today)
            dt += datetime.timedelta(minutes=work_this_day)
            minutes_left -= work_this_day
        return dt

    def work_minutes_between(self, start_datetime, end_datetime):
        dt = start_datetime
        total = 0
        while dt < end_datetime:
            if not self.is_workday(dt.date()):
                dt = datetime.datetime.combine(self.next_workday(dt.date()), datetime.time(9,0))
                continue
            work_start = datetime.datetime.combine(dt.date(), datetime.time(9,0))
            work_end = work_start + datetime.timedelta(hours=self.work_hours_per_day)
            if dt < work_start:
                dt = work_start
            if dt >= work_end:
                dt = datetime.datetime.combine(self.next_workday(dt.date()), datetime.time(9,0))
                continue
            next_dt = min(work_end, end_datetime)
            total += (next_dt - dt).total_seconds() // 60
            dt = next_dt
        return int(total)
