from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.database import close_driver

from app.routes.jobs import router as jobs_router
from app.routes.candidates import router as candidates_router
from app.routes.recommendations import router as recommendations_router
from app.routes.graph import router as graph_router


app = FastAPI(
    title="JobGraph API",
    description="Graph-based Job Recommendation System",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.include_router(jobs_router)
app.include_router(candidates_router)
app.include_router(recommendations_router)
app.include_router(graph_router)


@app.get("/")
def root():

    return {
        "message": "Welcome to JobGraph API"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.on_event("shutdown")
def shutdown_event():

    close_driver()