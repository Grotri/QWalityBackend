from main import create_app
from app.extensions import db
from app.models.tariff import Tariff

TARIFFS = [
    {
        "name": "demo",
        "price": 0,
        "user_limit": 1,
        "camera_limit": 1,
        "roles_allowed": ["owner"]
    },
    {
        "name": "standard",
        "price": 9900,  # 99.00 руб
        "user_limit": 4,
        "camera_limit": 3,
        "roles_allowed": ["owner", "user"]
    },
    {
        "name": "pro",
        "price": 19900,
        "user_limit": 8,
        "camera_limit": 10,
        "roles_allowed": ["owner", "admin", "moderator", "user"]
    },
    {
        "name": "ultima",
        "price": 39900,
        "user_limit": 1000,
        "camera_limit": None,
        "roles_allowed": ["owner", "admin", "moderator", "user"]
    }
]

app = create_app()

with app.app_context():
    for data in TARIFFS:
        existing = Tariff.query.filter_by(name=data["name"]).first()
        if not existing:
            db.session.add(Tariff(**data))
    db.session.commit()
    print("✔️ Tariffs seeded.")
