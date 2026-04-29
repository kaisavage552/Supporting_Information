from ase.build import bulk
from ase.io import write
 
 
def build_hcp(symbol: str, a: float, c: float):
    return bulk(symbol, crystalstructure="hcp", a=a, c=c)
 
 
def main():
    # Magnesium
    mg = build_hcp("Mg", a=3.2094, c=5.2108)
    write("mg_unitcell.data", mg, format="lammps-data", masses=True)
    print(f"Mg: {len(mg)} atoms, a={mg.cell.lengths()[0]:.4f} Å, "
          f"c={mg.cell.lengths()[2]:.4f} Å  →  mg_unitcell.data")
 
    # Zinc
    zn = build_hcp("Zn", a=2.6649, c=4.9470)
    write("zn_unitcell.data", zn, format="lammps-data", masses=True)
    print(f"Zn: {len(zn)} atoms, a={zn.cell.lengths()[0]:.4f} Å, "
          f"c={zn.cell.lengths()[2]:.4f} Å  →  zn_unitcell.data")
 
 
if __name__ == "__main__":
    main()