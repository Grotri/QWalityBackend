import click
from dotenv import load_dotenv
from flask import Flask
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

    app.url_map.strict_slashes = False

    @app.after_request
    def disable_cors(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

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
