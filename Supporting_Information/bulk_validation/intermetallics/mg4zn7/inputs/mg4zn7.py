from ase.io import read, write
from ase.build import make_supercell

# ---- change this per structure ----
cif_file = "Mg4Zn7.cif"           data_out = "mg4zn7.data"           

atoms = read(cif_file)

print("Number of atoms:", len(atoms))
write(data_out, atoms, format='lammps-data')
print("Wrote", data_out)
