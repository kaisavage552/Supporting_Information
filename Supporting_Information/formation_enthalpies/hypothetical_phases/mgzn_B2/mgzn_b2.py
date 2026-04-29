from ase import Atoms
from ase.build import bulk, make_supercell
from ase.io import write
import numpy as np

# Lattice parameter guess for B2 MgZn (Å)
a_b2 = 3.3  

# Simple cubic cell
cell_b2 = np.array([[a_b2, 0.0,  0.0],
                    [0.0,  a_b2, 0.0],
                    [0.0,  0.0,  a_b2]])

# Fractional positions for CsCl-type
positions_frac_b2 = [
    (0.0, 0.0, 0.0),       # Mg
    (0.5, 0.5, 0.5)        # Zn
]

symbols_b2 = ["Mg", "Zn"]

# Convert fractional to Cartesian
positions_cart_b2 = np.dot(positions_frac_b2, cell_b2)

mgzn_b2_prim = Atoms(symbols=symbols_b2,
                     positions=positions_cart_b2,
                     cell=cell_b2,
                     pbc=True)

# Make a 2x2x2 supercell
P = np.diag([2, 2, 2])
mgzn_b2_super = make_supercell(mgzn_b2_prim, P)

# Write LAMMPS data file
write("MgZn_B2_2x2x2.data", mgzn_b2_super, format="lammps-data",
      atom_style="atomic")

print("Written MgZn_B2_2x2x2.data")


# ============================================================
# 2. Pure hcp Zn → reference for 0 K relaxation
#    Use approximate experimental lattice constants; MEAM will relax
# ============================================================

# hcp Zn approximate parameters (Å)
a_hcp_zn = 2.66
c_hcp_zn = 4.95

zn_hcp_prim = bulk("Zn", crystalstructure="hcp", a=a_hcp_zn, c=c_hcp_zn)

# Make a 3x3x2 supercell (you can change this if you want)
zn_P = np.diag([3, 3, 2])
zn_hcp_super = make_supercell(zn_hcp_prim, zn_P)

write("Zn_hcp_3x3x2.data", zn_hcp_super, format="lammps-data",
      atom_style="atomic")

print("Written Zn_hcp_3x3x2.data")
