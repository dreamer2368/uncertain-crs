import numpy as np

# Rydberg energy
R0 = 13.605693122994  # eV
# Bohr radius
a0 = 5.29177e-11     # m
# electron charge
qe = 1.60217662e-19  # C
# electron mass
me = 9.10938356e-31  # kg
# speed of light
c0 = 2.99792458e8    # m/s
# mc2 in eV
mc2 = me * c0 * c0 / qe

# Excitation energy levels in eV, from NIST
E_ext = [11.54835442, 11.62359272, 11.72316039, 11.82807116]

# All take theta as model parameters, E as electron energy in eV.
def Excite_metastable(n,theta,E):
    # n: excited energy level, starting from 1,2,...
    b, gamma = theta
    return 4. * np.pi * a0 * a0 * R0 / E * b * ( 1.0 - E_ext[n-1]/E ) * ( (2. * E)**(-gamma) )

def Excite_resonance(n,theta,E):
    # n: excited energy level, starting from 1,2,...
    F0, beta = theta
    # from eV to (m/s)^2
    v2 = qe * E * 2.0 / me
    beta2 = v2 / c0 / c0
    # relativistic factor
    rel_factor = np.log(beta2 / (1.0 - beta2) * mc2 / 2.0 / E_ext[n-1]) - beta2
    return 4. * np.pi * a0 * a0 * R0 / E * F0 / E_ext[n-1] * rel_factor * ( 1.0 - (E_ext[n-1]/E) ) ** beta