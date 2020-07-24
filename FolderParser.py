import os

from FileParser import FileParser


class FolderParser:
    def __init__(self, sourcePathway, destinationPathway, startDate=0, endDate=0, pattern=""):
        self.sourcePathway = sourcePathway
        self.destinationPathway = destinationPathway
        self.startDate = startDate
        self.endDate = endDate
        self.pattern = pattern

    def ParseFolder(self):
        total_list = []
        source = self.sourcePathway
        destination = self.destinationPathway
        for file in os.scandir(source):
            if file.path.endswith(".log") and (file.is_file()):
                total_list += FileParser(file, destination, self.startDate, self.endDate, self.pattern).ParseFile()
            elif file.is_dir():
                parser = FolderParser(file.path, self.destinationPathway, self.startDate, self.endDate, self.pattern)
                total_list += parser.ParseFolder()

        return total_list





if __name__ == '__main__':

    Parser = FolderParser('/Users/shrirangbagdi/Desktop/unravel_logs 2', '/Users/shrirangbagdi/Desktop/')
    Parser.ParseFolder()
