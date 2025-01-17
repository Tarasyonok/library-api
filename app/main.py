from fastapi import FastAPI

from app.authors.router import router as authors_router
from app.books.router import router as books_router
from app.users.router import auth_router
from app.users.router import router as users_router
from app.lendings.router import router as lendings_router

app = FastAPI(
    title="Библиотека",
    root_path="",
)

app.include_router(authors_router)
app.include_router(books_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(lendings_router)



