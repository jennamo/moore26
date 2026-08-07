#!/bin/bash
#SBATCH --time=0-00:25:00
#SBATCH --mem=4G 
#SBATCH -p common
#SBATCH --output=/hpc/home/jem189/code/moore26/slurm_output/make_profile-%A-%a.out
#SBATCH --error=/hpc/home/jem189/code/moore26/slurm_output/make_profile-%A-%a.err
#SBATCH --array=1-640

config=all_paramfiles.txt
##config=srcfree_paramfiles.txt
paramfile=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $2}' $config)


source activate actdesi

python /hpc/home/jem189/code/moore26/make_profile.py ${paramfile} > /hpc/home/jem189/code/moore26/slurm_output/make_profile-$SLURM_JOB_ID-$SLURM_ARRAY_TASK_ID.out
