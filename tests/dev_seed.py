from datetime import datetime, timedelta

from app.extensions import db
from app.models import Tariff, License


def seed_test_tariff_and_license(client_id: int):
    tariff = Tariff.query.filter_by(name="dev-fixture").first()
    if not tariff:
        tariff = Tariff(
            name="dev-fixture",
            user_limit=99,
            price=0,
            camera_limit=99,
            roles_allowed=["owner", "admin", "moderator", "user"]
        )
        db.session.add(tariff)
        db.session.flush()

    license = License(
        client_id=client_id,
        tariff_id=tariff.id,
        activated_at=datetime.utcnow(),
        expired_at=datetime.utcnow() + timedelta(days=30),
        status="active"
    )
    db.session.add(license)
    db.session.commit()

    return tariff, license
