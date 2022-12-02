from datetime import date, timedelta, datetime


class DateUtil:

    @staticmethod
    def get_current_date() -> date:
        return date.today()

    @staticmethod
    def check_validity(date_str: str) -> bool:
        is_valid = False

        dt = datetime.strptime(date_str, '%d/%m/%y').date()
        current_date = DateUtil.get_current_date()

        if current_date <= dt:
            is_valid = True

        return is_valid

    @staticmethod
    def get_time_offset(days=0)-> date:
        current_time = DateUtil.get_current_date()
        offset_time = current_time + timedelta(days=days)

        return offset_time

    @staticmethod
    def get_string_from_date_object(date_obj: date) -> str:
        
        return date_obj.strftime("%d/%m/%y")

    @staticmethod
    def get_time_in_meridian(time_str: str) -> str:
        components = time_str.split(':')
        hour, minute = int(components[0], components[1])

        meridian= "AM" if hour< 12 else "PM"
        hour = hour-12 if meridian == "PM" else hour

        return str(hour) + ":" + str(minute) + " " + meridian
        

