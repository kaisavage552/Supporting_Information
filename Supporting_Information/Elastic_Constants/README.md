# Elastic Constants

Single-crystal elastic constants (Cᵢⱼ) and Voigt–Reuss–Hill bulk modulus (B) for pure Mg and two Mg–Zn intermetallics, calculated using the finite-strain method in LAMMPS.

---

## Structure

```
Elastic_Constants/
├── elastic_constants_summary.csv      Compiled Cᵢⱼ and bulk modulus for all three systems
├── Elastic constants bulk mod calcs.ipynb   Analysis notebook
├── mg_elastic/
│   ├── elastic_mg.in                  LAMMPS input (strain loop)
│   ├── mg_unitcell_relaxed.data       Input structure (from bulk_validation)
│   ├── mg_rerelaxed.data              Re-relaxed at tighter tolerance
│   └── stress_data.txt                Raw stress tensor vs. strain output
├── mgzn2_elastic/
│   ├── elastic_constants.in           Primary LAMMPS input
│   ├── full_workflow.in               Combined relax + strain script
│   ├── check_structure.in             Symmetry-check input
│   ├── diagnose.in                    Diagnostic input
│   ├── mgzn2_relaxed.data
│   ├── mgzn2_rerelaxed.data
│   └── stress_data.txt
└── mg21zn25_elastic/
    ├── elastic_mg21zn25.in
    ├── mg21zn25_relaxed.data
    ├── mg21zn25_rerelaxed.data
    └── stress_data.txt
```

---

## Method

Elastic constants are extracted from the linear stress–strain response. Small strains (±ε, typically ε = 0.001) are applied along each independent deformation mode; the resulting stress tensors are read from `stress_data.txt` and fitted in the analysis notebook.

To re-run a calculation use:

```bash
lmp -in elastic_constants.in
```

---

## Results Summary

| System | C₁₁ (GPa) | C₃₃ (GPa) | C₄₄ (GPa) | B (GPa) |
|--------|-----------|-----------|-----------|---------|
| Pure Mg | 64.7 | 69.6 | 17.1 | 36.9 |
| Mg₂₁Zn₂₅ | 90.7 | 95.6 | 28.0 | 51.9 |
| MgZn₂ | 105.0 | 106.6 | 28.7 | 58.7 |

See thesis Table 3 and §4.3 for comparison against DFT and experimental values.

---

## Analysis Notebook

`Elastic constants bulk mod calcs.ipynb` reads `stress_data.txt` for each system, fits the elastic constants, computes the Voigt–Reuss–Hill averages, and produces the comparison table.
