from fastapi import FastAPI
from routers.todo import router
from routers.auth import router as auth_router
from models.connect import create_db_and_table
from contextlib import asynccontextmanager
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_table()
    yield
    print("Shutting down...")

app = FastAPI(
    title="To-Do API", 
    description="A simple To-Do API built with FastAPI", 
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(router=router)
app.include_router(router=auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
