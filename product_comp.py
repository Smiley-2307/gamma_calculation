import cantera as ct
import numpy as np

# Edit these parameters to change the initial temperature, the pressure, and
# the phases in the mixture.

T = 527.69
P = 538657.7 

# phases
gas = ct.Solution('JP10.yaml')
carbon = ct.Solution('graphite.yaml')

# the phases that will be included in the calculation, and their initial moles
mix_phases = [(gas, 1.0), (carbon, 0.0)]

# gaseous fuel species
fuel_species = 'C10H16'

# equivalence ratio range
phi = np.arange(0.3,2.5,0.1)
npoints = len(phi)

mix = ct.Mixture(mix_phases)

# create some arrays to hold the data
tad = np.zeros(npoints)
xeq = np.zeros((mix.n_species, npoints))

for i in range(npoints):
    # set the gas state
    gas.set_equivalence_ratio(phi[i], fuel_species, 'O2:1.0, N2:3.76')

    # create a mixture of 1 mole of gas, and 0 moles of solid carbon.
    mix = ct.Mixture(mix_phases)
    mix.T = T
    mix.P = P

    # equilibrate the mixture adiabatically at constant P
    mix.equilibrate('HP', solver='gibbs', max_steps=1000)

    tad[i] = mix.T
    print('At phi = {0:12.4g}, Tad = {1:12.4g}'.format(phi[i], tad[i]))
    print('\n')
    #store the values of molefraction of products
    xeq[:, i] = mix.species_moles

print('temp of gas ', gas.T)

#set the state of gas to desired temp and pressure 
gas.TP = 1283.15,517111.4

#print out the value of gamma of gas
print('Gamma = ',gas.cp/gas.cv)

#at phi = 0.9 we get Tad as 2368





