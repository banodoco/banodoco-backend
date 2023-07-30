import mimetypes
from urllib.parse import urlparse
import boto3
import uuid
import os
import shutil

import requests
from banodoco.settings import AWS_ACCESS_KEY_ID, AWS_S3_BUCKET, AWS_S3_REGION, AWS_SECRET_ACCESS_KEY, SERVER, SERVER_ENV

s3_client = boto3.client(
    service_name='s3',
    region_name=AWS_S3_REGION
) if SERVER != SERVER_ENV.DEV.value else \
    boto3.client(
    service_name='s3',
    region_name=AWS_S3_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def upload_file(file, file_name='default', bucket=AWS_S3_BUCKET, object_name=None, folder='posts/'):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)
    
    unique_tag = str(uuid.uuid4())
    file_extension = os.path.splitext(object_name)[1]
    filename = unique_tag + file_extension

    # Upload the file
    content_type = mimetypes.guess_type(object_name)[0]
    data = {
        "Body": file,
        "Bucket": bucket,
        "Key": folder + filename,
        "ACL": "public-read"
    }
    if content_type:
        data['ContentType'] = content_type
    
    resp = s3_client.put_object(**data)
    object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
        AWS_S3_REGION,
        AWS_S3_BUCKET,
        folder + filename)
    return object_url

def is_s3_image_url(url):
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc.lower()

    if netloc.endswith('.amazonaws.com'):
        subdomain = netloc[:-len('.amazonaws.com')].split('-')
        if len(subdomain) > 1 and subdomain[0] == 's3':
            return True

    return False

def generate_s3_url(image_url, bucket=AWS_S3_BUCKET, file_ext='png', folder='posts/'):
    object_name = str(uuid.uuid4()) + '.' + file_ext

    response = requests.get(image_url)
    if response.status_code != 200:
        raise Exception("Failed to download the image from the given URL")

    file = response.content

    content_type = mimetypes.guess_type(object_name)[0]
    data = {
        "Body": file,
        "Bucket": bucket,
        "Key": folder + object_name,
        "ACL": "public-read"
    }
    if content_type:
        data['ContentType'] = content_type
    else:
        data['ContentType'] = 'image/png'

    resp = s3_client.put_object(**data)

    extension = os.path.splitext(object_name)[1]
    disposition = f'inline; filename="{object_name}"'
    if extension:
        disposition += f'; filename="{object_name}"'
    resp['ResponseMetadata']['HTTPHeaders']['Content-Disposition'] = disposition

    object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
        AWS_S3_REGION,
        AWS_S3_BUCKET,
        folder + object_name)
    return object_url