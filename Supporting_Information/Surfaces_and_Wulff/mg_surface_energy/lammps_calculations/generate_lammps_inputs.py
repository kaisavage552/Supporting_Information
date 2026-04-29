import os
import glob

slab_dir = "slabs"
calc_dir = "lammps_calculations"
log_dir = os.path.join(calc_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

slab_files = sorted(glob.glob(os.path.join("Mg_*.data")))

print(f"Found {len(slab_files)} slab files:")
for f in slab_files:
    print(f"  {f}")

for slab_file in slab_files:
    basename = os.path.splitext(os.path.basename(slab_file))[0]
    in_file = os.path.join(calc_dir, f"in.{basename}")
    
    rel_slab = os.path.relpath(slab_file, calc_dir)
    
    lammps_input = f"""# Surface energy relaxation: {basename}
units metal
atom_style atomic
boundary p p p

read_data {rel_slab}

pair_style meam
pair_coeff * * ../library.meam Zn Mg ZnMg.meam Mg

thermo 10
thermo_style custom step pe lx ly lz press pxx pyy pzz

min_style cg
minimize 1e-10 1e-10 10000 100000

variable pe equal pe
print "FINAL_PE = ${{pe}}"
print "FINAL_LX = $(lx)"
print "FINAL_LY = $(ly)"
print "FINAL_LZ = $(lz)"
"""
    
    with open(in_file, 'w') as f:
        f.write(lammps_input)
    
    print(f"Written: {in_file}")

print(f"\nTotal input files: {len(slab_files)}")
