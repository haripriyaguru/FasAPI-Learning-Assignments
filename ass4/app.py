from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...)
):
    content = await file.read()

    text_content = content.decode("utf-8")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "filename": file.filename,
            "content": text_content
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )