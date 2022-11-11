from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

DB_URL = "https://api.npoint.io/fce75509e3b02db89cea"

app = FastAPI()

user_db = []

# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def fetch_users():
    response = requests.get(url=DB_URL)
    response.raise_for_status()
    data = response.json()

    for user in data:
        user_db.append(user)


fetch_users()

@app.get("/")
async def root():
    return user_db


@app.get("/{user_id}")
async def show_user(user_id: int):
    return user_db[user_id-1]
