from app.models.license import License
from app.utils.auth import get_current_user


def get_active_license():
    user = get_current_user()
    return License.query.filter_by(client_id=user.client_id, status="active").order_by(
        License.activated_at.desc()).first()
