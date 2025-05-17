from app.repositories.camera_repository import CameraRepository
from app.utils.auth import get_current_client


class GetCamerasUseCase:
    @staticmethod
    def execute():
        return CameraRepository.get_all_by_client_id_and_status(
            client_id=get_current_client().id
        )
