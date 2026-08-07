#!/bin/bash
#SBATCH --time=0-03:30:00
#SBATCH -p common
#SBATCH -N 1
#SBATCH --mem=500G
#SBATCH -n 40
#SBATCH --array=1-640
#SBATCH --output=/hpc/home/jem189/code/moore26/slurm_output/stack_submaps-%A-%a.out
#SBATCH --error=/hpc/home/jem189/code/moore26/slurm_output/stack_submaps-%A-%a.err

config=all_paramfiles.txt
paramfile=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $2}' $config)

source activate actdesi
isTest=False

python /hpc/home/jem189/code/moore26/stack_submaps.py ${paramfile} $isTest> /hpc/home/jem189/code/moore26/slurm_output/stack-submaps-$SLURM_JOB_ID-$SLURM_ARRAY_TASK_ID.out
