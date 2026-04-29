# Formation Enthalpies

0 K formation enthalpy calculations for three categories of Mg–Zn phases: experimentally stable compounds, hypothetical prototype structures, and antisite-defect supercells.

Formation enthalpy is defined as:

> ΔHf = E(MgₓZn₁₋ₓ) − x·E(Mg) − (1−x)·E(Zn)    [eV/atom]

Reference energies for pure Mg and Zn are taken from the relaxed structures in `../bulk_validation/pure_elements/`.

---

## Structure

```
formation_enthalpies/
├── stable_phases/
│   ├── results_stable.csv          MEAM formation enthalpies for five stable phases
│   └── comparison_vs_DFT.csv       Comparison against DFT (Du 2023), experiment, and Jang (2018) MEAM
├── hypothetical_phases/
│   ├── Prototype structure sources for hypotheticals.txt   Crystal structure provenance
│   ├── results_hypothetical.csv
│   ├── Mg2Zn_C11b/                 MgSi₂-type (I4/mmm), 2:1 stoichiometry
│   ├── MgZn2_C11b/                 MgSi₂-type (I4/mmm), 1:2 stoichiometry
│   └── mgzn_B2/                    CsCl-type (Pm-3m), 1:1 stoichiometry
├── antisite_defects/
│   ├── results_antisite.csv
│   ├── Zn2Mg11/
│   ├── Zn4Mg7/
│   └── ZnMg2/
└── Formation enthalpies calculations.ipynb    Full analysis and convex hull (0 K)
```

Each calculation subdirectory contains `inputs/` (structure `.data` and LAMMPS script) and `outputs/` (relaxed structure and log).

---

## CSV File Descriptions

**`stable_phases/results_stable.csv`** — columns: `Phase`, `x_Zn`, `Atoms/Cell`, `E_total (eV)`, `ΔHf (eV/atom)`

**`stable_phases/comparison_vs_DFT.csv`** — columns: `Phase`, `MEAM (this work)`, `DFT (Du 2023)`, `Experiment`, `Jang MEAM (2018)`, `Deviation vs DFT (%)`

**`hypothetical_phases/results_hypothetical.csv`** and **`antisite_defects/results_antisite.csv`** — same schema as `results_stable.csv`.

---

## Reproducing the Analysis

Open `Formation enthalpies calculations.ipynb`. The notebook:
1. Calculates formation enthalpies for stable phases, antisite structures and hypothetical structures
2. Creates csv files for values (Kelpsa's unpublished data was added after csv file was created by notebook)
3. Produces the comparison tables shown in the thesis

Then use values to plot 0K convex hull shown in thesis

---

## Results Summary

| Phase | x_Zn | ΔHf MEAM (eV/atom) |
|-------|------|-------------------|
| MgZn₂ | 0.667 | −0.1064 |
| Mg₄Zn₇ | 0.636 | −0.1016 |
| Mg₂₁Zn₂₅ | 0.543 | −0.0890 |
| Mg₅₁Zn₂₀ | 0.282 | −0.0280 |
| Mg₂Zn₁₁ | 0.846 | −0.0119 |

See thesis Table 6 and §4.3 for comparison against DFT and experimental values.
