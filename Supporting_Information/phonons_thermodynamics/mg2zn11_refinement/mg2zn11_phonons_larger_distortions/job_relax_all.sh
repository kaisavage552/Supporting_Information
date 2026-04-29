#!/bin/bash
#PBS -l select=1:ncpus=8:mem=16gb
#PBS -l walltime=02:00:00
#PBS -N mg2zn11_distortions

cd $PBS_O_WORKDIR

module load LAMMPS/2Aug2023_update2-foss-2023a-kokkos

for STRUCT in supercell-001 supercell-002 supercell-003 supercell-004 supercell-005 supercell-006 supercell-007 supercell-008 supercell-009 supercell-010 supercell-011 supercell-012 supercell-013; do
    echo "Relaxing ${STRUCT}..."
    lmp -var STRUCT ${STRUCT} -in in.minimise > log_${STRUCT}.out
done

echo "=== Final potential energies ==="
for STRUCT in supercell-001 supercell-002 supercell-003 supercell-004 supercell-005 supercell-006 supercell-007 supercell-008 supercell-009 supercell-010 supercell-011 supercell-012 supercell-013; do
    echo -n "${STRUCT}: "
    grep "^Min" log_${STRUCT}.out | tail -1
done
