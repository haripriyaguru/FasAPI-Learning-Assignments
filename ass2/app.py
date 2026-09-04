from fastapi import FastAPI, Request, Form
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


@app.post("/reverse")
def reverse_text(request: Request, text: str = Form(...)):
    reversed_text = text[::-1]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "original_text": text,
            "reversed_text": reversed_text
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )