#!/bin/bash
#SBATCH --time=0-00:15:00
#SBATCH --mem=4G 
#SBATCH -p common
#SBATCH --output=/hpc/home/jem189/code/moore26/slurm_output/deproj_cib_sf-%A-%a.out
#SBATCH --error=/hpc/home/jem189/code/moore26/slurm_output/deproj_cib_sf-%A-%a.err
#SBATCH --array=1-40

config=all_samples.txt
sample=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $2}' $config)


source activate actdesi

python /hpc/home/jem189/code/moore26/deproj_cib_sf.py ${sample} > /hpc/home/jem189/code/moore26/slurm_output/deproj_cib_sf-$SLURM_JOB_ID-$SLURM_ARRAY_TASK_ID.out
