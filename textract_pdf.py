import simplejson
import logging
import os
import time
import boto3
import json
from botocore.exceptions import ClientError

from env import aws_access_key_id, aws_secret_access_key
from store import filter

pdf_file = "docs/Energielabel_7316JV_39.pdf"

BUCKET_NAME = "pdf-textract-bucket"
REGION_NAME = "us-west-1"
textract_client = boto3.client('textract', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=REGION_NAME)
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=REGION_NAME)

# Step 1
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# step 2
def startJob(s3BucketName, objectName):
    response = None
    response = textract_client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': objectName
            },
        }
    )

    return response["JobId"]

# step 3
def isJobComplete(jobId):
    time.sleep(5)
    response = textract_client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = textract_client.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status

# step 4
def getJobResults(jobId):
    pages = []

    time.sleep(5)

    response = textract_client.get_document_text_detection(JobId=jobId)
    
    pages.append(response)
    print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None
    if('NextToken' in response):
        nextToken = response['NextToken']

    while(nextToken):
        time.sleep(5)

        response = textract_client.get_document_text_detection(JobId=jobId, NextToken=nextToken)

        pages.append(response)
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']

    return pages


# Document
# upload_file(pdf_file, bucket=BUCKET_NAME)
# jobId = startJob(BUCKET_NAME, "Energielabel_7316JV_39.pdf")
# print("Started job with id: {}".format(jobId))

# if(isJobComplete(jobId)):  # online if case
if(True):
    file = open("response.json", "r") #local response 
    response = json.load(file) #local response 
    
    # response = getJobResults(jobId) # online response

    result = filter(response)
    response_file = open("result.json", "w")
    # magic happens here to make it pretty-printed
    response_file.write(simplejson.dumps(result, indent=4, sort_keys=True))
    response_file.close()
    