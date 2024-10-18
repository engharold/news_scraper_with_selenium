from datetime import datetime, date
import calendar
from dateutil.relativedelta import relativedelta

class DateUtils(object):

    @staticmethod
    def get_current_date():
        return datetime.now()
    
    @staticmethod
    def get_current_date_formatted():
        return datetime.now().strftime("%m/%d/%Y")

    @staticmethod
    def format_date(date_to_format: datetime):
        return date_to_format.strftime("%m/%d/%Y")

    @staticmethod
    def get_beginning_of_month(reference_date: datetime):
        return date(reference_date.year, reference_date.month, 1).strftime("%m/%d/%Y")

    @staticmethod
    def get_last_day_of_month(year: int, month: int):
        return calendar.monthrange(year, month)[1]

    @staticmethod
    def calculate_start_date(reference_date: datetime, months: int):
        return datetime.strftime(reference_date - relativedelta(months=months), '%m/%d/%Y')
    