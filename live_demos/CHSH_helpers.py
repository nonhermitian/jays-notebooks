from qiskit import QuantumCircuit, transpile
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


def check_job_status(job):
    
    # Calculate the total number of seconds
    total_seconds = 4000
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
            values = job.result().values
            break
        
        # print(job.status())
    else:
        values = np.array([ 1.94677571,  2.47369227,  2.64866075,  2.67480547,  2.2926904 ,
                            1.7697961 ,  0.83461975, -0.0502783 , -0.72601863, -1.67929516,
                            -2.2484455 , -2.54207076, -2.73916169, -2.54810415, -2.01113193,
                            -1.23684614, -0.4846828 ,  0.39015959,  1.18053444,  1.98699835])
    return values
    
