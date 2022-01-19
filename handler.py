# storage module for the project
from firebase_admin import storage
from firebase_admin import initialize_app
from firebase_admin import credentials
import os


# create class for uploading, downloading, and deleting files from firebase storage
class Storage_Handler:
    def __init__(self):
        # initialize firebase storage
        cred = credentials.Certificate(os.path.join(os.getcwd(), 'firebase-credentials.json'))
        self.storage = storage.initialize_app(cred)

    # upload file to firebase storage
    def upload(self, file_path, file_name):
        bucket = self.storage.bucket()
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_path)
        return blob.public_url

    # download file from firebase storage
    def download(self, file_name):
        bucket = self.storage.bucket()
        blob = bucket.blob(file_name)
        blob.download_to_filename(file_name)
        return file_name

    # delete file from firebase storage
    def delete(self, file_name):
        bucket = self.storage.bucket()
        blob = bucket.blob(file_name)
        blob.delete()
        return True


