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
"""general conversion step"""
import numpy as np


from qiskit_nature.second_q.operators import Tensor

from .qcschema_data import QCSchemaData
from .qcschema import (QCSchema,
                       QCModel,
                       QCTopology,
                       QCProperties,
                       QCProvenance,
                       QCWavefunction)


def to_qcschema(data: QCSchemaData, include_dipole: bool = True) -> QCSchema:
    molecule = QCTopology(
        schema_name="qcschema_molecule",
        schema_version=2,
        symbols=data.symbols,
        geometry=data.coords,
        molecular_charge=data.charge,
        molecular_multiplicity=data.multiplicity,
        masses=data.masses,
    )

    properties = QCProperties()
    properties.calcinfo_natom = len(data.symbols) if data.symbols is not None else None
    properties.calcinfo_nbasis = data.nbasis
    properties.calcinfo_nmo = data.nmo
    properties.calcinfo_nalpha = data.nalpha
    properties.calcinfo_nbeta = data.nbeta
    properties.return_energy = data.e_ref
    properties.nuclear_repulsion_energy = data.e_nuc
    properties.nuclear_dipole_moment = data.dip_nuc
    properties.scf_dipole_moment = data.dip_ref

    def format_np_array(arr):
        if isinstance(arr, Tensor):
            # NOTE: this also deals with symmetry-reduced integral classes and ensures that
            # they are not automatically unfolded to 1-fold symmetry
            arr = arr.array
        return arr.ravel().tolist()

    wavefunction = QCWavefunction(basis=data.basis)
    if data.mo_coeff is not None:
        wavefunction.orbitals_a = "scf_orbitals_a"
        wavefunction.scf_orbitals_a = format_np_array(data.mo_coeff)
    if data.mo_coeff_b is not None:
        wavefunction.orbitals_b = "scf_orbitals_b"
        wavefunction.scf_orbitals_b = format_np_array(data.mo_coeff_b)
    if data.mo_occ is not None:
        wavefunction.occupations_a = "scf_occupations_a"
        wavefunction.scf_occupations_a = format_np_array(data.mo_occ)
    if data.mo_occ_b is not None:
        wavefunction.occupations_b = "scf_occupations_b"
        wavefunction.scf_occupations_b = format_np_array(data.mo_occ_b)
    if data.mo_energy is not None:
        wavefunction.eigenvalues_a = "scf_eigenvalues_a"
        wavefunction.scf_eigenvalues_a = format_np_array(data.mo_energy)
    if data.mo_energy_b is not None:
        wavefunction.eigenvalues_b = "scf_eigenvalues_b"
        wavefunction.scf_eigenvalues_b = format_np_array(data.mo_energy_b)
    if data.hij is not None:
        wavefunction.fock_a = "scf_fock_a"
        wavefunction.scf_fock_a = format_np_array(data.hij)
    if data.hij_b is not None:
        wavefunction.fock_b = "scf_fock_b"
        wavefunction.scf_fock_b = format_np_array(data.hij_b)
    if data.hij_mo is not None:
        wavefunction.fock_mo_a = "scf_fock_mo_a"
        wavefunction.scf_fock_mo_a = format_np_array(data.hij_mo)
    if data.hij_mo_b is not None:
        wavefunction.fock_mo_b = "scf_fock_mo_b"
        wavefunction.scf_fock_mo_b = format_np_array(data.hij_mo_b)
    if data.eri is not None:
        wavefunction.eri = "scf_eri"
        wavefunction.scf_eri = format_np_array(data.eri)
    if data.eri_mo is not None:
        wavefunction.eri_mo_aa = "scf_eri_mo_aa"
        wavefunction.scf_eri_mo_aa = format_np_array(data.eri_mo)
    if data.eri_mo_ba is not None:
        wavefunction.eri_mo_ba = "scf_eri_mo_ba"
        wavefunction.scf_eri_mo_ba = format_np_array(data.eri_mo_ba)
    if data.eri_mo_bb is not None:
        wavefunction.eri_mo_bb = "scf_eri_mo_bb"
        wavefunction.scf_eri_mo_bb = format_np_array(data.eri_mo_bb)
    if include_dipole:
        if data.dip_x is not None:
            wavefunction.dipole_x = "scf_dipole_x"
            wavefunction.scf_dipole_x = format_np_array(data.dip_x)
        if data.dip_y is not None:
            wavefunction.dipole_y = "scf_dipole_y"
            wavefunction.scf_dipole_y = format_np_array(data.dip_y)
        if data.dip_z is not None:
            wavefunction.dipole_z = "scf_dipole_z"
            wavefunction.scf_dipole_z = format_np_array(data.dip_z)
        if data.dip_mo_x_a is not None:
            wavefunction.dipole_mo_x_a = "scf_dipole_mo_x_a"
            wavefunction.scf_dipole_mo_x_a = format_np_array(data.dip_mo_x_a)
        if data.dip_mo_y_a is not None:
            wavefunction.dipole_mo_y_a = "scf_dipole_mo_y_a"
            wavefunction.scf_dipole_mo_y_a = format_np_array(data.dip_mo_y_a)
        if data.dip_mo_z_a is not None:
            wavefunction.dipole_mo_z_a = "scf_dipole_mo_z_a"
            wavefunction.scf_dipole_mo_z_a = format_np_array(data.dip_mo_z_a)
        if data.dip_mo_x_b is not None:
            wavefunction.dipole_mo_x_b = "scf_dipole_mo_x_b"
            wavefunction.scf_dipole_mo_x_b = format_np_array(data.dip_mo_x_b)
        if data.dip_mo_y_b is not None:
            wavefunction.dipole_mo_y_b = "scf_dipole_mo_y_b"
            wavefunction.scf_dipole_mo_y_b = format_np_array(data.dip_mo_y_b)
        if data.dip_mo_z_b is not None:
            wavefunction.dipole_mo_z_b = "scf_dipole_mo_z_b"
            wavefunction.scf_dipole_mo_z_b = format_np_array(data.dip_mo_z_b)

    qcschema = QCSchema(
        schema_name="qcschema",
        schema_version=3,
        molecule=molecule,
        driver="energy",
        model=QCModel(
            method=data.method,
            basis=data.basis,
        ),
        keywords=data.keywords if data.keywords is not None else {},
        provenance=QCProvenance(
            creator=data.creator,
            version=data.version,
            routine=data.routine if data.routine is not None else "",
        ),
        return_result=data.e_ref,
        success=True,
        properties=properties,
        wavefunction=wavefunction,
    )
    return qcschema