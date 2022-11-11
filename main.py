from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import User
import requests

DB_URL = "https://api.npoint.io/fce75509e3b02db89cea"

app = FastAPI()

user_db = []

templates = Jinja2Templates(directory="templates")


def fetch_users():
    response = requests.get(url=DB_URL)
    response.raise_for_status()
    data = response.json()

    for user in data:
        user_db.append(User(
            id=user["id"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            password=user["password"],
            currency=user["currency"],
            balance=user["balance"]
        ))


fetch_users()

@app.get("/")
async def root():
    return user_db


@app.get("/users/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    user = user_db[user_id-1]
    return templates.TemplateResponse("user.html", {"request": request, "user": user})
