from app.repositories.camera_repository import CameraRepository
from app.schemas.camera.camera_create_dto import CameraCreateDTO
from app.utils.auth import get_current_client


class AddCameraUseCase:
    @staticmethod
    def execute(dto: CameraCreateDTO):
        client = get_current_client()
        return CameraRepository.create(
            name=dto.name,
            camera_url=dto.camera_url,
            client_id=client.id
        )
