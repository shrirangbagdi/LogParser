import json
import os

import boto3

from S3BucketParser.BucketFolderParser import BucketFolderParser

s3_object = boto3.resource('s3', aws_access_key_id="****",
                             aws_secret_access_key="****")


class S3BucketParser:
    def __init__(self, bucketName):
        self.bucketName = bucketName

    def Parser(self):
        self.bucketParser("unravellogdata")


    def bucketParser(self, bucketName):
        s3AllObj=s3_object.Bucket(bucketName).objects.all()
        for obj in s3AllObj:
            bucket_parser = BucketFolderParser(obj)
            messages = bucket_parser.parseBucketFolder()
            file_name = self.getFileName(obj.key)
            self.createJson(messages, file_name)
            self.uploadToS3(messages, obj.key)

    def getFileName(self, objectKey):
        (file, ext) = os.path.splitext(objectKey)

        return file.split('/')[-1]

    def uploadToS3(self, messages, objectKey):
        fileName = self.getFileName(objectKey)

        if messages:
            s3 = boto3.client('s3')
            s3.upload_file('/Users/shrirangbagdi/Desktop/' + fileName + '.json', 'unravellogdata', self.getBucketPathway(objectKey) + ".json")

    def createJson(self, messages, fileName):
        if messages:
            with open("/Users/shrirangbagdi/Desktop/" + fileName + '.json', 'w') as log_file:
                log_file.write('\n'.join(json.dumps(i) for i in messages) +
                               '\n')

    def getBucketPathway(self, objectKey):
        (file, ext) = os.path.splitext(objectKey)

        return file


if __name__ == '__main__':
    parser = S3BucketParser("unravellogdata")
    parser.Parser()
