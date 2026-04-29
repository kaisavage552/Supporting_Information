# Phonons and Thermodynamics

Phonon band structures, vibrational densities of states, thermal properties (Cv, entropy, free energy), and finite-temperature Gibbs formation free energies for pure Mg, Zn, and five Mg–Zn intermetallics. Gibbs free energies feed into the temperature-dependent convex hull analysis.

---

## Structure

```
phonons_thermodynamics/
├── pure elements/
│   ├── Mg_phonons/          FORCE_SETS, FORCE_CONSTANTS, band.yaml, phonopy.yaml
│   └── Zn_phonons/          (same)
├── intermetallics/
│   ├── mgzn2_phonons/
│   ├── mg4zn7_phonons_good/
│   ├── mg51zn20_phonons/
│   ├── mg21zn25_phonons/
│   └── mg2zn11_phonons/     Standard relaxed structure — see note below
├── mg2zn11_refinement/      Refined Mg₂Zn₁₁ structure and its phonon calculation
│   ├── mg2zn11_phonons_remove_symmetry/
│   └── mg2zn11_phonons_larger_distortions/
│       ├── force_calc_logs/
│       ├── phonon_supercells/
│       └── larger_distortion_structures/
├── band plots/
│   ├── phonon_all_panels_corrected.pdf    Full phonon panel figure for intermetallics
│   ├── phonon_comparison_exp_vs_meam.pdf
│   └── bandplots.ipynb                       Script plotting bands, all plots found here
└── Formation free energy calcs/
    ├── gibbs_formation_energies.csv           ΔGf (eV/atom) at 0–1000 K for all phases
    ├── gibbs_formation_energies_wide.csv      Same data in wide format
    ├── *_thermal_properties.yaml/.dat         Per-phase thermal property output from Phonopy
    ├── convex_hull_300K.png (final)      Convex hull at 300 K
    ├── formation free energy calcs.ipynb      Main analysis notebook
    
```

---

## Important Note — Mg₂Zn₁₁ Refinement

The standard CG-relaxed Mg₂Zn₁₁ structure (in `mg2zn11_phonons/`) yields triply degenerate imaginary frequencies at Γ, indicating a saddle point. A refined structure is stored in `mg2zn11_refinement/`. 0K formation enthalpy for this minimum structure is 0.0125 eV/atom. This structure is the basis for all reported phonon and Gibbs free energy results. See thesis §3.7 for the refinement protocol.

---

## Phonon Calculation Workflow (Phonopy + LAMMPS)

Each phonon directory follows the standard Phonopy finite-displacement approach:

### 1. Generate displaced supercells
```bash
phonopy --lammps -d --dim="2 2 2" -c *_relaxed.data 
```
Displaced supercells are stored as `supercell-*/` and converted to LAMMPS data files.

### 2. Compute forces
```bash
qsub *_phonons.pbs
```
Lammps force input scripts used to compute forces. PBS job scripts (`.pbs`) show the HPC submission commands used.

### 3. Collect forces and calculate phonons
```bash
phonopy --lammps -f forces-{*}.dump
phonopy -c *_relaxed.data --readfc -p band.conf
```
Outputs: `FORCE_SETS`, `FORCE_CONSTANTS`, `band.yaml`, `*_thermal_properties.yaml`.

### 4. Thermal properties → Gibbs free energy
```bash
phonopy-load --writefc
phonopy -t thermal.conf
```
Open `Formation free energy calcs/formation free energy calcs.ipynb`. The notebook reads `*_thermal_properties.yaml/.dat` and computes:

> ΔGf(T) = ΔHf(0K) + [G_compound(T) − x·G_Mg(T) − (1−x)·G_Zn(T)]

Results are written to `gibbs_formation_energies.csv`.

---

## Key Outputs

| File | Description |
|------|-------------|
| `band plots/phonon_all_panels_corrected.pdf` | Phonon band structure panel for all intermetallics (thesis Fig. 6) |
| `band plots/phonon_comparison_exp_vs_meam.pdf` | Phonon band structure panel for pure mg and zn (MEAM calculated and experimental) (thesis Fig. 5) |
| `Formation free energy calcs/gibbs_formation_energies.csv` | Temperature-dependent ΔGf for all phases |
| `Formation free energy calcs/convex_hull_300K_final.png` | Convex hull at 300 K (thesis Fig. 7) |

---

## File Formats

| Extension | Content |
|-----------|---------|
| `FORCE_SETS` | Phonopy-format atomic forces for each displaced supercell |
| `FORCE_CONSTANTS` | Pre-computed force constant matrix |
| `band.yaml` | Phonon eigenvalues along k-path |
| `phonopy.yaml` / `phonopy_disp.yaml` | Phonopy settings and displacement info |
| `*_thermal_properties.yaml` | Cv, entropy, free energy vs. temperature (Phonopy output) |
| `*_thermal_properties.dat` | Same, in plain-text tabular format |
| `.pbs` | HPC batch job submission scripts (cluster-specific, for reference only) |
