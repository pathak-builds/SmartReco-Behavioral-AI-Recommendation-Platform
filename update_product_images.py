from app.database import SessionLocal
from app.models.product import Product

db = SessionLocal()

try:

    image_map = {
        "Complete Generative AI Bootcamp": "/static/images/genai.jpg",
        "LLM Engineering Professional": "/static/images/llm.jpg",
        "LangGraph Masterclass": "/static/images/langgraph.jpg",
        "Production RAG Systems": "/static/images/rag.jpg",
        "Python for AI Engineers": "/static/images/python.jpg",
    }

    products = db.query(Product).all()

    for product in products:

        if product.name in image_map:

            product.image_url = image_map[product.name]

            print(f"Updated: {product.name}")

    db.commit()

    print("\nAll product images updated successfully!")

finally:

    db.close()