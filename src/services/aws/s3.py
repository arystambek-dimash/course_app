import boto3
from botocore.exceptions import ClientError

from src.core.config import settings

session = boto3.session.Session()


class S3Service:
    def __init__(self):
        self._s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION
        )
        self._bucket_name: str = settings.AWS_BUCKET_NAME

    async def upload_file(self, file_name: str, file_content: bytes, content_type: str):
        try:
            self._s3.put_object(
                Bucket=self._bucket_name,
                Key=file_name,
                Body=file_content,
                ContentType=content_type
            )
            return f"https://{self._bucket_name}.s3.amazonaws.com/{file_name}"
        except ClientError as e:
            print(f"An error occurred: {e}")
            return None

    async def delete_file(self, file_name: str):
        try:
            self._s3.delete_object(Bucket=self._bucket_name, Key=file_name)
            return True
        except ClientError as e:
            print(f"An error occurred: {e}")
            return False


s3_service = S3Service()
