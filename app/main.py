from fastapi import FastAPI

from app.authors.router import router as authors_router

app = FastAPI(
    title="Библиотека",
    root_path="",
)

app.include_router(authors_router)


