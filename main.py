import click
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.extensions import db, mail
from app.routes import register_routes
from tests.dev_seed import seed_test_tariff_and_license
from tests.dev_unseed import unseed_test_license_and_tariff

jwt = JWTManager()
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    CORS(app,
         resources={r"/*": {  # Применяем ко всем маршрутам
             "origins": "*",  # Разрешаем запросы с любых доменов
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],  # Все HTTP методы
             "allow_headers": "*",  # Все заголовки
             "expose_headers": "*",  # Все заголовки ответа доступны клиенту
             "supports_credentials": True,  # Поддержка cookies и авторизации
             "max_age": 86400  # Кеширование preflight-запросов на 24 часа
         }})

    register_routes(app)

    @app.cli.command("seed-dev")
    @click.option("--client-id", required=True, type=int, help="Client ID for seeding")
    def seed_dev(client_id):
        """Seed dev tariff and license data"""
        with app.app_context():
            seed_test_tariff_and_license(client_id)
            click.echo(f"Seeded data for client_id={client_id}")

    @app.cli.command("unseed-dev")
    @click.option("--client-id", required=True, type=int, help="Client ID for unseeding")
    def unseed_dev(client_id):
        """Unseed dev tariff and license data"""
        with app.app_context():
            unseed_test_license_and_tariff(client_id)
            click.echo(f"Unseeded data for client_id={client_id}")

    return app
