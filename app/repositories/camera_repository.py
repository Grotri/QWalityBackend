from app.extensions import db
from app.models import Camera
from app.utils.auth import get_current_client


class CameraRepository:
    @staticmethod
    def get_by_id(camera_id: int) -> Camera | None:
        return Camera.query.get(camera_id)

    @staticmethod
    def get_all_by_client_id(client_id: int) -> list[Camera]:
        return Camera.query.filter_by(client_id=client_id).all()

    @staticmethod
    def get_all_by_client_id_and_status(client_id: int) -> list[Camera]:
        return Camera.query.filter_by(client_id=client_id).all()

    @staticmethod
    def create(name: str, camera_url: str, client_id: int, status: str = "active") -> Camera:
        camera = Camera(
            name=name,
            camera_url=camera_url,
            client_id=client_id,
            status=status
        )
        db.session.add(camera)
        db.session.commit()
        return camera

    @staticmethod
    def update(camera_id: int, **kwargs) -> Camera:
        camera = CameraRepository.get_by_id(camera_id)
        if not camera:
            raise ValueError("Camera not found")

        allowed_fields = {"name", "camera_url", "status", "client_id", "deleted_at"}
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(camera, key, value)

        db.session.commit()
        return camera

    @staticmethod
    def delete(camera_id: int):
        camera = CameraRepository.get_by_id(camera_id)
        if camera:
            db.session.delete(camera)
            db.session.commit()
