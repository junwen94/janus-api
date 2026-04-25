"""Route for NEB calculations."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from janus_api.constants import DATA_DIR
from janus_api.schemas.neb_schemas import NEBRequest
from janus_api.utils.neb_helper import neb

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/neb", tags=["calculations"])


@router.post("/")
async def get_neb(request: NEBRequest) -> dict[str, Any]:
    """
    Endpoint to run NEB calculation and return barrier information.

    Parameters
    ----------
    request : NEBRequest
        The request body containing init/final structures and NEB parameters.

    Returns
    -------
    dict[str, Any]
        barrier, delta_e, max_force.

    Raises
    ------
    HTTPException
        If there is an error during the calculation.
    """
    init_path = DATA_DIR / request.init_struct
    final_path = DATA_DIR / request.final_struct
    logger.info("Request contents: %s", request)

    try:
        results = neb(
            init_struct=init_path,
            final_struct=final_path,
            **request.model_dump(exclude={"init_struct", "final_struct"}),
        )
        return JSONResponse(content={"results": results})
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error - {e}") from e
