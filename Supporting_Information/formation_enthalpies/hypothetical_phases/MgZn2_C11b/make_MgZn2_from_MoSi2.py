from ase.io import read, write

# Read MoSi2 C11b CIF
atoms = read(cif_file)
print("Original structure:")
print("  Formula:", atoms.get_chemical_formula())
print("  Number of atoms:", len(atoms))
print("  Cell (Å):\n", atoms.get_cell())

# Swap elements to get MgZn2 (Mg:Zn = 1:2)
#    Mo (1 per f.u.) -> Mg
#    Si (2 per f.u.) -> Zn
for atom in atoms:
    if atom.symbol == "Mo":
        atom.symbol = "Mg"
    elif atom.symbol == "Si":
        atom.symbol = "Zn"

print("\nAfter substitution (target = MgZn2 C11b):")
print("  Formula:", atoms.get_chemical_formula())
print("  Unique species:", sorted(set(a.symbol for a in atoms)))


if abs(scale_factor - 1.0) > 1e-8:
    cell = atoms.get_cell()
    new_cell = cell * scale_factor
    atoms.set_cell(new_cell, scale_atoms=True)
    print(f"\nApplied isotropic scaling with factor {scale_factor:.3f}")
    print("  New cell (Å):\n", atoms.get_cell())

# Write a CIF with MgZn2
write(output_cif, atoms)
print(f"\nWrote substituted CIF: {output_cif}")

# 5) Write LAMMPS data file
write(
    output_data,
    atoms,
    format="lammps-data",
    atom_style="atomic"
)
print(f"Wrote LAMMPS data file: {output_data}")
