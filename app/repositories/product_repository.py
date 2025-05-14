from app.extensions import db
from app.models import Product


class ProductRepository:
    @staticmethod
    def create(batch_number: str, camera_id: int) -> Product:
        product = Product(batch_number=batch_number, camera_id=camera_id)
        db.session.add(product)
        db.session.flush()  # чтобы получить product.id
        return product

    @staticmethod
    def get_by_id(product_id: int):
        return Product.query.get(product_id)
