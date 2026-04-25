"""Route for phonon calculations."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from janus_api.constants import DATA_DIR
from janus_api.schemas.phonons_schemas import PhononsRequest
from janus_api.utils.phonons_helper import phonons

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/phonons", tags=["calculations"])


@router.post("/")
async def get_phonons(request: PhononsRequest) -> dict[str, Any]:
    """
    Endpoint to perform phonon calculations and return thermal properties.

    Parameters
    ----------
    request : PhononsRequest
        The request body containing the parameters for the calculation.

    Returns
    -------
    dict[str, Any]
        Thermal properties: temperatures, heat_capacity, entropy, free_energy.

    Raises
    ------
    HTTPException
        If there is an error during the calculation.
    """
    struct_path = DATA_DIR / request.struct
    logger.info("Request contents: %s", request)

    try:
        results = phonons(
            struct=struct_path,
            **request.model_dump(exclude={"struct"}),
        )
        return JSONResponse(content={"results": results})
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error - {e}") from e
