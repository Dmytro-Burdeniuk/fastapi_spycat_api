from fastapi import FastAPI

from src.database.session import db_session_manager, Base
from src.database import models  # noqa: F401
from src.routes import cat_routes, mission_routes

# For this assessment: create tables at startup
Base.metadata.create_all(bind=db_session_manager.engine)

app = FastAPI(
    title="Spy Cat Agency API",
    version="1.0.0",
)

app.include_router(cat_routes.router)
app.include_router(mission_routes.router)
