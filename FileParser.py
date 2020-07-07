import json
import os
import re

from datetime import datetime


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

    def GenerateWarnings(self):
        list_of_warnings = []
        log_file = open(self.logfile, 'r')
        previous_type = ""
        warning = {}
        first_iteration = True
        first_phrase = 0
        second_phrase = 1
        third_phrase = 2

        for line in log_file:
            if self.StartsCorrectly(line):
                current_type = line.split()[third_phrase]

                if (not first_iteration) and ((previous_type == "WARN") or (previous_type == "ERROR")):
                    list_of_warnings.append(warning)
                    warning = {}

                if current_type == "WARN":
                    line_list = line.split()
                    date = line_list[first_phrase]
                    time = line_list[second_phrase]
                    message = line.split("WARN")[second_phrase]

                    warning = {'File Name': self.GetLogFileName(), 'Date': date, 'Time': time, 'Type': current_type,
                               'Message': message.strip()}
                    first_iteration = False

                if current_type == "ERROR":
                    line_list = line.split()
                    date = line_list[first_phrase]
                    time = line_list[second_phrase]
                    message = line.split("ERROR")[second_phrase]

                    warning = {'File Name': self.GetLogFileName(), 'Date': date,
                               'Time': time, 'Type': current_type,
                               'Message': message}
                    first_iteration = False

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
            date_to_compare = datetime.strptime(dictionaries["Date"], '%Y/%m/%d')
            if start_date < date_to_compare < end_date:
                updated_list.append(dictionaries)

        return updated_list

    def CreateJsonFile(self, listOfWarnings):
        if listOfWarnings:
            with open(self.destinationPathway + self.GetJsonFileName() + '.json', 'w') as log_file:
                json.dump(listOfWarnings, log_file, indent=4)

    def GetJsonFileName(self):
        absolute_file_pathway = self.logfile

        (file, ext) = os.path.splitext(absolute_file_pathway)

        return file.split('/')[-1]

    def GetLogFileName(self):
        absolute_file_pathway = self.logfile

        (file, ext) = os.path.splitext(absolute_file_pathway)

        return file.split('/')[-1] + ext

    def StartsCorrectly(self, line):
        first_phrase = 0
        second_phrase = 1
        minimum_length = 24
        minimum_spaces = 3
        if (len(line) < minimum_length) or (len(line.split()) < minimum_spaces):
            return False
        else:
            date = line.split()[first_phrase]
            time = line.split()[second_phrase]

            date_to_match = re.compile(r'\d\d\d\d/\d\d/\d\d')
            time_to_match = re.compile(r'\d\d:\d\d:\d\d.\d\d\d')

        return date_to_match.match(date) and time_to_match.match(time)


if __name__ == '__main__':
    Parser = FileParser('/Users/shrirangbagdi/Desktop/f.log', "/Users/shrirangbagdi/Desktop/")
    Parser.ParseFile()
