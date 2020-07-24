#Pattern3="[2020-05-11T16:54:33,500][WARN ][o.e.m.j.JvmGcMonitorService] [unravel_s_1] [gc][1126797] overhead, spent [709ms] collecting in the last [1.2s]"

import re
from datetime import datetime


class PatternThree:
    def __init__(self, line):
        self.line = line

    def IsPatternThree(self):
        try:
            time_stamp = self.line[1:24]
            message_type = self.line[26:30]
            return self.IsCorrectTimeStamp(time_stamp) and self.IsCorrectType(message_type)

        except:
            print("Not Pattern Three")
            return False

    def IsCorrectTimeStamp(self, TimeStamp):
        try:
            date = TimeStamp[0:10]
            time = TimeStamp[11:23]
            character = TimeStamp[10]

            date_to_match = re.compile(r'\d\d\d\d-\d\d-\d\d')
            time_to_match = re.compile(r'\d\d:\d\d:\d\d,\d\d\d')

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
            time = TimeStamp[11:19]

            return date + " " + time + "." + TimeStamp[20:23]
        except:
            print("Error converting timestamp")

    def GetCurrentType(self):
        return self.line[26:30]

    def GetTimeStamp(self):
        return self.line[1:24]

    def GetMessage(self):
        return self.line[30:]


if __name__ == '__main__':
    Pattern = PatternThree("[2020-05-11T16:54:33,500][WARN ][o.e.m.j.JvmGcMonitorService] [unravel_s_1] [gc][1126797] overhead, spent [709ms] collecting in the last [1.2s]")
    print(Pattern.ConvertTimestamp("2020-05-11T16:54:33,500"))
