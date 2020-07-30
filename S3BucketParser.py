import json
import os

import boto3

from BucketFolderParser import BucketFolderParser


class S3BucketParser:
    def __init__(self, bucketName):
        self.bucketName = bucketName

    def Parser(self):
        bucket = self.findBucket()
        if not bucket:
            print("Bucket not found!")

        else:
            self.bucketParser(bucket)

    def findBucket(self):
        s3_object = boto3.resource('s3', aws_access_key_id="AKIASCMI453UEAI6B3OS",
                                   aws_secret_access_key="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")

        for each_bucket in s3_object.buckets.all():
            if each_bucket.name == "unravellogdata":
                return each_bucket

    def bucketParser(self, bucket):
        for obj in bucket.objects.all():
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
