from app.models import Product
from app.extensions import db


class ProductRepository:
    @staticmethod
    def get_by_id(product_id: int) -> Product | None:
        return Product.query.get(product_id)

    @staticmethod
    def get_all_by_camera(camera_id: int) -> list[Product]:
        return Product.query.filter_by(camera_id=camera_id).all()

    @staticmethod
    def create(batch_number: str, camera_id: int) -> Product:
        product = Product(batch_number=batch_number, camera_id=camera_id)
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def update(product_id: int, **kwargs) -> Product:
        product = ProductRepository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        allowed_fields = {"batch_number", "camera_id"}
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(product, key, value)

        db.session.commit()
        return product

    @staticmethod
    def delete(product_id: int):
        product = ProductRepository.get_by_id(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
