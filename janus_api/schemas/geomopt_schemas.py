"""Schemas for geometry optimisation calculation functions."""

from __future__ import annotations

from pathlib import Path

from janus_core.helpers.janus_types import Architectures
from pydantic import BaseModel


class GeomOptResults(BaseModel):
    """Class validation for geometry optimisation results."""

    results_path: Path | None
    traj_path: Path | None
    final_energy: float | None
    max_force: float | None
    initial_spacegroup: str | None
    final_spacegroup: str | None
    emissions: float | None


class GeomOptRequest(BaseModel):
    """Class validation for geometry optimisation requests."""

    struct: str
    arch: Architectures | None = "mace_mp"
    fmax: float | None = 0.1
    steps: int | None = 1000
    format: str | None = "cif"
    relax_mode: str = "ionic"
