from ase.io import read, write
from ase.build import make_supercell

cif_file = "Mg2Zn11.cif"            
data_out = "mg2zn11.data"           

atoms = read(cif_file)

print("Number of atoms:", len(atoms))
write(data_out, atoms, format='lammps-data')
print("Wrote", data_out)
