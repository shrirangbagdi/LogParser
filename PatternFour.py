import re
from datetime import datetime

#"[2020-07-07T18:42:01.735] [INFO] ngui - com.unraveldata.ngui.topx.enabled :true"

class PatternFour:
    def __init__(self, line):
        self.line = line

    def IsPatternFour(self):
        try:
            time_stamp = self.line[1:24]
            message_type = self.line[27:31]
            message_type_two = self.line[27:32]
            return self.IsCorrectTimeStamp(time_stamp) and (self.IsCorrectType(message_type) or self.IsCorrectType(message_type_two))

        except:
            print("Not Pattern Three")
            return False

    def IsCorrectTimeStamp(self, TimeStamp):
        try:
            date = TimeStamp[0:10]
            time = TimeStamp[11:23]
            character = TimeStamp[10]

            date_to_match = re.compile(r'\d\d\d\d-\d\d-\d\d')
            time_to_match = re.compile(r'\d\d:\d\d:\d\d.\d\d\d')

            return date_to_match.match(date) and character == "T" and time_to_match.match(time)

        except:
            print("Not Pattern Three")
            return False

    # create a variable to check for a certain type ....
    def IsCorrectType(self, message_type):
        return message_type == "ERROR" or message_type == "WARN" or message_type == "INFO"

    def ConvertTimestamp(self, TimeStamp):
        try:
            date = TimeStamp[0:10]
            time = TimeStamp[11:23]

            return date + " " + time
        except:
            print("Error converting timestamp")

    def GetCurrentType(self):
        return self.line[26:30]

    def GetTimeStamp(self):
        return self.line[1:24]

    def GetMessage(self):
        return self.line[30:]

if __name__ == '__main__':
    Pattern = PatternFour("[2020-07-07T18:42:01.735] [ERROR] ngui - com.unraveldata.ngui.topx.enabled :true")
    (Pattern.IsPatternFour())
