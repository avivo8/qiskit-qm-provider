"""
Example: Adding Qiskit Pulse calibrations to a circuit and running on the backend.

This example attaches a custom pulse-level calibration to a gate using
qc.add_calibration(). When the circuit is run (or transpiled) with the backend,
the backend picks up these calibrations and translates them to QUA.

Requires Qiskit 1.x for full Qiskit Pulse support (DriveChannel, Schedule, etc.).
"""

# %%
from qiskit.circuit import QuantumCircuit
from qiskit import transpile
from qiskit_qm_provider import IQCCProvider, dump_qua_script




backend = IQCCProvider().get_backend("arbel")

# Assume backend is obtained from a provider and supports Pulse (e.g. FluxTunableTransmonBackend)
physical_qubit = (0,)  # Specify qubit in Qiskit through indices.
qubit = backend.get_qubit(physical_qubit[0])


#%%
    # Build a circuit that uses a gate we will calibrate

def create_circuit():
    qc = QuantumCircuit(2, 1)
    qc.h(0)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure_all()
    return qc
#%%
# Duration can be fetched from target directly for PulseMacros
qc = create_circuit()
transpiled = transpile(qc, backend)

qc.draw("mpl")  # without all the qubits just 2 and 3
#%%

# Get the actual running QUA program and dump it to a Python script file
debug_path = dump_qua_script(backend, transpiled, path="debug_entanglement_qua.py")
print(f"\nReal running QUA code written to: {debug_path}")
# %%

# Transpile and run; the backend will update its calibration mapping from the circuit
job = backend.run(transpiled, shots=1024)
result = job.result()
print(result)

# %%
