from fastapi import FastAPI, Form, UploadFile, File
import uvicorn

app = FastAPI()


@app.post("/register")
async def register(
    name: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...)
):
    content = await file.read()

    return {
        "name": name,
        "email": email,
        "filename": file.filename,
        "message": "Registration successful"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
