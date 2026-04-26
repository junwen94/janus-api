"""Contains routes for performing geometry optimisation calculations."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from janus_api.constants import DATA_DIR
from janus_api.schemas.geomopt_schemas import GeomOptRequest
from janus_api.utils.geomopt_helper import geomopt

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/geomopt", tags=["calculations"])


@router.post("/")
async def get_geomopt(request: GeomOptRequest) -> dict[str, Any]:
    """Perform geometry optimisation and return results with optimised structure."""
    struct_path = DATA_DIR / request.struct
    logger.info("Request contents: %s", request)

    try:
        results = geomopt(
            struct=struct_path,
            **request.model_dump(exclude={"struct"}, exclude_none=True),
        )
        return JSONResponse(content={"results": results})
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error - {e}"
        ) from e
