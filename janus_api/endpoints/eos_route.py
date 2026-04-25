"""Route for equation of state calculations."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from janus_api.constants import DATA_DIR
from janus_api.schemas.eos_schemas import EoSRequest
from janus_api.utils.eos_helper import eos

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/eos", tags=["calculations"])


@router.post("/")
async def get_eos(request: EoSRequest) -> dict[str, Any]:
    """
    Endpoint to perform EoS calculation and return fitted parameters.

    Parameters
    ----------
    request : EoSRequest
        The request body containing the parameters for the calculation.

    Returns
    -------
    dict[str, Any]
        bulk_modulus, v_0, e_0, volumes, energies.

    Raises
    ------
    HTTPException
        If there is an error during the calculation.
    """
    struct_path = DATA_DIR / request.struct
    logger.info("Request contents: %s", request)

    try:
        results = eos(
            struct=struct_path,
            **request.model_dump(exclude={"struct"}),
        )
        return JSONResponse(content={"results": results})
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error - {e}") from e
