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
    Perform phonon calculations and return band structure + thermal properties.

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
        thermal properties + band_svg (SVG string) + band_yaml (phonopy YAML with eigenvectors).
    """
    phonons_calc = Phonons(
        struct=struct,
        arch=arch,
        device="cpu",
        supercell=supercell,
        displacement=displacement,
        symmetrize=symmetrize,
        calcs=("bands", "thermal"),
        temp_min=temp_min,
        temp_max=temp_max,
        temp_step=temp_step,
        write_results=True,
        plot_to_file=True,
        hdf5=False,
        file_prefix=str(results_path / struct.stem),
    )
    phonons_calc.run()

    # Thermal properties (key is 'thermal_properties', not 'thermal')
    thermal = phonons_calc.results.get("thermal_properties", {})

    # SVG band structure plot written to disk by janus-core
    svg_path = Path(phonons_calc.bands_plot_file) if phonons_calc.bands_plot_file else None
    band_svg = svg_path.read_text() if svg_path and svg_path.exists() else None

    # band.yaml with eigenvectors — written from the phonopy object
    phonopy_obj = phonons_calc.results.get("phonon")
    band_yaml = None
    if phonopy_obj is not None:
        band_yaml_path = results_path / f"{struct.stem}-bands-eigvec.yaml"
        phonopy_obj.write_yaml_band_structure(filename=str(band_yaml_path))
        if band_yaml_path.exists():
            band_yaml = band_yaml_path.read_text()

    return {
        "temperatures": handle_data_types(thermal.get("temperatures")),
        "heat_capacity": handle_data_types(thermal.get("heat_capacity")),
        "entropy": handle_data_types(thermal.get("entropy")),
        "free_energy": handle_data_types(thermal.get("free_energy")),
        "band_svg": band_svg,
        "band_yaml": band_yaml,
    }
