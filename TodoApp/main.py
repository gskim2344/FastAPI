from fastapi import FastAPI,Request,status
from .models import Base
from .database import engine
from .routers import auth, todos, admin,users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import logging
from pyngrok import ngrok

ngrok.set_auth_token("30fEKgtiPBhoLf3IL1fjcCdu7Eb_7QmnUgK5XHNDbidEkizW8")
# 8000 포트에 대한 공개 터널 생성
public_url = ngrok.connect(8000)
print("Public URL:", public_url)

logging.basicConfig(
    filename='/home/ec2-user/app/logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="TodoApp/templates")

app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")
@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


@app.api_route("/healthy", methods=["GET", "POST"])
async def health_check(request: Request):
    logging.info("healthy")
    data = await request.json()
    print("📦 받은 데이터:", data)
    return {"status": "healthy received", "data": data}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
