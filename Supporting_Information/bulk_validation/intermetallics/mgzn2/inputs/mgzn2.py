from ase.io import read, write
from ase.build import make_supercell


cif_file = "MgZn2.cif"           
data_out = "mgzn2.data"           

# Read the CIF
atoms = read(cif_file)

print("Number of atoms:", len(atoms))
write(data_out, atoms, format='lammps-data')
print("Wrote", data_out)
