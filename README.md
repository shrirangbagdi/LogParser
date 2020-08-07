# LogParser

Author: Shrirang Bagdi - shrirangbagdi@gmail.com


Table of Contents
1. Description of Parser
2. Possible Commands
3. Necessary Libraries
4. Setup

## 1. Description of Parser

It is difficult to read through hundreds of lines of errors, warnings, information, etc. in order to understand what may be going wrong with an application. This open source log parsing project was created in order to aid in parsing such logs in order to find error and warning messages and to generate a detailed output file.

### Different Implementations:

#### Log Parser using AWS Lambda Function
When a user uploads log files into an S3 Bucket, an AWS lambda function is triggered. The AWS Lambda function parses through all the input files and generates a JSON file of messages. The generated output is uploaded into another S3 bucket.

#### Log Parser for an S3 Bucket without AWS Lambda
If one wants to just generate a JSON file without using the AWS lambda trigger, there is also an implementation that allows the user to generate JSON files through the parsing of the S3 Bucket. 

#### Log Parser for a file through the command line 
If one wants to just generate a JSON file by specificing the pathway of the log file there is also an implementation for that to aid the user in generating JSON files. 

## 2. Possible Commands

In order to run this parser properly, you will have to make sure that you run the commands properly. For now there are six possible commands. In order to run these commands properly, you must update the 
source pathway to include a folder as well as a destination pathway inside the property file. You must additionally read the [LogParser.properties](https://github.com/shrirangbagdi/LogParser/blob/master/LogParser.properties) file descriptions. It contains a list of possible commands that this parser can complete. For example, 
in order to run a file parser the user must include the command number as well as the file in the folder that they want to parse through.


## 3. Necessary Libraries
The user must make sure to have the latest version of python installed as well as boto3. 

## Setup

