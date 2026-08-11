from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.database import close_driver

from app.routes.jobs import router as jobs_router
from app.routes.candidates import router as candidates_router
from app.routes.recommendations import router as recommendations_router
from app.routes.graph import router as graph_router


# =====================================================
# FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title="JobGraph API",
    description="Graph-based Job Recommendation System",
    version="1.0.0"
)


# =====================================================
# CORS CONFIGURATION
# =====================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =====================================================
# API ROUTES
# =====================================================

app.include_router(jobs_router)

app.include_router(candidates_router)

app.include_router(recommendations_router)

app.include_router(graph_router)


# =====================================================
# ROOT ENDPOINT
# =====================================================

@app.get("/")
def root():

    return {
        "message": "Welcome to JobGraph API"
    }


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =====================================================
# SHUTDOWN
# =====================================================

@app.on_event("shutdown")
def shutdown_event():

    close_driver()