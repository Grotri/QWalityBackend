import os
import uuid
from io import BytesIO

from PIL import Image
from minio import Minio


class MinioClient:
    def __init__(self):
        self.endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        self.client = Minio(
            self.endpoint,
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
        return f"http://{self.endpoint}/{self.bucket}/{object_name}"

    def download_file(self, object_url: str) -> Image.Image:
        prefix = f"http://{self.endpoint}/{self.bucket}/"
        if not object_url.startswith(prefix):
            raise ValueError("Invalid object URL")

        object_name = object_url[len(prefix):]
        response = None
        try:
            response = self.client.get_object(self.bucket, object_name)
            data = BytesIO(response.read())
            image = Image.open(data)
            image.verify()
            data.seek(0)
            return Image.open(data)
        except Exception as e:
            raise ValueError(f"Failed to load image from MinIO: {e}")
        finally:
            if response:
                response.close()
                response.release_conn()

    def delete_file(self, object_url: str):
        prefix = f"http://{self.endpoint}/{self.bucket}/"
        if not object_url.startswith(prefix):
            raise ValueError("Invalid object URL")

        object_name = object_url[len(prefix):]
        self.client.remove_object(self.bucket, object_name)
