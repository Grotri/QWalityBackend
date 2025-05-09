import click
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.controllers import _build_cors_preflight_response, _corsify_actual_response
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

    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Methods']='*'
        response.headers['Access-Control-Allow-Origin']='*'
        response.headers['Vary']='Origin'
        return response

    # @app.after_request
    # def disable_cors(response):
    #     response.headers["Access-Control-Allow-Origin"] = "*"
    #     response.headers["Access-Control-Allow-Methods"] = "*"
    #     response.headers["Access-Control-Allow-Headers"] = "*"
    #     return response

    cache.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # CORS(app,
    #      resources={r"/*": {  # Применяем ко всем маршрутам
    #          "origins": "*",  # Разрешаем запросы с любых доменов
    #          "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],  # Все HTTP методы
    #          "allow_headers": "*",  # Все заголовки
    #          "expose_headers": "*",  # Все заголовки ответа доступны клиенту
    #          "supports_credentials": True,  # Поддержка cookies и авторизации
    #          "max_age": 86400  # Кеширование preflight-запросов на 24 часа
    #      }})

    # CORS(app, support_credentials=True)

    register_routes(app)

    # @app.after_request
    # def wrap_response(response):
    #     return _corsify_actual_response(response)

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
