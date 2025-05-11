from flask import Blueprint, jsonify
from minio import Minio
from minio.error import S3Error
import io
import os

utils_bp = Blueprint("utils", __name__)


@utils_bp.route("/utils/test-minio", methods=["GET"])
def test_minio():
    try:
        client = Minio(
            os.getenv("MINIO_ENDPOINT", "minio:9000"),
            access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
            secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
            secure=False
        )

        bucket_name = os.getenv("MINIO_BUCKET", "inspections")
        test_filename = "flask_test_file.txt"

        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)

        content = io.BytesIO(b"Test from Flask endpoint")
        client.put_object(
            bucket_name=bucket_name,
            object_name=test_filename,
            data=content,
            length=content.getbuffer().nbytes,
            content_type="text/plain"
        )

        return jsonify({"message": "✅ Файл успешно загружен в MinIO"}), 200

    except S3Error as e:
        return jsonify({"error": str(e)}), 500
