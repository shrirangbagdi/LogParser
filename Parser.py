import json
import re


class Parser:
    def __init__(self, logfile):
        self.logfile = logfile

    def ParseFile(self):
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

                    warning = {'Date': date, 'Time': time, 'Type': current_type, 'Message': message}
                    first_iteration = False

                if current_type == "ERROR":
                    line_list = line.split()
                    warning = {'Date': line_list[first_phrase], 'Time': line_list[second_phrase], 'Type': current_type,
                               'Message': line.split("ERROR")[second_phrase]}
                    first_iteration = False

                previous_type = current_type

            elif previous_type == "WARN" or previous_type == "ERROR":
                warning["Message"] += line

        if previous_type == "ERROR" or previous_type == "WARN":
            list_of_warnings.append(warning)

        with open('/Users/shrirangbagdi/Desktop/Contents.json', 'w') as log_file:
            json.dump(list_of_warnings, log_file, indent=4)

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
    Parser = Parser('/Users/shrirangbagdi/Desktop/l.log')
    Parser.ParseFile()

# make code cleaner
# add more methods
# add errors exceptions
# take in a folder, multiple log files, a log file and be able to convert into json object..

