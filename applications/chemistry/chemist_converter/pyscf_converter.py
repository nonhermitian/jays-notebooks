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
"""PyScF converter"""
import numpy as np
import pyscf
from opt_einsum import contract
from qiskit_nature.second_q.operators.symmetric_two_body import fold

from .qcschema_data import QCSchemaData
from .general import to_qcschema


def pyscf_to_qcschema(mf, include_dipole=True):
    """Convert a PySCF object to QCSchema

    Parameters:
        mf (pyscf.scf.hf.RHF): Input PySCF object
    """
    data = QCSchemaData()

    data.mo_coeff = mf.mo_coeff
    data.mo_energy = mf.mo_energy
    data.mo_occ = mf.mo_occ
    data.hij = mf.get_hcore()
    data.hij_mo = np.dot(np.dot(data.mo_coeff.T, data.hij), data.mo_coeff)
    data.eri = mf.mol.intor("int2e", aosym=8)
    data.eri_mo = fold(pyscf.ao2mo.full(mf.mol, data.mo_coeff, aosym=4))
    data.e_nuc = pyscf.gto.mole.energy_nuc(mf.mol)
    data.e_ref = mf.e_tot
    data.symbols = [mf.mol.atom_pure_symbol(i) for i in range(mf.mol.natm)]
    data.coords = mf.mol.atom_coords(unit="Bohr").ravel().tolist()
    data.multiplicity = mf.mol.spin + 1
    data.charge = mf.mol.charge
    data.masses = list(mf.mol.atom_mass_list())
    data.method = mf.__class__.__name__
    data.basis = mf.mol.basis
    data.creator = "PySCF"
    data.version = pyscf.__version__
    data.nbasis = mf.mol.nbas
    data.nmo = mf.mol.nao
    data.nalpha = mf.mol.nelec[0]
    data.nbeta = mf.mol.nelec[1]

    if include_dipole:
        mf.mol.set_common_orig((0, 0, 0))
        ao_dip = mf.mol.intor_symmetric("int1e_r", comp=3)

        d_m = mf.make_rdm1(mf.mo_coeff, mf.mo_occ)

        if not (isinstance(d_m, np.ndarray) and d_m.ndim == 2):
            d_m = d_m[0] + d_m[1]

        elec_dip = np.negative(contract("xij,ji->x", ao_dip, d_m).real)
        elec_dip = np.round(elec_dip, decimals=8)
        nucl_dip = contract("i,ix->x", mf.mol.atom_charges(), mf.mol.atom_coords())
        nucl_dip = np.round(nucl_dip, decimals=8)
        ref_dip = nucl_dip + elec_dip

        data.dip_nuc = nucl_dip
        data.dip_ref = ref_dip

        data.dip_x = ao_dip[0]
        data.dip_y = ao_dip[1]
        data.dip_z = ao_dip[2]
        data.dip_mo_x_a = np.dot(np.dot(data.mo_coeff.T, data.dip_x), data.mo_coeff)
        data.dip_mo_y_a = np.dot(np.dot(data.mo_coeff.T, data.dip_y), data.mo_coeff)
        data.dip_mo_z_a = np.dot(np.dot(data.mo_coeff.T, data.dip_z), data.mo_coeff)

    return to_qcschema(data, include_dipole=include_dipole)
