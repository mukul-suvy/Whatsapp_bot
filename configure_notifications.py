#custom imports

from csv_utils import CSVUtil
from datetime_utils import DateUtil
from request_utils import RequestUtils


class NotificationsMixin:

    def __init__(self, path_to_records_csv: str, path_to_schedule_csv: str) -> None:
        self.record_list = CSVUtil.read_csv_file_to_list_of_dict(path_to_records_csv)
        self.schedule_list = CSVUtil.read_csv_file_to_list_of_dict(path_to_schedule_csv)

    def configure_schedule_mapping(self) -> dict:
        schedule_mapping_today = {}

        now = DateUtil.get_current_date()
        today = DateUtil.get_string_from_date_object(now)

        for schedule in self.schedule_list:
            if schedule['date'] == today:
                standard = schedule['standard']
                subject = schedule['subject']

                if standard not in schedule_mapping_today.keys():
                    schedule_mapping_today[standard] = {}
                
                if subject not in schedule_mapping_today[standard].keys():
                    schedule_mapping_today[standard][subject]= {}

                schedule_mapping_today[standard][subject].update({
                    'link': schedule['link'],
                    'date': schedule['date'],
                    'time': schedule['time'],
                    'session': schedule['session']
                })
        return schedule_mapping_today

    def get_notifications_metadata_mapping_using_configs(self) -> dict:
        notifications_metadata_mapping = {}

        schedule_mapping = self.configure_schedule_mapping()

        standards = schedule_mapping.keys()

        for student_record in self.record_list:
            student_id = student_record['sid']
            student_name = student_record['name']
            student_standard = student_record['standard']
            student_phone_number = student_record['phone_number']
            student_subjects = eval(student_record['subjects'])

            student_is_valid = DateUtil.check_validity(student_record['validity'])

            if student_is_valid:
                if student_standard in standards:
                    subject_taught_today = schedule_mapping[student_standard].keys()

                    for subject in student_subjects:
                        if subject in subject_taught_today:
                            notifications_metadata_mapping[student_id] = {
                                'standard': student_standard,
                                'phone_number': RequestUtils.configure_number_with_country_code(student_phone_number),
                                'subjects': {
                                    subject:{
                                        'session': schedule_mapping[student_standard][subject]['session'],
                                        'time' : schedule_mapping[student_standard][subject]['time'],
                                        'link': schedule_mapping[student_standard][subject]['link']
                                    }
                                }
                            }
            else:
                print(f"Student :  {student_id} {student_name}'s validity expired.")

        return notifications_metadata_mapping

   