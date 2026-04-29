# Supporting Information

This directory contains all computational data, input files, analysis notebooks, and results supporting my MSci thesis:

> **Validation of the Jang et al. 2NN MEAM Potential for Mg–Zn Alloy Systems**

The potential validated throughout is the second-nearest-neighbour Modified Embedded Atom Method (2NN MEAM) potential of Jang et al. (2018) for the Mg–Zn binary system, assessed against DFT reference data and experiment across bulk, surface, phonon, and adsorbate properties.

---

## Folder Structure

| Folder | Description |
|--------|-------------|
| [`potentials/`](potentials/) | Interatomic potential files — MEAM (Jang et al.) and MACE-MH-1 |
| [`bulk_validation/`](bulk_validation/) | Structural relaxation of pure Mg, Zn and five intermetallics |
| [`formation_enthalpies/`](formation_enthalpies/) | 0 K formation enthalpy calculations for stable, hypothetical, and antisite-defect phases |
| [`Elastic_Constants/`](Elastic_Constants/) | Elastic constant and bulk modulus calculations |
| [`Surfaces_and_Wulff/`](Surfaces_and_Wulff/) | Surface energy calculations and Wulff equilibrium shape construction |
| [`phonons_thermodynamics/`](phonons_thermodynamics/) | Phonon dispersions, thermal properties, and finite-temperature Gibbs free energies |
| [`Adsorbates/`](Adsorbates/) | H, O, and OH adsorption on MgZn₂(10-10) computed with MACE-MH-1, plus MACE validation data |

---

## Software Requirements

### LAMMPS
All molecular-statics and force-constant calculations use **LAMMPS/2Aug2023_update2-foss-2023a-kokkos** compiled with the `USER-MEAMC` package for the `meam/c` pair style.

### Python
Analysis notebooks and scripts require **Python 3.9+**. Install dependencies with:

```
pip install ase phonopy numpy pandas matplotlib scipy mace-torch
```

Key package roles:

| Package | Purpose |
|---------|---------|
| `ase` | Structure reading/writing, slab construction |
| `phonopy` | Phonon band structures and thermal properties |
| `numpy` / `pandas` | Numerical analysis and CSV handling |
| `matplotlib` | All figures and plots |
| `mace-torch` | MACE-MH-1 potential evaluation (adsorbate section only) |

---

## Calculation Workflow

The sections build on each other as follows:

```
potentials/
    │
    ├─→ bulk_validation/          (1. structural relaxation — equilibrium cells)
    │       │
    │       ├─→ formation_enthalpies/   (2. 0 K thermodynamics)
    │       ├─→ Elastic_Constants/      (3. mechanical properties)
    │       │
    │       └─→ phonons_thermodynamics/ (4. force constants → phonons → Gibbs free energies)
    │                   │
    │                   └─→ Surfaces_and_Wulff/  (5. surface energies + Wulff shape)
    │
    └─→ Adsorbates/               (6. MACE-MH-1 adsorbate study — independent of MEAM)
```

---

## Important Notes

**Mg₂Zn₁₁ refinement.** The standard conjugate-gradient-relaxed Mg₂Zn₁₁ structure stored in `bulk_validation/` sits at a saddle point on the MEAM potential-energy surface and yields imaginary phonon frequencies at Γ. A refined minimum-energy structure, obtained by a 13-displacement search protocol, is stored in `phonons_thermodynamics/mg2zn11_refinement/` and is used for all downstream phonon, Gibbs free energy, surface, and adsorbate work. See the thesis §4.5.3 for details.

**Adsorbate calculations use MACE-MH-1, not MEAM.** The `Adsorbates/` section employs the MACE-MH-1 machine-learning potential for adsorption energies on MgZn₂(10-10). These results are not a validation of the MEAM potential itself.

**File extensions.** LAMMPS input scripts carry the extension `.zn` (or `.lammps`) and LAMMPS data files carry `.data`. Phonopy force data is stored in `FORCE_SETS` and `FORCE_CONSTANTS` files following the standard Phonopy convention.

---

## Cross-Reference to Thesis

| Section | Thesis chapter / figures |
|---------|--------------------------|
| `bulk_validation/` | Structural parameters — Table 2-4, §4.1-§4.2 |
| `formation_enthalpies/` | Formation enthalpies — Table 5-8, Fig. 4, §4.3-§4.4|
| `phonons_thermodynamics/` | Phonons, Gibbs free energy, convex hull — Figs 5–7, §4.5 |
| `Elastic_Constants/` | Elastic properties — Table 10, §4.6 |
| `Surfaces_and_Wulff/` | Surface energies, Wulff shape — Table 11-16, Figs 8, §4.7 |
| `Adsorbates/` | Adsorbate binding energies — Table 17, Figs 9–10, §4.8 |
