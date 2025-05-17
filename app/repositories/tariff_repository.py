from app.models import Tariff
from app.extensions import db


class TariffRepository:
    @staticmethod
    def get_by_id(tariff_id: int) -> Tariff | None:
        return Tariff.query.get(tariff_id)

    @staticmethod
    def get_by_name(name: str) -> Tariff | None:
        return Tariff.query.filter_by(name=name).first()

    @staticmethod
    def get_all() -> list[Tariff]:
        return Tariff.query.order_by(Tariff.price.asc()).all()

    @staticmethod
    def create(name: str, price: int, user_limit: int, camera_limit: int | None, roles_allowed: list[str]) -> Tariff:
        tariff = Tariff(
            name=name,
            price=price,
            user_limit=user_limit,
            camera_limit=camera_limit,
            roles_allowed=roles_allowed
        )
        db.session.add(tariff)
        db.session.commit()
        return tariff

    @staticmethod
    def update(tariff_id: int, **kwargs) -> Tariff:
        tariff = TariffRepository.get_by_id(tariff_id)
        if not tariff:
            raise ValueError("Tariff not found")

        allowed_fields = {"name", "price", "user_limit", "camera_limit", "roles_allowed"}
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(tariff, key, value)

        db.session.commit()
        return tariff

    @staticmethod
    def delete(tariff_id: int):
        tariff = TariffRepository.get_by_id(tariff_id)
        if tariff:
            db.session.delete(tariff)
            db.session.commit()
