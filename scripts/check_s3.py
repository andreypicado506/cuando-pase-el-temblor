#!/usr/bin/env python3

import argparse
import boto3
from typing import NoReturn, Union

def s3_file_exist(bucket_name, file_key) -> bool:
    """
    Check if a file exists in an S3 bucket.

    :param bucket_name: The name of the S3 bucket.
    :param file_key: The key (path) of the file within the bucket.
    """
    s3 = boto3.client('s3')
    try:
        s3.head_object(Bucket=bucket_name, Key=file_key)
        return True
    except Exception as e:
        return False

def create_s3_file(bucket_name, file_key, content) -> NoReturn:
    """
    Create a new file in an S3 bucket with the provided content.

    :param bucket_name: The name of the S3 bucket.
    :param file_key: The key (path) of the new file within the bucket.
    :param content: The content to be written to the file.
    """
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=content.encode('utf-8'))
    except Exception as e:
        print(f"Error creating S3 file: {e}")

def read_s3_file(bucket_name, file_key) -> Union[str, None]:
    """
    Read the content of a file from an S3 bucket.

    :param bucket_name: The name of the S3 bucket.
    :param file_key: The key (path) of the file within the bucket.
    :return: The content of the file as a UTF-8 encoded string, or None if there was an error.
    """
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        content = response['Body'].read().decode('utf-8')
        return content
    except Exception as e:
        return None

def update_s3_file(bucket_name, file_key, new_content) -> NoReturn:
    """
    Update the content of an existing file in an S3 bucket with new content.

    :param bucket_name: The name of the S3 bucket.
    :param file_key: The key (path) of the file to be updated within the bucket.
    :param new_content: The new content to replace the existing content of the file.
    """
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=new_content.encode('utf-8'))
    except Exception as e:
        print(f"Error updating S3 file: {e}")

def main() -> bool:
    # Parser for args
    parser = argparse.ArgumentParser(description="Script to check, read and write a file in AWS S3.")
    parser.add_argument("-b", "--bucket-name", type=str, required=True)
    parser.add_argument("-f", "--file-key", type=str, required=True)
    parser.add_argument("-l", "--local-file", required=True)

    # Main vars
    bucket_name          = parser.parse_args().bucket_name
    file_key             = parser.parse_args().file_key
    local_file_path      = parser.parse_args().local_file

    # Read the file that was previously created in the pipeline
    # it will have the latest data from OVSICORI
    with open(local_file_path, 'r') as file:
        last_earthquake_data = file.read()

    # Check if the file exists in the s3 bucket, if not, create it
    s3_file_created = s3_file_exist(bucket_name, file_key)
    if not s3_file_created:
        create_s3_file(bucket_name, file_key, last_earthquake_data)
        return False
    
    # Compare current data from OVSICORI 
    # with the info stored in the s3 file
    current_content = read_s3_file(bucket_name, file_key)
    if current_content != last_earthquake_data:
        update_s3_file(bucket_name, file_key, last_earthquake_data)
        return True
    else:
        return False

if __name__ == "__main__":
    print(main())
