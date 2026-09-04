from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Parameter Demo"}


# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     return {
#         "type": "Path Parameter",
#         "user_id": user_id
#     }


# @app.get("/products")
# def get_products(category: str):
#     return {
#         "type": "Query Parameter",
#         "category": category
#     }



@app.get("/items")
def list_items(category: str | None = None, limit: int = 10):
    return {"category": category, "limit": limit}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )