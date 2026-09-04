from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import secrets
import uvicorn

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

db = client["ass20_database"]
users_collection = db["users"]

sessions = {}

# Login page
@app.get("/")
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


# Login
@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):

    user = users_collection.find_one({
        "username": username,
        "password": password
    })

    if user is None:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    session_id = secrets.token_hex(16)

    sessions[session_id] = {
        "username": user["username"],
        "role": user["role"]
    }

    response = RedirectResponse(
        url="/profile",
        status_code=303
    )

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True
    )

    return response


# Profile
@app.get("/profile")
def profile(request: Request):

    session_id = request.cookies.get("session_id")

    if session_id not in sessions:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    user = sessions[session_id]

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "username": user["username"],
            "role": user["role"]
        }
    )


# Admin
@app.get("/admin")
def admin_page(request: Request):

    session_id = request.cookies.get("session_id")

    if session_id not in sessions:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    user = sessions[session_id]

    if user["role"] != "admin":

        return {
            "message": "Access denied. Admin only."
        }

    page = int(
        request.query_params.get("page", 1)
    )

    limit = 2

    skip = (page - 1) * limit

    users = list(
        users_collection.find(
            {},
            {
                "_id": 0,
                "password": 0
            }
        )
        .skip(skip)
        .limit(limit)
    )

    total_users = users_collection.count_documents({})

    total_pages = (total_users + limit - 1) // limit

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "users": users,
            "page": page,
            "total_pages": total_pages
        }
    )


# Logout
@app.get("/logout")
def logout(request: Request):

    session_id = request.cookies.get("session_id")

    if session_id in sessions:

        del sessions[session_id]

    response = RedirectResponse(
        url="/",
        status_code=303
    )

    response.delete_cookie("session_id")

    return response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


