from datetime import datetime

from app.extensions import db
from app.models.camera import Camera
from app.utils.auth import get_current_user


class AddCameraUseCase:
    @staticmethod
    def execute(data):
        user = get_current_user()
        camera = Camera(
            name=data.name,
            preview_url=data.preview_url,
            client_id=user.client_id,
            status="active",
            created_at=datetime.utcnow()
        )
        db.session.add(camera)
        db.session.commit()
        return camera
