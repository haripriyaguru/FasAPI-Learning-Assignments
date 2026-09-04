from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}


@app.get("/about")
def about():
    return {"message": "This is About page"}


@app.post("/users")
def create_user():
    return {"message": "User created"}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )