import boto3
import json
import os

from LambdaAWSFunction.log_parser import Log_Parser


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = 'ouput-bucket'

    log = Log_Parser()
    messages = log.parse_file(event)

    if messages:
        file_name = str(event["Records"][0]['s3']['object']['key'])
        (file, ext) = os.path.splitext(file_name)
        changed_file_name = file + ".json"

        uploadByteStream = bytes(('\n'.join(json.dumps(i) for i in messages) + '\n').encode('UTF-8'))

        s3.put_object(Bucket=bucket, Key=changed_file_name, Body=uploadByteStream)

