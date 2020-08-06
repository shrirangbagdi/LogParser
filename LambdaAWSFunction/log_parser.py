import os
import boto3

from LambdaAWSFunction.message import message


class Log_Parser:

    def __init__(self):
        pass

    def parse_file(self, event):
        s3 = boto3.resource("s3")
        file_obj = event["Records"][0]
        bucket_name = str(file_obj['s3']['bucket']['name'])
        file_name = str(file_obj['s3']['object']['key'])
        file_obj = s3.Object(bucket_name, file_name)

        if self.is_log(file_name) and file_name[-1] != "/" and (self.is_filled(file_obj)):
            case_id = self.get_id(file_name)
            parser = message(case_id, event)
            message_list = parser.generate_messages()
            return message_list

    def get_id(self, fileName):
        if "/" in fileName:
            return fileName.split("/")[0]
        else:
            return "No ID"

    def is_log(self, fileName):
        (file, ext) = os.path.splitext(fileName)

        return ext == ".log"

    def is_filled(self, fileObj):

        file_content = fileObj.get()["Body"].read().decode('utf-8')

        if file_content == "":
            return False

        return True


