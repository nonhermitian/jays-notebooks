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

"""Fulqrum
"""
import inspect
import types
from typing import Union, get_origin, get_args

import rustworkx as rx
from rustworkx.visualization import mpl_draw


class Workflow:
    def __init__(self, operations=[], 
                 workflow_id=None,
                 ):
        self.metadata = {}
        self.data = {}
        self.workflow_id = workflow_id
        self.dag = rx.PyDiGraph()
        # Make life easy and provide a way to input serial list of passes at init
        if not isinstance(operations, list):
            operations = [operations]
        if any(operations):
            oper = operations[0]
            node_id = self.dag.add_node(oper)
            oper._node_id = node_id
            oper._dag = self.dag
        
            for idx, oper in enumerate(operations[1:]):
                node_id = self.dag.add_child(idx, oper, None)
                oper._node_id = node_id
                oper._dag = self.dag

    def __getitem__(self, integer):
        return self.dag[integer]

    def run(self, **kwargs):
        for node in rx.topological_sort(self.dag):
            # Find parent nodes to this one
            parents = self.dag.predecessor_indices(node)
            current_args = inspect.signature(self.dag[node].run).parameters.keys()
            # Merge dicts of outputs into one big kwarg dict to pass
            input_dict = {}
            if not parents:
                input_dict = kwargs
            for parent in parents:
                input_dict = input_dict | self.data[parent]
            # Remove any items not in the signature of the current node
            temp_dict = input_dict.copy()
            for key in input_dict:
                if key not in current_args:
                    del temp_dict[key]
            input_dict = temp_dict
            # Execute node with parents dict
            outputs = self.dag[node].run(**input_dict)
            # If there are any outputs
            if outputs:
                    out_dict = {}
                    output_keys = list(self.dag[node].output_vars.keys())
                    # if multiple returns then they tuple
                    if isinstance(outputs, tuple):
                        for idx, item in enumerate(outputs):
                            out_dict[output_keys[idx]] = item
                    else:
                        out_dict[output_keys[0]] = outputs
                    self.data[node]  = out_dict

        if self.dag.num_nodes():
            if len(self.data[node]):
                return list(self.data[node].values())[0]
            else:
                return tuple(self.dag.data[node].values())

    def draw(self):
        return mpl_draw(self.dag,
                        with_labels=True,
                        node_color='orange',
                        labels=lambda node: node.__class__.__name__, font_size=10)

    def validate(self):
        valid = True
        for node in rx.topological_sort(self.dag):
            # Find parent nodes to this one
            parents = self.dag.predecessor_indices(node)
             # Get current args
            current_annotations = inspect.get_annotations(self.dag[node].run)
            input_types_dict = {}
            for parent in parents:
                input_types_dict = input_types_dict | self.dag[parent].output_vars

            for key, kind in input_types_dict.items():
                key_types = get_args(current_annotations[key])
                if any(key_types): 
                    if type not in get_args(current_annotations[key]):
                        valid = False
                else:
                    if not isinstance(kind, str):
                        if kind != current_annotations[key]:
                            valid = False
                    else:
                        if kind.__name__ != current_annotations[key]:
                            print('crap')
                            valid = False
                if not valid:
                    raise TypeError(f"Input type {kind} is not valid for '{key}':{current_annotations[key]} at node {node} : {self.dag[node].__name__}")
        return True
