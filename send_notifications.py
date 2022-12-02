#library imports
import requests
import logging
import configparser

#custom imports
from datetime_utils import DateUtil
from request_utils import RequestUtils
from configure_notifications import NotificationsMixin


class Notifications:
    def __init__(self, phone_number_id: str, bearer_token: str, api_version: str) -> None:
        self.api_endpoint = RequestUtils.configure_api_endpoint(api_version, phone_number_id)
        self.request_headers = RequestUtils.configure_headers(bearer_token)
        self.current_date = DateUtil.get_string_from_date_object(DateUtil.get_current_date())

    def configure_message_body(self, phone_number: str, standard: str, subject: str, session: str, date: str, time: str, link: str):
        return {"messaging_product": "whatsapp", "to": "918937085705", "type": "template", "template": {"name": "hello_world", "language": {"code": "en_US"}}}

    def get_metadata_mappings_using_configs(self):

        #configure students records file path
        student_records_config = configparser.ConfigParser()
        student_records_config.read('records.ini')

        student_record_base_path = student_records_config['location']['path'] + '/'  if student_records_config['location']['path'][-1] != '/' else student_records_config['location']['path']

        student_record_file_path = student_record_base_path + student_records_config['location']['filename']

        #configure schedule path
        schedule_config = configparser.ConfigParser()
        schedule_config.read('schedule.ini')

        schedule_base_path = schedule_config['location']['path'] + '/' if schedule_config['location']['path'][-1] != '/' else schedule_config['location']['path']

        schedule_file_path = schedule_base_path + schedule_config['location']['filename']

        # Creation of Mixin Classes
        mixin = NotificationsMixin(student_record_file_path, schedule_file_path)
        notifications_metadata_mapping = mixin.get_notifications_metadata_mapping_using_configs()

        return notifications_metadata_mapping

    def send_notifications(self):
        notifications_metadata_mapping= self.get_metadata_mappings_using_configs()

        for sid in notifications_metadata_mapping.keys():
            for subject in notifications_metadata_mapping[sid]['subjects']:
                student_phone_number = notifications_metadata_mapping[sid]['phone_number']
                student_standard = notifications_metadata_mapping[sid]['standard']
                session = notifications_metadata_mapping[sid]['subjects'][subject]['session']
                class_time = notifications_metadata_mapping[sid]['subjects'][subject]['time']
                class_link = notifications_metadata_mapping[sid]['subjects'][subject]['link']

                message_body = self.configure_message_body(phone_number=student_phone_number, standard=student_standard, subject=subject, session=session, date=self.current_date, time=class_time, link=class_link)

                response = requests.post(url=self.api_endpoint, json=message_body, headers=self.request_headers)

                if response.status_code not in [200, 201]:
                    logging.error("Unwanted code : " + str(response.status_code))

                else:
                    print(f"Message successfully delivered : {sid} for {student_standard} {subject} {class_time}")


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('credentials.ini')

    phone_number_id = config['service_secrets']['phone_number_id']
    bearer_token = config['service_secrets']['bearer_token']
    api_version = config['service_secrets']['api_version']

    notification = Notifications(phone_number_id, bearer_token, api_version)
    notification.send_notifications()