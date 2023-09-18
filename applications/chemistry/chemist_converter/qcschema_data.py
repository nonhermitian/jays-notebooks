# This code is part of a Qiskit project.
#
# (C) Copyright IBM 2023.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""QCSchema data class"""

from typing import Any, Sequence
import numpy as np


class QCSchemaData:
    """An internal data container to simplify the construction of QCSchema objects."""

    hij: np.ndarray | None = None
    hij_b: np.ndarray | None = None
    eri: np.ndarray | None = None
    hij_mo: np.ndarray | None = None
    hij_mo_b: np.ndarray | None = None
    eri_mo: np.ndarray | None = None
    eri_mo_ba: np.ndarray | None = None
    eri_mo_bb: np.ndarray | None = None
    e_nuc: float | None = None
    e_ref: float | None = None
    mo_coeff: np.ndarray | None = None
    mo_coeff_b: np.ndarray | None = None
    mo_energy: np.ndarray | None = None
    mo_energy_b: np.ndarray | None = None
    mo_occ: np.ndarray | None = None
    mo_occ_b: np.ndarray | None = None
    dip_x: np.ndarray | None = None
    dip_y: np.ndarray | None = None
    dip_z: np.ndarray | None = None
    dip_mo_x_a: np.ndarray | None = None
    dip_mo_y_a: np.ndarray | None = None
    dip_mo_z_a: np.ndarray | None = None
    dip_mo_x_b: np.ndarray | None = None
    dip_mo_y_b: np.ndarray | None = None
    dip_mo_z_b: np.ndarray | None = None
    dip_nuc: tuple[float, float, float] | None = None
    dip_ref: tuple[float, float, float] | None = None
    symbols: Sequence[str] | None = None
    coords: Sequence[float] | None = None
    multiplicity: int | None = None
    charge: int | None = None
    masses: Sequence[float] | None = None
    method: str | None = None
    basis: str | None = None
    creator: str | None = None
    version: str | None = None
    routine: str | None = None
    nbasis: int | None = None
    nmo: int | None = None
    nalpha: int | None = None
    nbeta: int | None = None
    keywords: dict[str, Any] | None = None