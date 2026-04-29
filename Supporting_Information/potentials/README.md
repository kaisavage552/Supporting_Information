# Potentials

Interatomic potential files used across this project.

---

## Files

| File | Description |
|------|-------------|
| `library.meam` | MEAM element library — single-element reference parameters for Mg, Zn, Nd, Pb |
| `ZnMg.meam` | MEAM alloy parameter file — cross-species Zn–Mg interaction parameters |
| `mace-mh-1.model` | MACE-MH-1 machine-learning potential (binary model, 57 MB) |

---

## MEAM Potential (Jang et al. 2018)

The 2NN MEAM potential is used for all LAMMPS calculations in `bulk_validation/`, `formation_enthalpies/`, `Elastic_Constants/`, `Surfaces_and_Wulff/`, and `phonons_thermodynamics/`.

**Reference:** H. Jang, B.-J. Lee, 2018. *Interatomic potentials for the Mg–Zn binary system*.


### LAMMPS Usage

```lammps
pair_style  meam/c
pair_coeff  * * library.meam Zn Mg ZnMg.meam Mg Zn
```

Requires LAMMPS compiled with the `USER-MEAMC` (or `MEAM`) package.

---

## MACE-MH-1 Potential

Used exclusively in the `Adsorbates/` section for adsorption energy calculations on MgZn₂(10-10). This is a pre-trained universal machine-learning interatomic potential.

**Model file:** `mace-mh-1.model` (PyTorch format, load with `mace-torch`).

```python
from mace.calculators import MACECalculator
calc = MACECalculator(model_paths='path/to/mace-mh-1.model', device='cpu')
```

Note: the same model file is referenced (not duplicated) by the `Adsorbates/` notebooks via a relative path.
