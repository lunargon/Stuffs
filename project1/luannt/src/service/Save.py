import pandas as pd
import json
import os
from datetime import datetime
from google.cloud import storage
from src.static.CONST import BUCKET_NAME, logger

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'cert/fresher-training-02-72e1b9d25fb1.json'

class Save():
    def __init__(self) -> None:
        pass
    
    def save(self, data, path) -> None:
        pass

# The CsvSave class converts a list of data into a pandas dataframe and saves it as a CSV filewith a specified
# path or default path.
class CsvSave(Save):
    def save(self, data: list) -> any:
        try:
            # Change to Dataframe and write to file
            frame = pd.DataFrame(data)
            result = frame.to_csv(index=False), 'text/csv'
        except Exception as e:
            logger.exception(f"ERROR: {str(e)}")
        # return csv str and type of file
        return result 
    
# The JsonSave class is a subclass of Save that saves a list of data to a JSON file with a specified
# path or default path.
class JsonSave(Save):
    def save(self, data: list) -> any:
        try:
            # Covert data to json
            result = json.dumps(data, indent=4, ensure_ascii=False), 'application/json'
        except Exception as e:
            logger.exception(f"ERROR: {str(e)}")
        # return json str and type of file
        return result

# The GCloudStore class provides a method to upload data to a Google Cloud Storage bucket with a
# specified path and file name format.
class GCloudStore:
    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(BUCKET_NAME)

    def upload(self, data: list, saver: Save, path: str = None):
        try:
            # Get now time and convert to string
            now = datetime.now()
            time = now.strftime("%H_%M_%S_%d_%m_%Y")
            if len(path) == 0:
                path = ''
            elif path[-1] != "/":
                path += "/"

            data, save_format = saver.save(data)
            file_format = save_format.split('/')[1]
            # Set date time to file name to prevent dulicate
            self.bucket.blob(
                path+f"product_tiki_{time}.{file_format}"
            ).upload_from_string(data, save_format)
        except Exception as e:
            logger.exception(f"ERROR: {str(e)}")