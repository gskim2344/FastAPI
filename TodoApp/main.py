from fastapi import FastAPI,Request,status
from .models import Base
from .database import engine
from .routers import auth, todos, admin,users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import logging
from pyngrok import ngrok
from TodoApp.modules.google_calendar import GoogleCalendar
import requests

ngrok.set_auth_token("30fEKgtiPBhoLf3IL1fjcCdu7Eb_7QmnUgK5XHNDbidEkizW8")

LAMBDA_ENDPOINT = "https://mov33u6lfk.execute-api.ap-northeast-1.amazonaws.com/Prod/api_endpoint"

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

    calendar=GoogleCalendar()
    calendar.add_calendar()
    calendar.get_available_slots("2025-08-01")
    send_to_lambda()
    return {"status": "healthy received", "data": data}

def send_to_lambda():
    payload = {
        "type": "line_event",
        "user": "테스트",
        "message": "예약 요청"
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(LAMBDA_ENDPOINT, json=payload, headers=headers)

    print(response.status_code)
    print(response.text)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
