# Quantum Application Demos

In this folder, we provide a set of example programs that can be used to explore applications on a quantum computer. The goal is to highlight the primitive functions and to show the power of Qiskit and quantum computers. I strongly believe that all quantum applications can be written as four steps with only step 3 using the quantum computer. Even complicated examples will just iterate over these steps four steps and why we have the concept of functions (using quantum serverless tools) so that in the future these notebooks could be hosted.

The four steps are:

1. Map the problem to a Quantum Native format (Set of Operators, and a set of Quantum Circuits)
2. Optimize the circuits and operators to run on quantum hardware
3. Execute using a quantum primitive function (estimator or sampler)
4. Post-processing of the results to return either a plot or the answer

## Examples

### First Programs

- [Mermin](Mermin.ipynb)-- showing how to run a list of quantum circuits and demonstrate entanglement.
- [Golden Ratio Optimization](GoldenRatio.ipynb) -- Showing how we can use the Golden Ratio method to optimize the phase to minimize the Mermin Operator.
- VQE -- A general method showing how to use VQE inside a minimized loop.

### Optimization

- Basic Quadratic Program Workflow -- A basic 3-variable workflow with no constraints
- Knapsack Workflow -- 
- MaxCut Workflow.

### Chemistry

### Machine Learning
