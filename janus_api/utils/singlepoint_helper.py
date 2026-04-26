"""Helper functions for performing singeploint calculations."""

from __future__ import annotations

from pathlib import Path

from janus_core.calculations.single_point import SinglePoint
from janus_core.helpers.janus_types import Architectures, Properties

from janus_api.constants import DATA_DIR
from janus_api.schemas.singlepoint_schemas import SinglePointResults
from janus_api.utils.data_conversion_helper import handle_data_types


def singlepoint(
    struct: Path,
    arch: Architectures = "mace_mp",
    properties: list[Properties] = ("energy", "forces", "stress"),
    range_selector: str = ":",
    write_results: bool = True,
    results_path: Path = DATA_DIR,
    format: str = "cif",
) -> SinglePointResults:
    """
    Perform single point calculations and return results.

    Parameters
    ----------
    struct : Path
        Path of structure to simulate.
    arch : Architectures
        MLIP architecture to use for single point calculations. Default is "mace_mp".
    properties : List[Properties]
        Physical properties to calculate. Default is ("energy", "forces", "stress").
    range_selector : str
        Range of indices to include from the structure. Default is all.
    write_results : bool
        Tells function if to save the results of the calculation or not, default
        is True.
    results_path : Path
        Location to save the results default is DATA_DIR.
    file_format : str
        File format to output results as, default is "cif".

    Returns
    -------
    SinglePointResults
        Results of the single point calculations.
    """
    read_kwargs = {"index": range_selector}
    results_path = results_path / f"{struct.stem}-spoint-results.{format}"
    write_kwargs = {"filename": results_path, "format": format}

    singlepoint_kwargs = {
        "struct": struct,
        "properties": properties,
        "arch": arch,
        "device": "cpu",
        "read_kwargs": read_kwargs,
        "write_results": write_results,
        "write_kwargs": write_kwargs,
    }

    s_point = SinglePoint(**singlepoint_kwargs)

    s_point.run()
    results = handle_data_types(s_point.results)
    results["results_path"] = results_path

    return results
