import boto3


def upload_file(bucket, bucket_path, file_path):
    s3 = boto3.client('s3')
    s3.upload_file(Bucket=bucket,
                   Filename=file_path,
                   Key=bucket_path)


def mkdir(bucket, dir_name):
    response = boto3.client('s3')
    response.put_object(
        Bucket=bucket,
        Key=dir_name + '/'
    )
