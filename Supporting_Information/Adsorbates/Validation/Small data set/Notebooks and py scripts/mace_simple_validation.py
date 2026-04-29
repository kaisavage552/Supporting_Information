from ase.io import read, write
from ase.optimize import BFGS
from mace.calculators import mace_mp
from pathlib import Path
import json
import sys

# Initialize MACE calculator
try:
    calc = mace_mp(
        model='mace-mh-1.model',
        default_dtype='float64',
        device='cpu',
        head='omat_pbe'
    )
except Exception as e:
    sys.exit(1)

# Input/output directories
input_dir = Path('mace_simple_validation_set')
output_dir = Path('mace_simple_validation_results')
output_dir.mkdir(parents=True, exist_ok=True)

# Structure files
structure_files = {
    'Mg': {
        'file': 'Mg.cif',
        'format': 'cif',
        'formula_atoms': 1,  # atoms per formula unit
        'description': 'Magnesium (hcp)'
    },
    'Zn': {
        'file': 'Zn.cif',
        'format': 'cif',
        'formula_atoms': 1,
        'description': 'Zinc (hcp)'
    },
    'MgO': {
        'file': 'MgO.cif',
        'format': 'cif',
        'formula_atoms': 2,  # MgO = 2 atoms
        'description': 'Magnesium oxide (rocksalt)'
    },
    'ZnO': {
        'file': 'ZnO.cif',
        'format': 'cif',
        'formula_atoms': 2,  # ZnO = 2 atoms
        'description': 'Zinc oxide (wurtzite)'
    },
    'Mg(OH)2': {
        'file': 'Mg_OH_2.cif',
        'format': 'cif',
        'formula_atoms': 5,  # Mg(OH)2 = 1Mg + 2O + 2H = 5 atoms
        'description': 'Magnesium hydroxide (brucite)'
    },
    'Zn(OH)2': {
        'file': 'Zn_OH_2.cif',
        'format': 'cif',
        'formula_atoms': 5,  # Zn(OH)2 = 1Zn + 2O + 2H = 5 atoms
        'description': 'Zinc hydroxide (wulfingite)'
    },
    'MgH2': {
        'file': 'MgH2.cif',
        'format': 'cif',
        'formula_atoms': 3,  # MgH2 = 1Mg + 2H = 3 atoms
        'description': 'Magnesium hydride (rutile)'
    }
}

print(f"\nInput directory: {input_dir}")
print(f"Output directory: {output_dir}")

# Check all files exist
all_exist = True
for compound, info in structure_files.items():
    filepath = input_dir / info['file']
    if filepath.exists():
        print(f" {compound}: {info['file']}")
    else:
        print(f" {compound}: {info['file']} not found")
        all_exist = False

if not all_exist:
    print("\Some files missing.")
    sys.exit(1)

results = {}

for compound, info in structure_files.items():
    print(f"\n{'='*70}")
    print(f"Processing: {compound} - {info['description']}")
    print(f"{'='*70}")
    
    filepath = input_dir / info['file']
    
    try:
        # Load structure
        print(f"Loading: {filepath}")
        if info['format'] == 'lammps-data':
            atoms = read(str(filepath), format='lammps-data', style='atomic')
        else:
            atoms = read(str(filepath))
        
        n_atoms = len(atoms)
        print(f"  Atoms in cell: {n_atoms}")
        
        # Get composition
        from collections import Counter
        composition = Counter(atoms.get_chemical_symbols())
        print(f"  Composition: {dict(composition)}")
        
        # Get initial cell parameters
        cell_lengths = atoms.cell.lengths()
        cell_angles = atoms.cell.angles()
        print(f"  Initial cell: a={cell_lengths[0]:.4f}, b={cell_lengths[1]:.4f}, c={cell_lengths[2]:.4f} Å")
        print(f"  Angles: α={cell_angles[0]:.2f}°, β={cell_angles[1]:.2f}°, γ={cell_angles[2]:.2f}°")
        
        # Attach calculator
        atoms.calc = calc
        
        # Get initial energy
        E_initial = atoms.get_potential_energy()
        E_initial_per_atom = E_initial / n_atoms
        print(f"\n  E_initial: {E_initial:.6f} eV ({E_initial_per_atom:.6f} eV/atom)")
        
        # Relax structure
        print(f"  Relaxing with MACE (fmax=0.01, max_steps=200)...")
        traj_file = output_dir / f'{compound}_relax.traj'
        opt = BFGS(atoms, trajectory=str(traj_file))
        opt.run(fmax=0.01, steps=200)
        
        # Get final energy
        E_final = atoms.get_potential_energy()
        E_final_per_atom = E_final / n_atoms
        delta_E = E_final - E_initial
        delta_E_per_atom = delta_E / n_atoms
        
        # Calculate per formula unit
        n_formula_units = n_atoms / info['formula_atoms']
        E_per_formula = E_final / n_formula_units
        
        # Get final cell parameters
        cell_lengths_final = atoms.cell.lengths()
        cell_angles_final = atoms.cell.angles()
        
        print(f"\n  Results:")
        print(f"    E_final: {E_final:.6f} eV")
        print(f"    E_per_atom: {E_final_per_atom:.6f} eV/atom")
        print(f"    E_per_formula: {E_per_formula:.6f} eV/f.u.")
        print(f"    ΔE (relaxation): {delta_E:.6f} eV ({delta_E_per_atom:.6f} eV/atom)")
        print(f"    Optimization steps: {opt.get_number_of_steps()}")
        print(f"    Final cell: a={cell_lengths_final[0]:.4f}, b={cell_lengths_final[1]:.4f}, c={cell_lengths_final[2]:.4f} Å")
        
        # Check convergence
        converged = opt.get_number_of_steps() < 200
        if converged:
            print(f"Converged")
        else:
            print(f"Hit step limit (may not be fully converged)")
        
        # Save results
        results[compound] = {
            'description': info['description'],
            'n_atoms': n_atoms,
            'composition': dict(composition),
            'formula_atoms': info['formula_atoms'],
            'n_formula_units': n_formula_units,
            'E_initial': E_initial,
            'E_initial_per_atom': E_initial_per_atom,
            'E_final': E_final,
            'E_final_per_atom': E_final_per_atom,
            'E_per_formula': E_per_formula,
            'delta_E': delta_E,
            'delta_E_per_atom': delta_E_per_atom,
            'opt_steps': opt.get_number_of_steps(),
            'converged': converged,
            'cell_initial': {
                'a': cell_lengths[0],
                'b': cell_lengths[1],
                'c': cell_lengths[2],
                'alpha': cell_angles[0],
                'beta': cell_angles[1],
                'gamma': cell_angles[2]
            },
            'cell_final': {
                'a': cell_lengths_final[0],
                'b': cell_lengths_final[1],
                'c': cell_lengths_final[2],
                'alpha': cell_angles_final[0],
                'beta': cell_angles_final[1],
                'gamma': cell_angles_final[2]
            }
        }
        
        # Save relaxed structure
        xyz_file = output_dir / f'{compound}_relaxed.xyz'
        write(str(xyz_file), atoms)
        print(f"Saved: {xyz_file}")
        
    except Exception as e:
        print(f"Error processing {compound}: {e}")
        import traceback
        traceback.print_exc()
        continue

# Save results to JSON
json_file = output_dir / 'mace_simple_validation_results.json'
with open(json_file, 'w') as f:
    json.dump(results, f, indent=2)
