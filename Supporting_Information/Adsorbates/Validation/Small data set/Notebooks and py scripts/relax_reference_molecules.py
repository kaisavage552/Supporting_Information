from ase import Atoms
from ase.optimize import BFGS
from mace.calculators import mace_mp
import json
from pathlib import Path

# Load MACE calculator
calc = mace_mp(
    model='mace-mh-1.model',
    default_dtype='float64',
    device='cpu',
    head='omat_pbe'
)

results = {}

print("1. O₂ molecule - bond length optimisation")
# Create O2 at experimental bond length
o2 = Atoms('O2', positions=[[0, 0, 0], [0, 0, 1.21]])
o2.center(vacuum=10.0)  # 10 Å vacuum on all sides
o2.calc = calc

print(f"\nInitial geometry:")
print(f"  Bond length: 1.21 Å (experimental)")
print(f"  Box size: {o2.get_cell().diagonal()}")

# Get initial energy
E_o2_initial = o2.get_potential_energy()
print(f"  Initial energy: {E_o2_initial:.6f} eV")

# Relax the molecule
print(f"Optimizing geometry")
opt_o2 = BFGS(o2, trajectory='o2_relax.traj', logfile='o2_relax.log')
opt_o2.run(fmax=0.01, steps=100)

# Final optimized state
E_o2_final = o2.get_potential_energy()
d_o2_final = o2.get_distance(0, 1)
E_o2_per_atom = E_o2_final / 2
forces = o2.get_forces()
max_force = max([abs(f).max() for f in forces])

print(f"Optimisation complete:")
print(f"  Final bond length: {d_o2_final:.4f} Å")
print(f"  Bond length change: {d_o2_final - 1.21:+.4f} Å")
print(f"  Final energy: {E_o2_final:.6f} eV")
print(f"  Energy change: {E_o2_final - E_o2_initial:+.6f} eV")
print(f"  Max force: {max_force:.6f} eV/Å")
print(f"  Optimization steps: {opt_o2.get_number_of_steps()}")

# Calculate bond energy
cohesive_o2 = abs(E_o2_final)  # Energy to dissociate O2 -> 2O at infinity
print(f"Cohesive energy: {cohesive_o2:.3f} eV")
print(f"  Experimental O2 bond: 5.12 eV")
print(f"  MACE overbinding: {(cohesive_o2/5.12 - 1)*100:+.1f}%")

results['O2'] = {
    'E_initial': E_o2_initial,
    'E_final': E_o2_final,
    'E_total': E_o2_final,
    'E_per_atom': E_o2_per_atom,
    'bond_length_initial': 1.21,
    'bond_length_final': d_o2_final,
    'bond_length_change': d_o2_final - 1.21,
    'energy_change': E_o2_final - E_o2_initial,
    'max_force': max_force,
    'opt_steps': opt_o2.get_number_of_steps(),
    'cohesive_energy': cohesive_o2,
    'experimental_bond_energy': 5.12
}
print("2. H₂ molecule - bond length optimisation")
# Create H2 at experimental bond length
h2 = Atoms('H2', positions=[[0, 0, 0], [0, 0, 0.74]])
h2.center(vacuum=10.0)  # 10 Å vacuum on all sides
h2.calc = calc

print(f"Initial geometry:")
print(f"  Bond length: 0.74 Å (experimental)")
print(f"  Box size: {h2.get_cell().diagonal()}")

# Get initial energy
E_h2_initial = h2.get_potential_energy()
print(f"  Initial energy: {E_h2_initial:.6f} eV")

# Relax the molecule
print(f"Optimising geometry (fmax = 0.01 eV/Å)")
opt_h2 = BFGS(h2, trajectory='h2_relax.traj', logfile='h2_relax.log')
opt_h2.run(fmax=0.01, steps=100)

# Final optimised state
E_h2_final = h2.get_potential_energy()
d_h2_final = h2.get_distance(0, 1)
E_h2_per_atom = E_h2_final / 2
forces = h2.get_forces()
max_force = max([abs(f).max() for f in forces])

print(f"  Optimisation complete:")
print(f"  Final bond length: {d_h2_final:.4f} Å")
print(f"  Bond length change: {d_h2_final - 0.74:+.4f} Å")
print(f"  Final energy: {E_h2_final:.6f} eV")
print(f"  Energy change: {E_h2_final - E_h2_initial:+.6f} eV")
print(f"  Max force: {max_force:.6f} eV/Å")
print(f"  Optimization steps: {opt_h2.get_number_of_steps()}")

# Calculate bond energy
cohesive_h2 = abs(E_h2_final)
print(f"  Cohesive energy: {cohesive_h2:.3f} eV")
print(f"  Experimental H2 bond: 4.52 eV")
print(f"  MACE overbinding: {(cohesive_h2/4.52 - 1)*100:+.1f}%")

results['H2'] = {
    'E_initial': E_h2_initial,
    'E_final': E_h2_final,
    'E_total': E_h2_final,
    'E_per_atom': E_h2_per_atom,
    'bond_length_initial': 0.74,
    'bond_length_final': d_h2_final,
    'bond_length_change': d_h2_final - 0.74,
    'energy_change': E_h2_final - E_h2_initial,
    'max_force': max_force,
    'opt_steps': opt_h2.get_number_of_steps(),
    'cohesive_energy': cohesive_h2,
    'experimental_bond_energy': 4.52
}

output_file = Path('mace_simple_validation_results/molecular_references.json')
output_file.parent.mkdir(exist_ok=True)

with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

