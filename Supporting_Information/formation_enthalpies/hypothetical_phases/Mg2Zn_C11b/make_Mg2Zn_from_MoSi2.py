from ase.io import read, write
from ase.geometry import cellpar_to_cell

# Read MoSi2 C11b CIF
atoms = read(cif_file)
print("Original structure:")
print("  Formula:", atoms.get_chemical_formula())
print("  Number of atoms:", len(atoms))
print("  Cell (Å):\n", atoms.get_cell())

# Swap elements to get Mg2Zn
# C11b prototype: A(2a) = Mo, B(4e) = Si.
# want Mg2Zn: put Zn on A (2a) and Mg on B (4e).
for atom in atoms:
    if atom.symbol == "Mo":
        atom.symbol = "Zn"
    elif atom.symbol == "Si":
        atom.symbol = "Mg"

print("\nAfter substitution (target = Mg2Zn C11b):")
print("  Formula:", atoms.get_chemical_formula())
print("  Unique species:", sorted(set(a.symbol for a in atoms)))

# Optional: isotropic lattice scaling
if abs(scale_factor - 1.0) > 1e-8:
    cell = atoms.get_cell()
    new_cell = cell * scale_factor
    atoms.set_cell(new_cell, scale_atoms=True)
    print(f"\nApplied isotropic scaling with factor {scale_factor:.3f}")
    print("  New cell (Å):\n", atoms.get_cell())

# Write a CIF with Mg2Zn
write(output_cif, atoms)
print(f"\nWrote substituted CIF: {output_cif}")

# Write LAMMPS data file
#    atom_style 'atomic' is fine for most metallic potentials (EAM/MEAM etc.)
write(
    output_data,
    atoms,
    format="lammps-data",
    atom_style="atomic"
)
print(f"Wrote LAMMPS data file: {output_data}")
