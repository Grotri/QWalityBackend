import os
import uuid
from io import BytesIO

from minio import Minio


class MinioClient:
    def __init__(self):
        self.client = Minio(
            os.getenv("MINIO_ENDPOINT", "localhost:9000"),
            access_key=os.getenv("MINIO_ACCESS_KEY"),
            secret_key=os.getenv("MINIO_SECRET_KEY"),
            secure=False
        )
        self.bucket = os.getenv("MINIO_BUCKET", "product-images")
        self._ensure_bucket()

    def _ensure_bucket(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def upload_file(self, file_stream, file_name: str, content_type: str = "image/jpeg") -> str:
        object_name = f"{uuid.uuid4()}_{file_name}"
        self.client.put_object(
            self.bucket,
            object_name,
            file_stream,
            length=-1,
            part_size=10 * 1024 * 1024,
            content_type=content_type
        )
        return f"http://{self.client._endpoint}/{self.bucket}/{object_name}"

    from io import BytesIO

    def download_file(self, object_url: str) -> BytesIO:
        # Извлекаем object_name из URL
        prefix = f"http://{self.client._endpoint}/{self.bucket}/"
        if not object_url.startswith(prefix):
            raise ValueError("Invalid object URL")

        object_name = object_url[len(prefix):]

        response = self.client.get_object(self.bucket, object_name)
        return BytesIO(response.read())

    def delete_file(self, object_url: str):
        prefix = f"http://{self.client._endpoint}/{self.bucket}/"
        if not object_url.startswith(prefix):
            raise ValueError("Invalid object URL")

        object_name = object_url[len(prefix):]
        self.client.remove_object(self.bucket, object_name)
