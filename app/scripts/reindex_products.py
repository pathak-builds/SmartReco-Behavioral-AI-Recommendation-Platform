from app.database import SessionLocal
from app.models.product import Product
from app.services.embedding_service import EmbeddingService


def main():
    db = SessionLocal()
    embedding_service = EmbeddingService()

    products = (
        db.query(Product)
        .filter(Product.is_active.is_(True))
        .all()
    )

    print(f"Found {len(products)} products")

    for product in products:
        embedding_service.upsert_product(product)
        print(f"Indexed: {product.name}")

    print(f"\nTotal vectors: {embedding_service.count()}")

    db.close()


if __name__ == "__main__":
    main()