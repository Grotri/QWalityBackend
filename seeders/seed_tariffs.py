from app.extensions import db
from app.models.tariff import Tariff
from main import create_app

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
        "price": 299900,  # 2999.00 руб = 299900
        "user_limit": 4,
        "camera_limit": 3,
        "roles_allowed": ["owner", "user"]
    },
    {
        "name": "pro",
        "price": 899900,  # 8999.00 руб = 899900
        "user_limit": 8,
        "camera_limit": 8,
        "roles_allowed": ["owner", "admin", "moderator", "user"]
    },
    {
        "name": "ultima",
        "price": 1799900,  # 17999.00 руб = 1799900
        "user_limit": 20,
        "camera_limit": 15,
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
