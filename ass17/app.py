from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import uvicorn

app = FastAPI()


# -------------------------
# JWT Configuration
# -------------------------

SECRET_KEY = "my-secret-key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# -------------------------
# Password Hashing
# -------------------------

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# -------------------------
# OAuth2
# -------------------------

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# -------------------------
# Fake User Database
# -------------------------

users = {
    "hari": {
        "username": "hari",
        "hashed_password": pwd_context.hash("12345")
    }
}


# -------------------------
# Verify Password
# -------------------------

def verify_password(
    plain_password,
    hashed_password
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# -------------------------
# Create JWT Token
# -------------------------

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# -------------------------
# Login
# -------------------------

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = users.get(form_data.username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        user["hashed_password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token_expires = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = create_access_token(
        data={
            "sub": user["username"]
        },
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# -------------------------
# Get Current User
# -------------------------

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = users.get(username)

    if user is None:
        raise credentials_exception

    return user


# -------------------------
# Protected Route
# -------------------------

@app.get("/profile")
def profile(
    current_user = Depends(get_current_user)
):

    return {
        "message": "Access granted",
        "username": current_user["username"]
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )