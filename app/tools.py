import boto3
from app import app

s3 = boto3.client(
    "s3",
    aws_access_key_id = app.config['S3_KEY'],
    aws_secret_access_key = app.config['S3_SECRET']
)

def upload_to_s3(file, filename, bucket_name, acl='public-read'):

    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                'ACL': acl,
                'ContentType': file.content_type
            }
        )
    except Exception as e:
        print('Upload error: ', e)
        return e
    
    return "{}{}".format(app.config['S3_LOCATION'], filename)