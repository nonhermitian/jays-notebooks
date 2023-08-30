# This code is part of Qiskit.
#
# (C) Copyright IBM 2019, 2023.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Translator between an Ising Hamiltonian and a quadratic program"""

import math
from typing import Optional, Tuple, Union
from warnings import warn

import numpy as np
from qiskit.opflow import PauliSumOp
from qiskit.quantum_info import Pauli, SparsePauliOp

from optimization.exceptions import QiskitOptimizationError
from optimization.problems.quadratic_program import QuadraticProgram


def to_ising(
    quad_prog: QuadraticProgram, opflow: Optional[bool] = None
) -> Tuple[Union[PauliSumOp, SparsePauliOp], float]:
    """Return the Ising Hamiltonian of this problem.

    Variables are mapped to qubits in the same order, i.e.,
    i-th variable is mapped to i-th qubit.
    See https://github.com/Qiskit/qiskit-terra/issues/1148 for details.

    .. note::

        The default value of ``opflow`` argument is currently set ``True``, but it will
        first be changed to ``False`` and then deprecated in future releases.

    Args:
        quad_prog: The problem to be translated.
        opflow: The output object is a ``PauliSumOp`` operator if True.
            Otherwise, it is ``SparsePauliOp``. (default: True)

    Returns:
        A tuple (qubit_op, offset) comprising the qubit operator for the problem
        and offset for the constant value in the Ising Hamiltonian.

    Raises:
        QiskitOptimizationError: If an integer variable or a continuous variable exists
            in the problem.
        QiskitOptimizationError: If constraints exist in the problem.
    """
    if opflow is None:
        opflow = True
        warn(
            "`opflow` argument of `to_ising` is not set explicitly. "
            "It is currently set True, but the default value will be changed to False. "
            "We suggest using `SparsePauliOp` instead of Opflow operators.",
            stacklevel=2,
        )

    # if problem has variables that are not binary, raise an error
    if quad_prog.get_num_vars() > quad_prog.get_num_binary_vars():
        raise QiskitOptimizationError(
            "The type of all variables must be binary. "
            "You can use `QuadraticProgramToQubo` converter "
            "to convert integer variables to binary variables. "
            "If the problem contains continuous variables, `to_ising` cannot handle it. "
            "You might be able to solve it with `ADMMOptimizer`."
        )

    # if constraints exist, raise an error
    if quad_prog.linear_constraints or quad_prog.quadratic_constraints:
        raise QiskitOptimizationError(
            "There must be no constraint in the problem. "
            "You can use `QuadraticProgramToQubo` converter "
            "to convert constraints to penalty terms of the objective function."
        )

    # initialize Hamiltonian.
    num_vars = quad_prog.get_num_vars()
    pauli_list = []
    offset = 0.0
    zero = np.zeros(num_vars, dtype=bool)

    # set a sign corresponding to a maximized or minimized problem.
    # sign == 1 is for minimized problem. sign == -1 is for maximized problem.
    sense = quad_prog.objective.sense.value

    # convert a constant part of the objective function into Hamiltonian.
    offset += quad_prog.objective.constant * sense

    # convert linear parts of the objective function into Hamiltonian.
    for idx, coef in quad_prog.objective.linear.to_dict().items():
        z_p = zero.copy()
        weight = coef * sense / 2
        z_p[idx] = True

        pauli_list.append(SparsePauliOp(Pauli((z_p, zero)), -weight))
        offset += weight

    # create Pauli terms
    for (i, j), coeff in quad_prog.objective.quadratic.to_dict().items():
        weight = coeff * sense / 4

        if i == j:
            offset += weight
        else:
            z_p = zero.copy()
            z_p[i] = True
            z_p[j] = True
            pauli_list.append(SparsePauliOp(Pauli((z_p, zero)), weight))

        z_p = zero.copy()
        z_p[i] = True
        pauli_list.append(SparsePauliOp(Pauli((z_p, zero)), -weight))

        z_p = zero.copy()
        z_p[j] = True
        pauli_list.append(SparsePauliOp(Pauli((z_p, zero)), -weight))

        offset += weight

    if pauli_list:
        # Remove paulis whose coefficients are zeros.
        qubit_op = sum(pauli_list).simplify(atol=0)
    else:
        # If there is no variable, we set num_nodes=1 so that qubit_op should be an operator.
        # If num_nodes=0, I^0 = 1 (int).
        num_vars = max(1, num_vars)
        qubit_op = SparsePauliOp("I" * num_vars, 0)

    if opflow:
        qubit_op = PauliSumOp(qubit_op)

    return qubit_op, offset
