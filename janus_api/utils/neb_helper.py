"""Helper functions for performing NEB calculations."""

from __future__ import annotations

from pathlib import Path

from janus_core.calculations.neb import NEB
from janus_core.helpers.janus_types import Architectures

from janus_api.constants import DATA_DIR
from janus_api.utils.data_conversion_helper import handle_data_types


def neb(
    init_struct: Path,
    final_struct: Path,
    arch: Architectures = "mace_mp",
    n_images: int = 15,
    fmax: float = 0.1,
    steps: int = 100,
    results_path: Path = DATA_DIR,
) -> dict:
    """
    Run NEB calculation and return barrier information.

    Parameters
    ----------
    init_struct : Path
        Path to the initial structure.
    final_struct : Path
        Path to the final structure.
    arch : Architectures
        MLIP architecture. Default is "mace_mp".
    n_images : int
        Number of intermediate NEB images. Default is 15.
    fmax : float
        Force convergence criterion in eV/Å. Default is 0.1.
    steps : int
        Maximum optimisation steps. Default is 100.
    results_path : Path
        Directory to write output files.

    Returns
    -------
    dict
        barrier (eV), delta_e (eV), max_force (eV/Å).
    """
    neb_calc = NEB(
        init_struct=init_struct,
        final_struct=final_struct,
        arch=arch,
        device="cpu",
        n_images=n_images,
        fmax=fmax,
        steps=steps,
        write_results=True,
        file_prefix=str(results_path / "neb"),
    )
    results = neb_calc.run()

    return handle_data_types(
        {
            "barrier": results.get("barrier"),
            "delta_e": results.get("delta_E"),
            "max_force": results.get("max_force"),
        }
    )
