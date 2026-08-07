#!/bin/bash
#SBATCH --time=0-00:15:00
#SBATCH -p common
#SBATCH -N 1
#SBATCH --mem=32G
#SBATCH --output=/hpc/home/jem189/code/moore26/slurm_output/flag_radio_contamination-%A.out
#SBATCH --error=/hpc/home/jem189/code/moore26/slurm_output/flag_radio_contamination-%A.err

source activate actdesi
python /hpc/home/jem189/code/moore26/flag_radio_contamination.py $1 $2 > /hpc/home/jem189/code/moore26/slurm_output/flag_radio_contamination-$SLURM_JOB_ID.out