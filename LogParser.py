import json
import sys
import os

from FileParser import FileParser
from FolderParser import FolderParser


class LogParser:
    def __init__(self, propertyFile):
        self.propertyFile = propertyFile
        self.parseSpecificDate = False

    def GetSource(self):
        try:
            property_file = open(self.propertyFile, 'r')
            for line in property_file:
                if "SourcePath" in line:
                    source_pathway = line.split("=")[-1].strip()
                    if not os.path.exists(source_pathway):
                        raise Exception("File does not exist")
                    else:
                        return source_pathway
                else:
                    break
        except:
            raise Exception("Something went wrong with your file, or destination path")

    def GetDestination(self):
        try:
            property_file = open(self.propertyFile, 'r')
            for line in property_file:
                if "DestinationPath" in line:
                    return line.split("=")[-1].strip()
        except:
            raise Exception("Something went wrong with your file, or destination path")

    def CreateJsonFile(self, listOfWarnings):
        destination = self.GetDestination()

        if listOfWarnings:
            with open(destination + "AllResults" + '.json', 'w') as log_file:
                log_file.write('[' + ',\n'.join(json.dumps(i) for i in listOfWarnings) +
                    ']\n')
                #json.dump(listOfWarnings, log_file, indent=4)

    def RunParser(self):
        command_line_arguments = sys.argv[1:]
        source_path = self.GetSource()
        destination_path = self.GetDestination()

        if (source_path or destination_path) is None:
            raise Exception("Something went wrong with your file, source path, or destination path")

        elif not command_line_arguments:
            parser = FolderParser(source_path, destination_path, 0, 0, "")
            list_of_warnings = parser.ParseFolder()
            self.CreateJsonFile(list_of_warnings)

        elif command_line_arguments[0] == "help":
            print("You must put an input parameter along with the necessary arguments. For example: LogParser.py 5 sql")
            print("InputParam=0, Input is given by user in terminal to indicate that a folder needs to be parsed")
            print("InputParam=1, Input is given by user in terminal to indicate that a specific log file in the "
                  "folder needs to be parsed")
            print("InputParam=2, Input is given by user in terminal to indicate that two specific log files in the "
                  "folder needs to be parsed")
            print("InputParam=3, Input is given by user in terminal to indicate that three specific log files in the "
                  "folder needs to be parsed")
            print("InputParam=4, Input is given by user in terminal to indicate a specific start date & end date")
            print("InputParam=5, Input is given by user in terminal to indicate a specific pattern")

        else:
            command_input = int(command_line_arguments[0])

            if len(command_line_arguments) < 1:
                raise Exception("Please enter an argument")

            elif command_input < 0 or command_input > 5:
                raise Exception("Please enter a valid input paramater")

            elif command_input == 0:
                parser = FolderParser(source_path, destination_path, 0, 0, "")
                list_of_warnings = parser.ParseFolder()
                self.CreateJsonFile(list_of_warnings)

            elif command_input == 1:
                # create command for multiple files....
                file_name = source_path + "/" + command_line_arguments[1].strip()
                parser = FileParser(file_name, destination_path, 0, 0, "")
                list_of_all_warnings = parser.ParseFile()
                self.CreateJsonFile(list_of_all_warnings)

            elif command_input == 2:
                first_file_name = source_path + "/" + command_line_arguments[1].strip()
                parser_one = FileParser(first_file_name, destination_path, 0, 0, "")
                list_one = parser_one.ParseFile()

                second_file_name = source_path + "/" + command_line_arguments[2].strip()
                parser_two = FileParser(second_file_name, destination_path, 0, 0, "")
                list_two = parser_two.ParseFile()

                self.CreateJsonFile(list_one + list_two)

            elif command_input == 3:
                first_file_name = source_path + "/" + command_line_arguments[1].strip()
                parser_one = FileParser(first_file_name, destination_path, 0, 0, "")
                list_one = parser_one.ParseFile()

                second_file_name = source_path + "/" + command_line_arguments[2].strip()
                parser_two = FileParser(second_file_name, destination_path, 0, 0, "")
                list_two = parser_two.ParseFile()

                third_file_name = source_path + "/" + command_line_arguments[3].strip()
                parser_three = FileParser(third_file_name, destination_path, 0, 0, "")
                list_three = parser_three.ParseFile()

                self.CreateJsonFile(list_one + list_two + list_three)

            elif command_input == 4:
                start_date = command_line_arguments[1]
                end_date = command_line_arguments[2]
                parser = FolderParser(source_path, destination_path, start_date, end_date, "")
                list_one = parser.ParseFolder()
                self.CreateJsonFile(list_one)

            elif command_input == 5:
                pattern = command_line_arguments[1]
                parser = FolderParser(source_path, destination_path, 0, 0, pattern)
                list_one = parser.ParseFolder()
                self.CreateJsonFile(list_one)


if __name__ == '__main__':
    LogParser = LogParser("/Users/shrirangbagdi/PycharmProjects/LogParser/LogParser.properties")
    LogParser.RunParser()
