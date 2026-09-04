from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import uvicorn

app = FastAPI()


# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# OAuth2
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# Fake user database
users = {
    "hari": {
        "username": "hari",
        "hashed_password": pwd_context.hash("12345")
    }
}


# Verify password
def verify_password(plain_password, hashed_password):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# Login
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = users.get(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return {
        "message": "Login successful",
        "username": user["username"]
    }


# Protected route
@app.get("/profile")
def profile(
    token: str = Depends(oauth2_scheme)
):

    return {
        "message": "You can access this protected route",
        "token": token
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )