from app.models import Client
from app.extensions import db


class ClientRepository:
    @staticmethod
    def get_by_id(client_id: int) -> Client | None:
        return Client.query.get(client_id)

    @staticmethod
    def get_by_email(email: str) -> Client | None:
        return Client.query.filter_by(email=email).first()

    @staticmethod
    def get_by_tin(tin: str) -> Client | None:
        return Client.query.filter_by(tin=tin).first()

    @staticmethod
    def create(email: str, tin: str, type_: str, conf_threshold: float = 0.25) -> Client:
        client = Client(email=email, tin=tin, type=type_, conf_threshold=conf_threshold)
        db.session.add(client)
        db.session.commit()
        return client

    @staticmethod
    def update_conf_threshold(client_id: int, new_threshold: float) -> Client:
        client = ClientRepository.get_by_id(client_id)
        if not client:
            raise ValueError("Client not found")
        client.conf_threshold = new_threshold
        db.session.commit()
        return client

    @staticmethod
    def delete(client_id: int):
        client = ClientRepository.get_by_id(client_id)
        if client:
            db.session.delete(client)
            db.session.commit()
