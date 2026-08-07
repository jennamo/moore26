#!/bin/bash
#SBATCH --time=0-01:30:00
#SBATCH -p common
#SBATCH --mem=80G
#SBATCH --output=/hpc/home/jem189/code/moore26/slurm_output/covariance-%A-%a.out
#SBATCH --error=/hpc/home/jem189/code/moore26/slurm_output/covariance-%A-%a.err
#SBATCH --array=1-120

# Specify the path to the config file
config=sf_paramfiles.txt
paramfile=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $2}' $config)

source activate actdesi

python /hpc/home/jem189/code/moore26/covariance.py ${paramfile} >  /hpc/home/jem189/code/moore26/slurm_output/covariance-$SLURM_JOB_ID-$SLURM_ARRAY_TASK_ID.out
