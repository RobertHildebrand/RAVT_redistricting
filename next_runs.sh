#!/bin/bash
sbatch --array=1-25 --job-name AL_bvap slurm_batch.sh AL bvap_deep
sbatch --array=1-25 --job-name AL_50_50 slurm_batch.sh AL bvap_deep_pp
sbatch --array=1-25 --job-name AL_75_25 slurm_batch.sh AL bvap_deep75_pp25
sbatch --array=1-25 --job-name AL_90_10 slurm_batch.sh AL bvap_deep90_pp10
sbatch --array=1-25 --job-name AL_95_5 slurm_batch.sh AL bvap_deep95_pp5
sbatch --array=1-25 --job-name AL_pp slurm_batch.sh AL compactness
mv *.out outfiles
mv *.*.out outfiles
squeue -A ravt