import re
from datetime import datetime


class PatternOne:
    def __init__(self, line):
        self.line = line

    def IsPatternOne(self):
        try:
            time_stamp = self.line[0:23]
            message_type = self.line.split()[2]
            return self.IsCorrectTimeStamp(time_stamp) and self.IsCorrectType(message_type)

        except:
            print("Not Pattern One")
            return False

    def IsCorrectTimeStamp(self, TimeStamp):
        try:
            date = TimeStamp.split()[0]
            time = TimeStamp.split()[1]

            date_to_match = re.compile(r'\d\d\d\d/\d\d/\d\d')
            time_to_match = re.compile(r'\d\d:\d\d:\d\d.\d\d\d')

            return date_to_match.match(date) and time_to_match.match(time)
        except:
            print("Not Pattern One")
            return False

#create a variable to check for a certain type ....
    def IsCorrectType(self, message_type):
        return message_type == "ERROR" or message_type == "WARN" or message_type == "INFO"

    def ConvertTimestamp(self, timestamp):
        try:
            date = timestamp.split()[0]
            time = timestamp.split()[1]

            return datetime.strptime(date, '%Y/%m/%d').strftime('%Y-%m-%d') + " " + time
        except:
            print("Trouble converting timestamp")

    def GetCurrentType(self):
        return self.line.split()[2]

    def GetTimeStamp(self):
        return self.line[0:23]

    def GetMessage(self):
        return self.line.split(self.GetCurrentType())[-1]


if __name__ == '__main__':
    Pattern = PatternOne("2020/06/19 21:41:49.537 WARN this message type is pattern one")
    Pattern.IsPatternOne()
