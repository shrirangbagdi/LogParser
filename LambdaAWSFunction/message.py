import boto3

from PatternFour import PatternFour
from PatternOne import PatternOne
from PatternThree import PatternThree


class message:

    def __init__(self, caseID, event):
        self.caseID = caseID
        self.event = event

    def generate_messages(self):
        s3 = boto3.client('s3')
        list_of_messages = []
        warning = {}
        event = self.event

        file_name = str(event['Records'][0]['s3']['object']['key'])

        bucket = str(event['Records'][0]['s3']['bucket']['name'])
        obj = s3.get_object(Bucket=bucket, Key=file_name)

        previous_type = ""
        first_iteration = True

        for line in obj["Body"].read().decode(encoding="utf-8").splitlines():
            pattern_one = PatternOne(line)
            pattern_three = PatternThree(line)
            pattern_four = PatternFour(line)

            if pattern_one.IsPatternOne():
                if (not first_iteration) and (previous_type == "WARN" or previous_type == "ERROR"):
                    list_of_messages.append(warning)

                else:
                    first_iteration = False

                warning = {}
                current_type = pattern_one.GetCurrentType()

                if current_type == "WARN":
                    timestamp = pattern_one.GetTimeStamp()
                    message = pattern_one.GetMessage()
                    warning = {'File Name': file_name, 'Case ID': self.caseID,
                               'Timestamp': pattern_one.ConvertTimestamp(timestamp),
                               'Type': current_type, 'Message': message.strip()}

                if current_type == "ERROR":
                    timestamp = pattern_one.GetTimeStamp()
                    message = pattern_one.GetMessage()
                    warning = {'File Name': file_name, 'Case ID': self.caseID,
                               'Timestamp': pattern_one.ConvertTimestamp(timestamp),
                               'Type': current_type, 'Message': message.strip()}

                previous_type = current_type
            elif pattern_three.IsPatternThree():

                if (not first_iteration) and (previous_type == "WARN" or previous_type == "ERROR"):
                    list_of_messages.append(warning)

                else:
                    first_iteration = False

                warning = {}
                current_type = pattern_three.GetCurrentType()

                if current_type == "WARN":
                    timestamp = pattern_three.GetTimeStamp()
                    message = pattern_three.GetMessage()
                    warning = {'File Name': file_name, 'Case ID': self.caseID,
                               'Timestamp': pattern_three.ConvertTimestamp(timestamp),
                               'Type': current_type, 'Message': message.strip()}

                if current_type == "ERROR":
                    timestamp = pattern_three.GetTimeStamp()
                    message = pattern_three.GetMessage()
                    warning = {'File Name': file_name, 'Case ID': self.caseID,
                               'Timestamp': pattern_three.ConvertTimestamp(timestamp),
                               'Type': current_type, 'Message': message.strip()}

                previous_type = current_type
            elif pattern_four.IsPatternFour():

                if (not first_iteration) and (previous_type == "WARN" or previous_type == "ERROR"):
                    list_of_messages.append(warning)

                else:
                    first_iteration = False

                warning = {}
                current_type = pattern_four.GetCurrentType()

                if current_type == "WARN":
                    timestamp = pattern_four.GetTimeStamp()
                    message = pattern_four.GetMessage()
                    warning = {'File Name': file_name, 'Case ID': self.caseID,
                               'Timestamp': pattern_four.ConvertTimestamp(timestamp),
                               'Type': current_type, 'Message': message.strip()}

                if current_type == "ERROR":
                    timestamp = pattern_four.GetTimeStamp()
                    message = pattern_four.GetMessage()
                    warning = {'File Name': file_name, 'Case ID': self.caseID,
                               'Timestamp': pattern_four.ConvertTimestamp(timestamp),
                               'Type': current_type, 'Message': message.strip()}

                previous_type = current_type

            elif previous_type == "WARN" or previous_type == "ERROR":
                warning["Message"] += line

        if previous_type == "ERROR" or previous_type == "WARN":
            list_of_messages.append(warning)

        return list_of_messages