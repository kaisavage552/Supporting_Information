import argparse
from collections import Counter
from typing import Optional

import numpy as np
from ase import Atoms
from ase.io import read, write

COMMON_STYLES = ["atomic", "full", "charge", "molecular"]


def try_read(path: str, style: Optional[str]) -> tuple[Atoms, str]:
    if style:
        return read(path, format="lammps-data", style=style), style
    last_err = None
    for st in COMMON_STYLES:
        try:
            return read(path, format="lammps-data", style=st), st
        except Exception as e:
            last_err = e
    raise RuntimeError(f"Failed to read {path} with styles {COMMON_STYLES}. Last error: {last_err}")


def swap_by_symbols(atoms: Atoms) -> Atoms:
    new = atoms.copy()
    syms = new.get_chemical_symbols()
    if not (("Mg" in syms) and ("Zn" in syms)):
        return None  # signal not applicable
    mapping = {"Mg": "Zn", "Zn": "Mg"}
    new.set_chemical_symbols([mapping.get(s, s) for s in syms])
    return new


def swap_by_types(atoms: Atoms, type_mg: int, type_zn: int) -> Atoms:
    new = atoms.copy()
    # Get type array from ASE
    for key in ("atomtypes", "types", "type"):
        if key in new.arrays:
            types = np.asarray(new.arrays[key])
            break
    else:
        raise RuntimeError("Could not find an atom type array (atomtypes/types/type) in the input file.")
    if type_mg is None or type_zn is None:
        raise ValueError("When swapping by types you must provide both --type-mg and --type-zn.")

    syms = np.array(new.get_chemical_symbols(), dtype=object)
    # If current symbols are all the same placeholder, that's fine—we overwrite.
    syms[types == type_mg] = "Zn"
    syms[types == type_zn] = "Mg"
    new.set_chemical_symbols(syms.tolist())
    return new


def maybe_jitter(atoms: Atoms, sigma: float, seed: int) -> None:
    if sigma and sigma > 0.0:
        rng = np.random.default_rng(seed)
        disp = rng.normal(0.0, sigma, size=(len(atoms), 3))
        atoms.set_positions(atoms.get_positions() + disp)


def safe_write(outpath: str, atoms: Atoms, style_used: str) -> None:
        try:
        write(outpath, atoms, format="lammps-data", atom_style=style_used)
    except TypeError:
        write(outpath, atoms, format="lammps-data", style=style_used)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Input LAMMPS data file (Mg4Zn7).")
    ap.add_argument("-o", "--output", required=True, help="Output LAMMPS data file (Zn4Mg7).")
    ap.add_argument("--style", choices=COMMON_STYLES, default=None, help="LAMMPS atom_style of input.")
    ap.add_argument("--type-mg", type=int, default=None, help="Type id that is Mg in the INPUT file (use with --type-zn).")
    ap.add_argument("--type-zn", type=int, default=None, help="Type id that is Zn in the INPUT file (use with --type-mg).")
    ap.add_argument("--jitter", type=float, default=0.0, help="Optional random displacement (Å) before writing.")
    ap.add_argument("--seed", type=int, default=42, help="Random seed for --jitter.")
    args = ap.parse_args()

    atoms, style_used = try_read(args.input, args.style)

       swapped = swap_by_symbols(atoms)

    if swapped is None:
        swapped = swap_by_types(atoms, args.type_mg, args.type_zn)

    maybe_jitter(swapped, args.jitter, args.seed)

    comp_in = Counter(atoms.get_chemical_symbols())
    comp_out = Counter(swapped.get_chemical_symbols())
    assert sum(comp_in.values()) == sum(comp_out.values()), "Atom count changed unexpectedly!"
    assert np.allclose(swapped.cell.array, atoms.cell.array), "Cell changed unexpectedly."
    assert np.all(swapped.pbc == atoms.pbc), "PBC changed unexpectedly."

    safe_write(args.output, swapped, style_used)

    
    def fmt_comp(c): return ", ".join(f"{el}:{n}" for el, n in sorted(c.items()))
    print("=== Mg4Zn7 -> Zn4Mg7 swap complete ===")
    print(f"in:  {args.input}")
    print(f"out: {args.output}")
    print(f"atom_style used: {style_used}")
    print(f"composition (in):  {fmt_comp(comp_in)}")
    print(f"composition (out): {fmt_comp(comp_out)}")
    if args.jitter and args.jitter > 0:
        print(f"Applied jitter σ = {args.jitter:.3f} Å (seed {args.seed}).")
    print("Note: Ensure your LAMMPS input uses pair_coeff element order matching the *type order* in the OUTPUT file.")

if __name__ == "__main__":
    main()
