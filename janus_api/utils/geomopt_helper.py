"""Helper functions for performing geometry optimisation calculations."""

from __future__ import annotations

from io import StringIO
from pathlib import Path

import numpy as np
from ase.io import write as ase_write
from janus_core.calculations.geom_opt import GeomOpt
from janus_core.helpers.janus_types import Architectures

from janus_api.constants import DATA_DIR


def geomopt(
    struct: Path,
    arch: Architectures | None = "mace_mp",
    fmax: float = 0.1,
    steps: int = 1000,
    format: str | None = "cif",
    **_,
) -> dict:
    """
    Perform geometry optimisation and return results including optimised structure.

    Parameters
    ----------
    struct : Path
        Path of structure to optimise.
    arch : Architectures
        MLIP architecture. Default is "mace_mp".
    fmax : float
        Force convergence criterion in eV/Å. Default is 0.1.
    steps : int
        Maximum optimisation steps. Default is 1000.
    format : str
        Output file format (unused, kept for schema compat).

    Returns
    -------
    dict
        final_energy, max_force, optimised_structure (VASP string).
    """
    traj_path = DATA_DIR / f"{struct.stem}-traj.traj"

    geom_opt = GeomOpt(
        struct=struct,
        arch=arch,
        device="cpu",
        fmax=fmax,
        steps=steps,
        write_results=False,
        write_traj=True,
        traj_kwargs={"filename": str(traj_path)},
    )
    geom_opt.run()

    opt_struct = geom_opt.struct

    try:
        final_energy = float(opt_struct.get_potential_energy())
    except Exception:
        final_energy = None

    try:
        forces = opt_struct.get_forces()
        max_force = float(np.max(np.linalg.norm(forces, axis=1)))
    except Exception:
        max_force = None

    try:
        sio = StringIO()
        ase_write(sio, opt_struct, format="vasp")
        optimised_structure = sio.getvalue()
    except Exception:
        optimised_structure = None

    return {
        "final_energy": final_energy,
        "max_force": max_force,
        "optimised_structure": optimised_structure,
    }
