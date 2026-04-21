#%%
import cirq 
from itertools import combinations
import numpy as np 
 
  
def logical_rz(qubits: list[cirq.Qid], t: float, m0: int, m1: int) -> cirq.Circuit: 
    """Create a circuit that applies a Z rotation e^{-i Z t / 2} to a 
    logical qubit encoded in a thermodynamic code. 
  
    Args: 
        qubits: The physical qubits that encode the logical qubit. 
        t: The rotation angle in radians. 
  
    Returns: 
        A Cirq circuit that applies a Z rotation to the logical qubit. 
    """ 
    physical_theta = -t / (m1 - m0)

    # global phase
    phi0 = (physical_theta / 2) * (2 * m0 - n)
    
    circuit = cirq.Circuit()
    for q in qubits: 
        circuit.append(cirq.rz(physical_theta).on(q))
        
    # apply global phase
    circuit.append(cirq.GlobalPhaseGate(np.exp(-1j * phi0)))
    return circuit 
 
 
def logical_Z(qubits: list[cirq.Qid]) -> cirq.Circuit: 
    """Create a circuit that applies a Z operation to a logical qubit 
    encoded in a thermodynamic code. 
  
    Args: 
        qubits: The physical qubits that encode the logical qubit. 
        t: The rotation angle in radians. 
     
    Returns: 
        A Cirq circuit with a Z operation applied to the logical qubit. 
    """ 
    return logical_rz(qubits, np.pi, m0, m1)


def fixed_wgt_state(n: int, w:int) -> np.ndarray:
    dim = 2**n
    state = np.zeros(dim, dtype=complex)
    
    basis_indices = []
    for ones in combinations(range(n), w):
        bits = [0] * n
        for j in ones:
            bits[j] = 1
        idx = int("".join(map(str, bits)), 2)
        basis_indices.append(idx)
        
    amp = 1 / np.sqrt(len(basis_indices))
    for idx in basis_indices:
        state[idx] = amp
    return state

#%%
# thermodynamic code parameters
n  = 4
m0 = 1
m1 = 3

# construct logical states |0>_L and |1>_L
zero_L = fixed_wgt_state(n, m0)
one_L  = fixed_wgt_state(n, m1)
logical_states = {
    0: {"vector": zero_L, "m": m0},
    1: {"vector": one_L,  "m": m1}    
}

# simulating S-gate

#set initial state
logical = 0
psi_L = logical_states[logical]["vector"]

# S-gate parameters
delta_phi = np.pi / 2

m_ref = logical_states[logical]["m"]
theta_s = delta_phi / (m1 - m0)
global_phase = (-theta_s / 2) * (2 * m0 - n)

# simulation
qubits = cirq.LineQubit.range(n)
sim = cirq.Simulator()

circuit = logical_rz(qubits, delta_phi, m0, m1)
result = sim.simulate(circuit, qubit_order = qubits, initial_state=psi_L)
final_state = result.final_state_vector 

#%%
print("\n Initial state vector:")
print(psi_L)
print("\nFinal state vector:")
print(final_state)
# %%

# Z-gate parameters
theta_z = np.pi / (m1 - m0)
global_phase = (-theta_z / 2) * (2 * m0 - n)
circuit = logical_Z(qubits)
result = sim.simulate(circuit, qubit_order = qubits, initial_state=psi_L)
final_state = result.final_state_vector * np.exp(-1j * global_phase)

print("\n Initial state vector:")
print(psi_L)
print("\nFinal state vector:")
print(final_state)
# %%
