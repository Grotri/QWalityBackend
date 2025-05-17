from typing_extensions import deprecated

from app.repositories.camera_repository import CameraRepository


class DeleteCameraUseCase:
    @staticmethod
    @deprecated("Shouldn't use it")
    def execute(camera_id: int):
        CameraRepository.update(
            camera_id,
            **{"status": "deleted"}
        )
