from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
try:
    from .graph import ask_question
    from .config import SESSION_SECRET
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from graph import ask_question
    from config import SESSION_SECRET

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)
app.mount("/static", StaticFiles(directory=BASE_DIR / "app" / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "app" / "templates")


class ChatRequest(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/api/chat/")
def chat(request: Request, data: ChatRequest):
    question = data.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Please enter a question.")
    try:
        history = request.session.get("history", [])
        answer = ask_question(question, history)
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
        request.session["history"] = history[-10:]
        return {"answer": answer}
    except Exception as error:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(error))
