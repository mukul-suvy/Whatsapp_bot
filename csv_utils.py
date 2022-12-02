import os
import csv
import logging
from typing import Dict, List


class CSVUtil:

    @staticmethod
    def read_csv_file_to_list_of_dict(source: str) -> List[dict]:
        try:
            if os.path.exists(path=source):
                with open(source) as file:
                    records = [{key: value for key, value in row.items()} for row in csv.DictReader(file, skipinitialspace=True)]
                
                return records
            else:
                raise ValueError("File missing : " + source)

        except Exception as ex:
            logging.error("Exception occured while reading CSV file : "+str(ex))

class CSVSanitizer:
    pass