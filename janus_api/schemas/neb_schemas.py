"""Schemas for NEB calculation functions."""

from __future__ import annotations

from janus_core.helpers.janus_types import Architectures
from pydantic import BaseModel


class NEBRequest(BaseModel):
    """Validation for NEB calculation requests."""

    init_struct: str
    final_struct: str
    arch: Architectures = "mace_mp"
    n_images: int = 15
    fmax: float = 0.1
    steps: int = 100
    interpolator: str = "pymatgen"


class NEBResults(BaseModel):
    """Validation for NEB calculation results."""

    barrier: float | None = None
    delta_e: float | None = None
    max_force: float | None = None
    neb_svg: str | None = None
    neb_traj: str | None = None
