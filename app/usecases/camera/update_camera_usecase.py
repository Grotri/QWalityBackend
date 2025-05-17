from app.repositories.camera_repository import CameraRepository
from app.schemas.camera.camera_update_dto import CameraUpdateDTO


class UpdateCameraUseCase:
    @staticmethod
    def execute(camera_id: int, dto: CameraUpdateDTO):
        data = dto.model_dump(exclude_unset=True)
        return CameraRepository.update(
            camera_id=camera_id,
            **data
        )
