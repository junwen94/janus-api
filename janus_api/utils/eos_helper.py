"""Helper functions for performing equation of state calculations."""

from __future__ import annotations

from pathlib import Path

from janus_core.calculations.eos import EoS
from janus_core.helpers.janus_types import Architectures, EoSNames

from janus_api.constants import DATA_DIR
from janus_api.utils.data_conversion_helper import handle_data_types


def eos(
    struct: Path,
    arch: Architectures = "mace_mp",
    min_volume: float = 0.95,
    max_volume: float = 1.05,
    n_volumes: int = 7,
    eos_type: EoSNames = "birchmurnaghan",
    results_path: Path = DATA_DIR,
) -> dict:
    """
    Perform equation of state calculation and return fitted parameters.

    Parameters
    ----------
    struct : Path
        Path of structure to simulate.
    arch : Architectures
        MLIP architecture. Default is "mace_mp".
    min_volume : float
        Minimum volume scaling factor. Default is 0.95.
    max_volume : float
        Maximum volume scaling factor. Default is 1.05.
    n_volumes : int
        Number of volume points to sample. Default is 7.
    eos_type : EoSNames
        EoS fit type. Default is "birchmurnaghan".
    results_path : Path
        Directory to write output files.

    Returns
    -------
    dict
        bulk_modulus, v_0, e_0, plus raw volumes and energies arrays.
    """
    eos_calc = EoS(
        struct=struct,
        arch=arch,
        device="cpu",
        min_volume=min_volume,
        max_volume=max_volume,
        n_volumes=n_volumes,
        eos_type=eos_type,
        minimize=True,
        write_results=True,
        file_prefix=str(results_path / struct.stem),
    )
    results = eos_calc.run()

    return {
        "bulk_modulus": results.get("bulk_modulus"),
        "v_0": results.get("v_0"),
        "e_0": results.get("e_0"),
        "volumes": handle_data_types(getattr(eos_calc, "volumes", None)),
        "energies": handle_data_types(getattr(eos_calc, "energies", None)),
    }
