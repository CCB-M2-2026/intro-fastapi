from fastapi import FastAPI
from src.characters.infraestructure.api import router as character_router

app= FastAPI()
app.include_router(character_router)

