import os

from S3BucketParser.BucketFileParser import BucketFileParser


class BucketFolderParser:
    def __init__(self, obj):
        self.obj = obj

    def parseBucketFolder(self):
        directory = self.obj.key
        print(directory)
        if directory[-1] != "/" and self.isLog(directory) and (not self.isEmpty(self.obj)):
            case_id = self.getID(directory)
            bucket_parser = BucketFileParser(case_id, self.obj)
            message_list = bucket_parser.generateMessages()
            return message_list
        elif directory[-1] != "/" and self.isCompressed(directory):
            pass


    def getID(self, directory):
        if "/" in directory:
            return directory.split("/")[0]
        else:
            return "No ID"

    def isLog(self, directory):
        (file, ext) = os.path.splitext(directory)
        return ext == ".log"

    def isEmpty(self, directory):
        if directory.get()['Body'].read().decode('utf-8') == "":
            return True
        return False

    def isCompressed(self, directory):

        (file, ext) = os.path.splitext(directory)
        return ext == ".tar.gz" or ext == ".log.gz" or ext == ".zip" or ext == ".gz" or ext == ".tar"


if __name__ == '__main__':
    parser = BucketFolderParser("f")
    parser.isLog("unravel.log")
