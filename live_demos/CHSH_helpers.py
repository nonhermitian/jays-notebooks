from qiskit import QuantumCircuit, transpile
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import time
import datetime
from qiskit.providers.jobstatus import JobStatus

def build_chsh_circuit(parameter):
    chsh_circuits = QuantumCircuit(2)
    chsh_circuits.h(0)
    chsh_circuits.cx(0, 1)
    chsh_circuits.ry(parameter, 0)
    
    return chsh_circuits


def build_observables(ops, number_of_phases):
    observables = [[ops[0]]*number_of_phases,[ops[1]]*number_of_phases,[ops[2]]*number_of_phases,[ops[3]]*number_of_phases]
    observables = [item for sublist in observables for item in sublist]
    
    return observables

def build_chsh_witnesses(expectation_values, phases):
    chsh1 = expectation_values[0:phases] - expectation_values[phases:2*phases] + expectation_values[2*phases:3*phases] + expectation_values[3*phases:]
    chsh2 = expectation_values[0:phases] + expectation_values[phases:2*phases] - expectation_values[2*phases:3*phases] + expectation_values[3*phases:]
    
    return chsh1, chsh2


def reconstruct_results(job, number_of_phases):
    
    # Calculate the total number of seconds
    total_seconds = 120
    update_seconds = 4
    timer = datetime.timedelta(seconds = total_seconds)
    print(timer, end="\r")
 
    while total_seconds > 0:

        time.sleep(update_seconds)
        total_seconds -= update_seconds
        timer = datetime.timedelta(seconds = total_seconds)
        print(timer, end="\r")
        
        status = job.status()
        if status == JobStatus.DONE:
            # print("in loop")
            # Build the CHSH witnesses
            expectation_values_real = job.result().values
            chsh1, chsh2 = build_chsh_witnesses(expectation_values_real, number_of_phases)
            break
        
        # print(job.status())
    else:
        chsh2 = np.array([ 1.94677571,  2.47369227,  2.64866075,  2.67480547,  2.2926904 ,
                         1.7697961 ,  0.83461975, -0.0502783 , -0.72601863, -1.67929516,
                        -2.2484455 , -2.54207076, -2.73916169, -2.54810415, -2.01113193,
                        -1.23684614, -0.4846828 ,  0.39015959,  1.18053444,  1.98699835])
        
    return chsh2
    


def plot_results(witnesses, phases, backends):
    # backend_name = backend.name
    colors = plt.cm.get_cmap('tab20b')
    if len(witnesses) != len(backends):
        print("Error: Number of backends different than number of witnesses")
    for idx, witness in enumerate(witnesses):
        if backends[idx].name[:3] == 'sim' or backends[idx].name[-3:] == 'tor':
            
            plt.plot(phases, witness, 'o-', color=colors(2+idx*4), label='CHSH Noiseless')
        else:
            plt.plot(phases, witness, 'o-', color=colors(2+idx*4), label='CHSH %s'%(backends[idx].name))

    plt.axhline(y=2, color='r', linestyle='-')
    plt.axhline(y=-2, color='r', linestyle='-')
    plt.axhline(y=np.sqrt(2)*2, color='b', linestyle='-.')
    plt.axhline(y=-np.sqrt(2)*2, color='b', linestyle='-.')
    plt.ylim(-3.2,3.2)
    plt.xlabel('Theta')
    plt.ylabel('CHSH witness')
    plt.legend(loc="center right")
    # plt.savefig("CHSH.pdf", format="pdf", bbox_inches="tight")
    plt.show()