"""Schemas for equation of state calculation functions."""

from __future__ import annotations

from janus_core.helpers.janus_types import Architectures, EoSNames
from pydantic import BaseModel


class EoSRequest(BaseModel):
    """Validation for EoS calculation requests."""

    struct: str
    arch: Architectures = "mace_mp"
    min_volume: float = 0.95
    max_volume: float = 1.05
    n_volumes: int = 7
    eos_type: EoSNames = "birchmurnaghan"


class EoSResults(BaseModel):
    """Validation for EoS calculation results."""

    bulk_modulus: float | None = None
    v_0: float | None = None
    e_0: float | None = None
    volumes: list[float] | None = None
    energies: list[float] | None = None
    eos_svg: str | None = None
