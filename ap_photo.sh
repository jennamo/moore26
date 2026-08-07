#!/bin/bash
#SBATCH --time=0-08:00:00
#SBATCH -N 1
#SBATCH -n 40
#SBATCH -p common
#SBATCH --output=/hpc/home/jem189/code/moore26/slurm_output/ap_photo-%A-%a.out
#SBATCH --error=/hpc/home/jem189/code/moore26/slurm_output/ap_photo-%A-%a.err
#SBATCH --array=1-48

config=ap_photo_config.txt
paramfile=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $2}' $config)

source activate actdesi
isTest=False
python /hpc/home/jem189/code/moore26/ap_photo.py ${paramfile} $isTest> /hpc/home/jem189/code/moore26/slurm_output/ap_photo-$SLURM_JOB_ID-$SLURM_ARRAY_TASK_ID.out