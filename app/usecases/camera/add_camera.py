from app.repositories.camera_repository import CameraRepository
from app.schemas.camera.camera_create_dto import CameraCreateDTO


class AddCameraUseCase:
    @staticmethod
    def execute(dto: CameraCreateDTO):
        return CameraRepository.create(
            dto.name,
            dto.camera_url
        )