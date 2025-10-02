from fastapi import FastAPI
from api.routes import chat_routes

app = FastAPI(title="Memory Chatbot API")

app.include_router(chat_routes.router)
