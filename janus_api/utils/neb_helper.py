"""Helper functions for performing NEB calculations."""

from __future__ import annotations

import io
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ase.io import write as ase_write

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
    interpolator: str = "pymatgen",
    results_path: Path = DATA_DIR,
) -> dict:
    """
    Run NEB calculation and return barrier, energy profile SVG, and trajectory.

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
    interpolator : str
        Interpolation method ("pymatgen" or "ase"). Default is "pymatgen".
    results_path : Path
        Directory to write output files.

    Returns
    -------
    dict
        barrier, delta_e, max_force, neb_svg, neb_traj (extxyz string).
    """
    def _make_neb(interp: str) -> NEB:
        return NEB(
            init_struct=init_struct,
            final_struct=final_struct,
            arch=arch,
            device="cpu",
            n_images=n_images,
            fmax=fmax,
            steps=steps,
            minimize=True,
            interpolator=interp,
            write_results=True,
            file_prefix=str(results_path / "neb"),
        )

    neb_calc = _make_neb(interpolator)
    try:
        results = neb_calc.run()
    except Exception as e:
        if interpolator != "ase" and "singular" in str(e).lower():
            # pymatgen IDPP failed — fall back to ASE linear interpolation
            neb_calc = _make_neb("ase")
            results = neb_calc.run()
        else:
            raise

    # Energy profile SVG
    neb_svg = None
    try:
        fig = neb_calc.nebtools.plot_band()
        buf = io.StringIO()
        fig.savefig(buf, format="svg", bbox_inches="tight")
        plt.close(fig)
        neb_svg = buf.getvalue()
    except Exception:
        pass

    # NEB trajectory as extxyz (all images including endpoints)
    neb_traj = None
    try:
        images = neb_calc.nebtools.images
        buf_xyz = io.StringIO()
        ase_write(buf_xyz, images, format="extxyz")
        neb_traj = buf_xyz.getvalue()
    except Exception:
        pass

    return handle_data_types(
        {
            "barrier": results.get("barrier"),
            "delta_e": results.get("delta_E"),
            "max_force": results.get("max_force"),
            "neb_svg": neb_svg,
            "neb_traj": neb_traj,
        }
    )
