"""Schemas for phonon calculation functions."""

from __future__ import annotations

from janus_core.helpers.janus_types import Architectures
from pydantic import BaseModel


class PhononsRequest(BaseModel):
    """Validation for phonon calculation requests."""

    struct: str
    arch: Architectures = "mace_mp"
    supercell: int = 2
    displacement: float = 0.01
    symmetrize: bool = False
    temp_min: float = 0.0
    temp_max: float = 1000.0
    temp_step: float = 50.0


class PhononsResults(BaseModel):
    """Validation for phonon calculation results."""

    temperatures: list[float] | None = None
    heat_capacity: list[float] | None = None
    entropy: list[float] | None = None
    free_energy: list[float] | None = None
    band_svg: str | None = None
    band_yaml: str | None = None
