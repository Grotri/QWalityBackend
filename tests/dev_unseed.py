from app.extensions import db
from app.models import License, Tariff


def unseed_test_license_and_tariff(client_id: int):
    License.query.filter_by(client_id=client_id).delete()

    Tariff.query.filter_by(name="dev-fixture").delete()

    db.session.commit()
