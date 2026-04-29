# Bulk Validation

Structural relaxation of pure elements and Mg–Zn intermetallic compounds using the Jang et al. 2NN MEAM potential. Equilibrium lattice parameters are compared against experiment and DFT where possible.

---

## Structure

```
bulk_validation/
├── pure_elements/
│   ├── Mg/
│   │   ├── inputs/    mg_unitcell.data, mg_unitcell_in.zn, generate_unitcells.py
│   │   └── outputs/   mg_unitcell_relaxed.data, log file
│   └── Zn/
│       ├── inputs/    zn_unitcell.data, zn_unitcell_in.zn
│       └── outputs/   zn_unitcell_relaxed.data, log file
└── intermetallics/
    ├── mgzn2/         MgZn₂  (C14 hexagonal, 12 atoms)
    ├── mg2zn11/       Mg₂Zn₁₁ (cubic Pm-3, 39 atoms)
    ├── mg4zn7/        Mg₄Zn₇  (monoclinic, 110 atoms)
    ├── mg21zn25/      Mg₂₁Zn₂₅ (trigonal, 276 atoms)
    └── mg51zn20/      Mg₅₁Zn₂₀ (276 atoms)
```

Each compound folder contains:
- `inputs/` — crystal structure file (`.data` and `.cif` ), LAMMPS input script (`.zn`), and optionally a Python script used to generate the initial structure
- `outputs/` — relaxed structure (`.data`) and LAMMPS log

---

## Relaxation Protocol

All structures are relaxed to a local energy minimum using conjugate-gradient minimisation with anisotropic cell relaxation (`fix box/relax aniso`). Convergence tolerances: energy 10⁻¹² eV, force 10⁻¹² eV/Å, maximum atomic displacement 0.1 Å per iteration.

To re-run any calculation use:

```bash
lmp -in <phase>_cellrelax_in.zn
```

---

## Key Results

Relaxed lattice parameters are compared against experimental values in the main thesis (Tables 2-4, §4.1-§4.2).

---

## Important Note — Mg₂Zn₁₁

The relaxed Mg₂Zn₁₁ structure here sits at a saddle point on the MEAM potential-energy surface (see `mg2zn11/summary_Mg2Zn11.txt`). A refined minimum-energy structure is stored in `../phonons_thermodynamics/mg2zn11_refinement/` and should be used for all downstream calculations.
