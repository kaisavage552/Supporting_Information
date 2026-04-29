# Adsorbates

Adsorption binding energies for H, O, and OH on the MgZn₂(10-10) surface, computed using the MACE-MH-1 machine-learning potential. This section also contains MACE-MH-1 validation data (water formation enthalpy, small validation set of structures) used to verify the choice of MACE-MH-1 as the reference calculator.

> **Note:** All calculations in this section use MACE-MH-1, not the Jang MEAM potential. The results are for adsorption energetics on MgZn₂, which MEAM is not parameterised to describe.

The MACE-MH-1 model file is stored in `../potentials/mace-mh-1.model`.

---

## Structure

```
Adsorbates/
├── MgZn2_10-10/
│   ├── MACE-MH-1 Structures/        coverted unrelaxed and relaxed adsorbate structures (XYZ format)
│   │   ├── clean slab/              Bare MgZn₂(10-10) surface
│   │   ├── H/                       H adsorbed at Mg-top, Zn-top, bridge sites
│   │   ├── O/                       O adsorbed at Mg-top, Zn-top, bridge sites
│   │   └── OH/                      OH adsorbed at Mg-top, bridge sites
│   ├── original DFT structures/     Reference DFT input structures (converted structures in correct format are in MACE-MH-1 Structures/ folder)
│   │   ├── H/
│   │   ├── O/
│   │   └── OH/
│   └── Notebooks/
│       └── binding_energies.ipynb   Computes and tabulates binding energies
└── Validation/
    ├── H2O formation enthalpy test/
    │   ├── water formation enthalpy test.ipynb
    │   └── h2o_formation_test.json
    └── Small data set/
        ├── mace_simple_validation_set/    CIF and LAMMPS data files for Mg, Zn, MgO, ZnO,
        │                                  MgH₂, Mg(OH)₂, Zn(OH)₂
        ├── mace_simple_validation_results/ Relaxed XYZ structures and result JSON
        └── Notebooks and py scripts/
            ├── mace_simple_validation.py
            ├── relax_reference_molecules.py
            └── Mace validation calcs.ipynb
```

---

## Binding Energy Calculation

Adsorption binding energy:

> Eᵦ = E(slab+adsorbate) − E(clean slab) − E(adsorbate reference)

where reference energies for isolated H₂, O₂, and H₂O molecules are computed with MACE-MH-1 (`relax_reference_molecules.py`).

To reproduce the binding energies, open `MgZn2_10-10/Notebooks/binding_energies.ipynb`. The notebook reads the relaxed XYZ structures from `MACE-MH-1 Structures/` and applies the formula above.

---

## MACE Validation

Before using MACE-MH-1 for adsorbate calculations, two validation checks were performed:

1. **H₂O formation enthalpy** (`Validation/H2O formation enthalpy test/`) — verifies the potential reproduces the experimental water formation enthalpy.
2. **Small reference structure set** (`Validation/Small data set/`) — relaxes seven Mg/Zn-containing compounds (oxides, hydroxides, hydrides) and compares lattice parameters and energies against known values.

Results from these checks are recorded in `h2o_formation_test.json` and `mace_simple_validation_results.json`.

---

## Adsorption Sites

| Adsorbate | Sites studied |
|-----------|--------------|
| H | Mg-top, Zn-top, bridge (between Mg sites) |
| O | Mg-top, Zn-top, bridge (between Mg sites) |
| OH | Mg-top, bridge (between Mg sites) |

See thesis §4.8, table 17 and Figs. 9-10 for binding energy tables and visualisations.
