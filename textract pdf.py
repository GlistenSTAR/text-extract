import simplejson
import logging
import os
import time
import boto3
from botocore.exceptions import ClientError

aws_access_key_id="AKIASB66JFBS2OSVJAQD" 
aws_secret_access_key= "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"

pdf_file = "docs/doc05857020210910103344.pdf"

BUCKET_NAME = "pdf-textract-bucket"
REGION_NAME = "us-west-1"
textract_client = boto3.client('textract', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=REGION_NAME)
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=REGION_NAME)

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

# upload_file(pdf_file, bucket=bucket)

def startJob(s3BucketName, objectName):
    response = None
    response = textract_client.start_document_text_detection(
    DocumentLocation={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': objectName
        },
    },
    OutputConfig={
        'S3Bucket': s3BucketName,
        'S3Prefix': 'response'
    }
    )

    return response["JobId"]

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
jobId = startJob(BUCKET_NAME, "doc05857020210910103344.pdf")
print("Started job with id: {}".format(jobId))
if(isJobComplete(jobId)):
    response = getJobResults(jobId)
    response_file = open("response.json", "w")
    # magic happens here to make it pretty-printed
    response_file.write(simplejson.dumps(response, indent=4, sort_keys=True))
    response_file.close()
    