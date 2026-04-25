"""Main module for the application."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from janus_api.constants import FRONTEND_URL, PORT
from janus_api.endpoints import (
    eos_route,
    geomopt_route,
    neb_route,
    phonons_route,
    singlepoint_route,
    upload_route,
)
import logging_config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URL,
    allow_methods=["*"],
)

app.include_router(upload_route.router)
app.include_router(singlepoint_route.router)
app.include_router(geomopt_route.router)
app.include_router(phonons_route.router)
app.include_router(eos_route.router)
app.include_router(neb_route.router)

if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0", port=PORT, log_config=logging_config.LOGGING_CONFIG
    )
