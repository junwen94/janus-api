"""Helper functions for performing phonon calculations."""

from __future__ import annotations

from pathlib import Path

from janus_core.calculations.phonons import Phonons
from janus_core.helpers.janus_types import Architectures

from janus_api.constants import DATA_DIR
from janus_api.utils.data_conversion_helper import handle_data_types


def phonons(
    struct: Path,
    arch: Architectures = "mace_mp",
    supercell: int = 2,
    displacement: float = 0.01,
    symmetrize: bool = False,
    temp_min: float = 0.0,
    temp_max: float = 1000.0,
    temp_step: float = 50.0,
    results_path: Path = DATA_DIR,
) -> dict:
    """
    Perform phonon calculations and return thermal properties.

    Parameters
    ----------
    struct : Path
        Path of structure to simulate.
    arch : Architectures
        MLIP architecture. Default is "mace_mp".
    supercell : int
        Supercell scaling (same in all directions). Default is 2.
    displacement : float
        Atomic displacement in Å. Default is 0.01.
    symmetrize : bool
        Whether to symmetrize force constants. Default is False.
    temp_min : float
        Minimum temperature in K. Default is 0.0.
    temp_max : float
        Maximum temperature in K. Default is 1000.0.
    temp_step : float
        Temperature step in K. Default is 50.0.
    results_path : Path
        Directory to write output files.

    Returns
    -------
    dict
        Thermal properties: temperatures, heat_capacity, entropy, free_energy.
    """
    phonons_calc = Phonons(
        struct=struct,
        arch=arch,
        device="cpu",
        supercell=supercell,
        displacement=displacement,
        symmetrize=symmetrize,
        calcs=("thermal",),
        temp_min=temp_min,
        temp_max=temp_max,
        temp_step=temp_step,
        write_results=True,
        hdf5=False,
        file_prefix=str(results_path / struct.stem),
    )
    phonons_calc.run()

    thermal = phonons_calc.results.get("thermal", {})
    return {
        "temperatures": handle_data_types(thermal.get("temperatures")),
        "heat_capacity": handle_data_types(thermal.get("heat_capacity")),
        "entropy": handle_data_types(thermal.get("entropy")),
        "free_energy": handle_data_types(thermal.get("free_energy")),
    }
