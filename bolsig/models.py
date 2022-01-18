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
# hbar = h / 2pi
hbar = 6.62607004e-34 / 2.0 / np.pi   # m2 kg / s
# static polarizability
alpha = 11.08     # a0^3
# E (eV) from k^2 (a0^(-2))
Efromk2 = hbar * hbar / 2.0 / me / qe / a0 / a0 

# Excitation energy levels in eV, from NIST
E_ext = [11.54835442, 11.62359272, 11.72316039, 11.82807116]

# Ionization energy levels in eV, from NIST
E_ion = [15.7596119, 27.62967]

# All take theta as model parameters, E as electron energy in eV.
def Excite_metastable(n,theta,E):
    # n: excited energy level, starting from 1,2,...
    b, gamma = theta
    return 4. * np.pi * a0 * a0 * R0 / E * b * ( 1.0 - E_ext[n-1]/E ) * ( (2. * E)**(-gamma) )

def Excite_resonance(n,theta,E):
    # n: excited energy level, starting from 1,2,...
    F0, beta, C1, alpha0 = theta
    # from eV to (m/s)^2
    v2 = qe * E * 2.0 / me
    beta2 = v2 / c0 / c0
    # relativistic factor
    rel_factor = np.log(beta2 / (1.0 - beta2) * mc2 / 2.0 / E_ext[n-1] * C1 ) - beta2
    return 4. * np.pi * a0 * a0 * R0 / E * F0 / E_ext[n-1] * rel_factor * ( 1.0 - (E_ext[n-1]/E) ** alpha0 ) ** beta

def total_Ion_BED(theta,E):
    a, b, c = theta
    t = E / E_ion[0]
    return 4. * np.pi * a0 * a0 / t * ( a * np.log(t) + b * (1. - 1. / t) + c * np.log(t) / (t + 1.) )

def elastic_MERT(theta,E,N=10):
    NE = len(E)
    k = np.sqrt( E / Efromk2 ) # wavenumber in a0^(-1)
    crs = np.zeros((NE,))

    A, D, F, E1 = theta
    eta0 = - A * ( 1. + 4. / 3. * alpha * k * k * np.log(k) ) - np.pi / 3. * alpha * k + D * k**2 + F * k**3
    eta0 = np.arctan(eta0 * k)
    
    eta1 = np.pi / 15. * alpha * k * ( 1. - np.sqrt(E/E1) )
    eta1 = np.arctan(eta1 * k)
    
    crs += np.sin(eta0 - eta1)**2
    
    for L in range(1,N):
        eta0 = np.copy(eta1)
        L1 = L+1
        eta1 = np.pi * alpha * k / (2.*L1 + 3.) / (2.*L1 + 1.) / (2.*L1 - 1.)
        eta1 = np.arctan(eta1 * k)
        
        crs += (L + 1.) * np.sin(eta0 - eta1)**2
    
    return crs * 4. * np.pi / k / k * a0 * a0

def elastic_modified_MERT(theta,E,N=10):
    NE = len(E)
    k = np.sqrt( E / Efromk2 ) # wavenumber in a0^(-1)
    crs = np.zeros((NE,))

    A, D, F, E1, E2, E3 = theta
    eta0 = - A * ( 1. + 4. / 3. * alpha * k * k * np.log(k) ) - np.pi / 3. * alpha * k + D * k**2 + F * k**3
    eta0 = np.arctan(eta0 * k)
    
    # one more parameter added on eta1.
    eta1 = np.pi / 15. * alpha * k * ( 1. - np.sqrt(E)/E1 + E/E2 )
    eta1 = np.arctan(eta1 * k)
    
    crs += np.sin(eta0 - eta1)**2
    
    for L in range(1,N):
        eta0 = np.copy(eta1)
        L1 = L+1
        eta1 = np.pi * alpha * k / (2.*L1 + 3.) / (2.*L1 + 1.) / (2.*L1 - 1.)
        if (L==1):
            eta1 *= (1.0 + E/E3)
        eta1 = np.arctan(eta1 * k)
        
        crs += (L + 1.) * np.sin(eta0 - eta1)**2
    
    return crs * 4. * np.pi / k / k * a0 * a0

def elastic_empirical_MERT(theta,E,N=10):
    A, D, F, E1, Ec, tc = theta
    
    NE = len(E)
    Et = np.copy(E)
    Et *= 1.0 - 0.5 * (Et/Ec)**(2/tc) / (1.0 + (Et/Ec)**(2/tc))
    k = np.sqrt( Et / Efromk2 ) # wavenumber in a0^(-1)
    crs = np.zeros((NE,))

    eta0 = - A * ( 1. + 4. / 3. * alpha * k * k * np.log(k) ) - np.pi / 3. * alpha * k + D * k**2 + F * k**3
    eta0 = np.arctan(eta0 * k)
    
    # one more parameter added on eta1.
    eta1 = np.pi / 15. * alpha * k * ( 1. - np.sqrt(Et/E1) )
    eta1 = np.arctan(eta1 * k)
    
    crs += np.sin(eta0 - eta1)**2
    
    for L in range(1,N):
        eta0 = np.copy(eta1)
        L1 = L+1
        eta1 = np.pi * alpha * k / (2.*L1 + 3.) / (2.*L1 + 1.) / (2.*L1 - 1.)
        eta1 = np.arctan(eta1 * k)
        
        crs += (L + 1.) * np.sin(eta0 - eta1)**2
    
    return crs * 4. * np.pi / k / k * a0 * a0
    