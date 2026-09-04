from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()


# -------------------------
# CORS Middleware
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# -------------------------
# Custom Middleware
# -------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.time()

    print("Request Method:", request.method)
    print("Request URL:", request.url)

    response = await call_next(request)

    process_time = time.time() - start_time

    print("Response Status:", response.status_code)
    print("Process Time:", process_time)

    return response


# -------------------------
# Home
# -------------------------

@app.get("/")
def home():

    return {
        "message": "Middleware Demo"
    }


# -------------------------
# Students
# -------------------------

@app.get("/students")
def get_students():

    return {
        "students": [
            "Hari",
            "Priya",
            "Arun"
        ]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )