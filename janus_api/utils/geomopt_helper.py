"""Helper functions for performing geometry optimisation calculations."""

from __future__ import annotations

from io import StringIO
from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import write as ase_write
from janus_core.calculations.geom_opt import GeomOpt
from janus_core.helpers.janus_types import Architectures

from janus_api.constants import DATA_DIR


def geomopt(
    struct: Path,
    arch: Architectures | None = "mace_mp",
    fmax: float = 0.1,
    steps: int = 1000,
    relax_mode: str = "ionic",
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
    relax_mode : str
        One of "ionic" (positions only), "cell" (hydrostatic), or "full".

    Returns
    -------
    dict
        final_energy, max_force, optimised_structure (CIF string).

    Notes
    -----
    Pipeline: GeomOpt writes extxyz (janus-core native) → ASE reads back →
    clean Atoms (no info dict) → CIF string. The clean step drops
    final_spacegroup from atoms.info, preventing ASE from writing a CIF
    with a space group name but no symmetry operations (which WEAS rejects).
    """
    traj_path = DATA_DIR / f"{struct.stem}-traj.traj"

    geomopt_kwargs: dict = {
        "struct": struct,
        "arch": arch,
        "device": "cpu",
        "fmax": fmax,
        "steps": steps,
        "write_results": False,
        "write_traj": True,
        "traj_kwargs": {"filename": str(traj_path)},
    }

    if relax_mode == "ionic":
        geomopt_kwargs["filter_class"] = None
    elif relax_mode == "cell":
        geomopt_kwargs["filter_kwargs"] = {"hydrostatic_strain": True}
    # "full": janus-core default FrechetCellFilter

    geom_opt = GeomOpt(**geomopt_kwargs)
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
        # Strip info dict (contains final_spacegroup set by janus-core) before
        # writing CIF — prevents ASE from emitting a space group name without
        # symmetry operations, which WEAS cannot parse.
        clean = Atoms(
            symbols=opt_struct.get_chemical_symbols(),
            positions=opt_struct.get_positions(),
            cell=opt_struct.get_cell(),
            pbc=opt_struct.get_pbc(),
        )
        sio = StringIO()
        ase_write(sio, clean, format="cif")
        optimised_structure = sio.getvalue()
    except Exception:
        optimised_structure = None

    return {
        "final_energy": final_energy,
        "max_force": max_force,
        "optimised_structure": optimised_structure,
    }
