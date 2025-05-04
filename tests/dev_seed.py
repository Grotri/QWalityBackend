from datetime import datetime, timedelta

from app.extensions import db
from app.models import Tariff, License


def seed_test_tariff_and_license(client_id: int):
    tariff = Tariff.query.filter_by(name="dev-fixture").first()
    if not tariff:
        tariff = Tariff(
            name="dev-fixture",
            max_users=99,
            max_cameras=99,
            roles=["owner", "admin", "moderator", "user"]
        )
        db.session.add(tariff)
        db.session.flush()

    license = License(
        client_id=client_id,
        tariff_id=tariff.id,
        active=True,
        expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db.session.add(license)
    db.session.commit()

    return tariff, license
