import click
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager

from app.extensions import db, mail, cache
from app.routes import register_routes
from tests.dev_seed import seed_test_tariff_and_license
from tests.dev_unseed import unseed_test_license_and_tariff

jwt = JWTManager()
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    app.url_map.strict_slashes = False

    def option_todo(id):
        return '', 204

    app.add_url_rule('/', view_func=option_todo, provide_automatic_options=False, methods=['OPTIONS'])
    app.add_url_rule(r'/<path:path>', view_func=option_todo, provide_automatic_options=False, methods=['OPTIONS'])

    cache.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    register_routes(app)

    @app.cli.command("seed-dev")
    @click.option("--client-id", required=True, type=int, help="Client ID for seeding")
    def seed_dev(client_id):
        with app.app_context():
            seed_test_tariff_and_license(client_id)
            click.echo(f"Seeded data for client_id={client_id}")

    @app.cli.command("unseed-dev")
    @click.option("--client-id", required=True, type=int, help="Client ID for unseeding")
    def unseed_dev(client_id):
        with app.app_context():
            unseed_test_license_and_tariff(client_id)
            click.echo(f"Unseeded data for client_id={client_id}")

    return app
