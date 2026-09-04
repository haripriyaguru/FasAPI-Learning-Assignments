from fastapi import FastAPI, Response, Request, Form
import uvicorn

app = FastAPI()


# Session storage
sessions = {}


# Home
@app.get("/")
def home():
    return {
        "message": "Session Login API"
    }


# Login
@app.post("/login")
def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):

    if username == "hari" and password == "12345":

        session_id = "abc123"

        # Store session on server
        sessions[session_id] = username

        # Store session ID in browser cookie
        response.set_cookie(
            key="session_id",
            value=session_id
        )

        return {
            "message": "Login successful"
        }

    return {
        "message": "Invalid username or password"
    }


# Profile
@app.get("/profile")
def profile(request: Request):

    # Read cookie
    session_id = request.cookies.get("session_id")

    # Check session
    if session_id not in sessions:
        return {
            "message": "Please login first"
        }

    username = sessions[session_id]

    return {
        "message": "Welcome",
        "username": username
    }


# Logout
@app.get("/logout")
def logout(
    request: Request,
    response: Response
):

    # Read session ID
    session_id = request.cookies.get("session_id")

    # Delete session
    if session_id in sessions:
        del sessions[session_id]

    # Delete cookie
    response.delete_cookie("session_id")

    return {
        "message": "Logout successful"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
