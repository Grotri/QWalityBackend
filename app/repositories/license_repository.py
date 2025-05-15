from app.models import License
from app.extensions import db
from datetime import datetime


class LicenseRepository:
    @staticmethod
    def get_by_id(license_id: int) -> License | None:
        return License.query.get(license_id)

    @staticmethod
    def get_latest_by_client(client_id: int) -> License | None:
        return (
            License.query.filter_by(client_id=client_id)
            .order_by(License.activated_at.desc())
            .first()
        )

    @staticmethod
    def get_all_by_client(client_id: int) -> list[License]:
        return License.query.filter_by(client_id=client_id).all()

    @staticmethod
    def create(
            client_id: int,
            tariff_id: int,
            status: str,
            payment_id: int | None = None,
            expired_at: datetime | None = None,
    ) -> License:
        license = License(
            client_id=client_id,
            tariff_id=tariff_id,
            payment_id=payment_id,
            status=status,
            expired_at=expired_at,
        )
        db.session.add(license)
        db.session.commit()
        return license

    @staticmethod
    def update(license_id: int, **kwargs) -> License:
        license = LicenseRepository.get_by_id(license_id)
        if not license:
            raise ValueError("License not found")

        allowed_fields = {"tariff_id", "payment_id", "status", "expired_at"}
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(license, key, value)

        db.session.commit()
        return license

    @staticmethod
    def delete(license_id: int):
        license = LicenseRepository.get_by_id(license_id)
        if license:
            db.session.delete(license)
            db.session.commit()
