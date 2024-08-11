from fastapi import FastAPI
from routers import books, users, auth

app = FastAPI()


app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System"}