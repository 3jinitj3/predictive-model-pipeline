from fastapi import FastAPI
from app.api.routes import auth, users, ml_models
# from contextlib import asynccontextmanager
# from app.db.session import Database
# from app.db.models.users import Users
# from app.db.models.logins import Logins


# Loads 
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     database = Database()
#     async_engine = database.create_session_objects()
#     database.meta_create_all(async_engine)
#     yield
    

app = FastAPI()
# app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ml_models.router)



@app.get('/')
def read_root():
    return {'message': 'Hello World'}


