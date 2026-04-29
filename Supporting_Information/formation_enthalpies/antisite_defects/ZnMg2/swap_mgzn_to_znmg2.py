import argparse
from collections import Counter
from typing import Optional

from ase.io import read, write
from ase import Atoms


COMMON_STYLES = ["full", "atomic", "charge", "molecular"]


def try_read_lammps_data(path: str, style: Optional[str] = None) -> tuple[Atoms, str]:
       if style:
        atoms = read(path, format="lammps-data", style=style)
        return atoms, style

    last_err = None
    for st in COMMON_STYLES:
        try:
            atoms = read(path, format="lammps-data", style=st)
            return atoms, st
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(
        "Failed to read LAMMPS data with common styles "
        f"{COMMON_STYLES}. Last error: {last_err}"
    )


def swap_species(atoms: Atoms, mapping: dict[str, str]) -> Atoms:
    
    new = atoms.copy()
    symbols = new.get_chemical_symbols()
    new.set_chemical_symbols([mapping.get(s, s) for s in symbols])
    return new


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Input LAMMPS data file (MgZn2).")
    ap.add_argument("-o", "--output", required=True, help="Output LAMMPS data file (ZnMg2).")
    ap.add_argument("--style", choices=COMMON_STYLES, default=None,
                   help="LAMMPS atom style of the input data. If omitted, auto-detect.")
    args = ap.parse_args()

    atoms, style_used = try_read_lammps_data(args.input, style=args.style)

    
    comp_before = Counter(atoms.get_chemical_symbols())


    mapping = {"Mg": "Zn", "Zn": "Mg"}
    swapped = swap_species(atoms, mapping)
    comp_after = Counter(swapped.get_chemical_symbols())

    
    assert sum(comp_before.values()) == sum(comp_after.values()), "Atom count changed unexpectedly!"


    assert (swapped.cell.array == atoms.cell.array).all()
    assert (swapped.pbc == atoms.pbc).all()

    write(args.output, swapped, format="lammps-data", atom_style=style_used)

    def fmt_comp(c):
        return ", ".join(f"{k}:{v}" for k, v in sorted(c.items()))

    print("=== ZnMg2 Swap Summary ===")
    print(f"Input file:   {args.input}")
    print(f"Output file:  {args.output}")
    print(f"Atom style:   {style_used}")
    print(f"Composition before: {fmt_comp(comp_before)}")
    print(f"Composition after:  {fmt_comp(comp_after)}")
    print("Cell (Å):")
    a = swapped.cell
    for i, v in enumerate(a.tolist(), start=1):
        print(f"  a{i}: {v}")
    print(f"PBC: {tuple(swapped.pbc)}")
    print("\nNext steps:")
    print("- In your LAMMPS input, ensure 'mass' and any 'pair_coeff' lines match the Zn/Mg type order in the *output* data file.")
    print("- Run an energy/force minimization (e.g., 'minimize' or FIRE) with your chosen Zn-Mg potential.")
    print("- If the structure is unstable, LAMMPS will show large forces/negative modes and relax to a different configuration.")


if __name__ == "__main__":
    main()
