import json
import os
import re

from datetime import datetime

from PatternFour import PatternFour
from PatternOne import PatternOne
from PatternThree import PatternThree


class FileParser:
    def __init__(self, logfile, destinationPathway, dateStart=0, dateEnd=0, pattern=""):
        self.logfile = logfile
        self.destinationPathway = destinationPathway
        self.dateStart = dateStart
        self.dateEnd = dateEnd
        self.pattern = pattern

    def ParseFile(self):
        list_of_warnings = self.GenerateWarnings()
        updated_list = self.UpdateWarningList(list_of_warnings)
        return updated_list

    # { "name" : "khilawar", "File_Name": "unravel_us_1.log","Type": "INFO", "timestamp" :"2020-06-19 21:39:30.568"}

    def GenerateWarnings(self):

        list_of_warnings = []
        log_file = open(self.logfile, 'r')
        previous_type = ""
        current_type = ""
        warning = {}
        first_iteration = True

        for line in log_file:
            pattern_one = PatternOne(line)
            pattern_three = PatternThree(line)
            pattern_four = PatternFour(line)

            # check if warning is first iteration later......
            if pattern_one.IsPatternOne():

                if (not first_iteration) and (previous_type == "WARN" or previous_type == "ERROR"):
                    list_of_warnings.append(warning)

                else:
                    first_iteration = False

                warning = {}
                current_type = pattern_one.GetCurrentType()

                if current_type == "WARN":
                    timestamp = pattern_one.GetTimeStamp()
                    message = pattern_one.GetMessage()
                    warning = {'File Name': self.GetLogFileName(), 'Timestamp': pattern_one.ConvertTimestamp(timestamp),
                               'Type': current_type, 'Message': message.strip()}

                if current_type == "ERROR":
                    timestamp = pattern_one.GetTimeStamp()
                    message = pattern_one.GetMessage()
                    warning = {'File Name': self.GetLogFileName(), 'Timestamp': pattern_one.ConvertTimestamp(timestamp),
                               'Type': current_type, 'Message': message.strip()}

                previous_type = current_type

            elif pattern_three.IsPatternThree():

                if (not first_iteration) and (previous_type == "WARN" or previous_type == "ERROR"):
                    list_of_warnings.append(warning)

                else:
                    first_iteration = False

                warning = {}
                current_type = pattern_three.GetCurrentType()

                if current_type == "WARN":
                    timestamp = pattern_three.GetTimeStamp()
                    message = pattern_three.GetMessage()
                    warning = {'File Name': self.GetLogFileName(),
                               'Timestamp': pattern_three.ConvertTimestamp(timestamp),
                               'Type': current_type, 'Message': message.strip()}

                if current_type == "ERROR":
                    timestamp = pattern_three.GetTimeStamp()
                    message = pattern_three.GetMessage()
                    warning = {'File Name': self.GetLogFileName(),
                               'Timestamp': pattern_three.ConvertTimestamp(timestamp),
                               'Type': current_type, 'Message': message.strip()}

                previous_type = current_type


            elif pattern_four.IsPatternFour():

                if (not first_iteration) and (previous_type == "WARN" or previous_type == "ERROR"):
                    list_of_warnings.append(warning)

                else:
                    first_iteration = False

                warning = {}
                current_type = pattern_three.GetCurrentType()

                if current_type == "WARN":
                    timestamp = pattern_four.GetTimeStamp()
                    message = pattern_four.GetMessage()
                    warning = {'File Name': self.GetLogFileName(),
                               'Timestamp': pattern_three.ConvertTimestamp(timestamp),
                               'Type': current_type, 'Message': message.strip()}

                if current_type == "ERROR":
                    timestamp = pattern_four.GetTimeStamp()
                    message = pattern_four.GetMessage()
                    warning = {'File Name': self.GetLogFileName(),
                               'Timestamp': pattern_three.ConvertTimestamp(timestamp),
                               'Type': current_type, 'Message': message.strip()}

                previous_type = current_type


            elif previous_type == "WARN" or previous_type == "ERROR":
                warning["Message"] += line

        if previous_type == "ERROR" or previous_type == "WARN":
            list_of_warnings.append(warning)

        return list_of_warnings

    def UpdateWarningList(self, listOfWarnings):
        if (self.dateStart == 0 or self.dateEnd == 0) and self.pattern == "":
            self.CreateJsonFile(listOfWarnings)
            return listOfWarnings
        elif not self.pattern == "":
            updated_list = self.FindWarningsWithPattern(listOfWarnings)
            self.CreateJsonFile(updated_list)
            return updated_list
        elif not (self.dateStart == 0 or self.dateStart == 0):
            updated_list = self.FindWarningsWithDate(listOfWarnings)
            self.CreateJsonFile(updated_list)
            return updated_list
        return listOfWarnings

    def FindWarningsWithPattern(self, listOfWarnings):
        updated_list = []
        pattern = self.pattern.lower()
        for dictionaries in listOfWarnings:
            if pattern in dictionaries["Message"].lower():
                updated_list.append(dictionaries)
        return updated_list

    def FindWarningsWithDate(self, listOfWarnings):
        updated_list = []
        start_date = datetime.strptime(self.dateStart, '%Y/%m/%d')
        end_date = datetime.strptime(self.dateEnd, '%Y/%m/%d')

        for dictionaries in listOfWarnings:
            date_to_compare = datetime.strptime(dictionaries["Date"], '%Y-%m-%d')
            if start_date < date_to_compare < end_date:
                updated_list.append(dictionaries)

        return updated_list

    def CreateJsonFile(self, listOfWarnings):
        now = datetime.now()
        if listOfWarnings:
            with open(self.destinationPathway + self.GetJsonFileName() + " " + now.strftime("%Y-%m-%d %H:%M:%S") + '.json', 'w') as log_file:
                log_file.write('[' + ',\n'.join(json.dumps(i) for i in listOfWarnings) +
                               ']\n')

                # json.dump(listOfWarnings, log_file, indent=0)

    def GetJsonFileName(self):
        absolute_file_pathway = self.logfile

        (file, ext) = os.path.splitext(absolute_file_pathway)

        return file.split('/')[-1]

    def GetLogFileName(self):
        absolute_file_pathway = self.logfile

        (file, ext) = os.path.splitext(absolute_file_pathway)

        return file.split('/')[-1] + ext


if __name__ == '__main__':
    Parser = FileParser('/Users/shrirangbagdi/Desktop/f.log', "/Users/shrirangbagdi/Desktop/")
    # Parser = FileParser('/home/ec2-user/logdata', "/Users/shrirangbagdi/Desktop/")
    Parser.ParseFile()
