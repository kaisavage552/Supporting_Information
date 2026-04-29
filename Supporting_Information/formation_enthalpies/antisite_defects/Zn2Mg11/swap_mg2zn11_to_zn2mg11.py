import argparse
from collections import Counter
from typing import Optional

import numpy as np
from ase import Atoms
from ase.io import read, write


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
        f"Failed to read {path} with styles {COMMON_STYLES}. Last error: {last_err}"
    )


def swap_species(atoms: Atoms, mapping: dict[str, str]) -> Atoms:
    new = atoms.copy()
    symbols = new.get_chemical_symbols()
    new.set_chemical_symbols([mapping.get(s, s) for s in symbols])
    return new


def maybe_jitter_positions(atoms: Atoms, sigma: float, seed: int = 42) -> None:
    if sigma and sigma > 0.0:
        rng = np.random.default_rng(seed)
        disp = rng.normal(loc=0.0, scale=sigma, size=(len(atoms), 3))
        atoms.set_positions(atoms.get_positions() + disp)


def safe_write_lammps_data(outpath: str, atoms: Atoms, style_used: str) -> None:
        try:
        write(outpath, atoms, format="lammps-data", atom_style=style_used)
    except TypeError:
        write(outpath, atoms, format="lammps-data", style=style_used)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Input LAMMPS data file (Mg2Zn11).")
    ap.add_argument("-o", "--output", required=True, help="Output LAMMPS data file (Zn2Mg11).")
    ap.add_argument("--style", choices=COMMON_STYLES, default=None,
                   help="LAMMPS atom style of the input data. If omitted, auto-detect.")
    ap.add_argument("--jitter", type=float, default=0.0,
                   help="Optional Gaussian position jitter (Å) before writing (default 0.0).")
    ap.add_argument("--seed", type=int, default=42, help="Random seed for --jitter.")
    args = ap.parse_args()

    atoms, style_used = try_read_lammps_data(args.input, style=args.style)

    comp_before = Counter(atoms.get_chemical_symbols())

    mapping = {"Mg": "Zn", "Zn": "Mg"}
    swapped = swap_species(atoms, mapping)

    maybe_jitter_positions(swapped, args.jitter, seed=args.seed)

    comp_after = Counter(swapped.get_chemical_symbols())

    assert sum(comp_before.values()) == sum(comp_after.values()), "Atom count changed unexpectedly!"
    assert np.allclose(swapped.cell.array, atoms.cell.array), "Cell changed unexpectedly."
    assert np.all(swapped.pbc == atoms.pbc), "PBC changed unexpectedly."

    safe_write_lammps_data(args.output, swapped, style_used)

    def fmt_comp(c): return ", ".join(f"{el}:{n}" for el, n in sorted(c.items()))
    a = swapped.cell
    print("=== Zn2Mg11 Swap Summary ===")
    print(f"Input file:      {args.input}")
    print(f"Output file:     {args.output}")
    print(f"Atom style:      {style_used}")
    print(f"Composition in:  {fmt_comp(comp_before)}")
    print(f"Composition out: {fmt_comp(comp_after)}")
    print("Cell (Å):")
    for i, v in enumerate(a.tolist(), start=1):
        print(f"  a{i}: {v}")
    print(f"PBC:             {tuple(swapped.pbc)}")
    if args.jitter and args.jitter > 0:
        print(f"Applied random jitter σ = {args.jitter:.3f} Å (seed {args.seed}).")
    print("\nNext steps:")
    print("- Ensure your LAMMPS 'mass' and 'pair_coeff' lines match the new type order in the output data file.")
    print("- Relax with minimize/FIRE (and optionally box/relax) using your chosen Zn–Mg potential.")


if __name__ == "__main__":
    main()
