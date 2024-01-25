#!/bin/bash
sbatch --array=10-13 --job-name AL_cnty slurm_batch_cnty.sh AL dem_gerrymander
sbatch --array=10-13 --job-name AK_cnty slurm_batch_cnty.sh AK dem_gerrymander
sbatch --array=10-13 --job-name AZ_cnty slurm_batch_cnty.sh AZ dem_gerrymander
sbatch --array=10-13 --job-name AR_cnty slurm_batch_cnty.sh AR dem_gerrymander
sbatch --array=10-13 --job-name CA_cnty slurm_batch_cnty.sh CA dem_gerrymander
sbatch --array=10-13 --job-name CO_cnty slurm_batch_cnty.sh CO dem_gerrymander
sbatch --array=10-13 --job-name CT_cnty slurm_batch_cnty.sh CT dem_gerrymander
sbatch --array=10-13 --job-name DC_cnty slurm_batch_cnty.sh DC dem_gerrymander
sbatch --array=10-13 --job-name DE_cnty slurm_batch_cnty.sh DE dem_gerrymander
sbatch --array=10-13 --job-name FL_cnty slurm_batch_cnty.sh FL dem_gerrymander
sbatch --array=10-13 --job-name GA_cnty slurm_batch_cnty.sh GA dem_gerrymander
sbatch --array=10-13 --job-name HI_cnty slurm_batch_cnty.sh HI dem_gerrymander
sbatch --array=10-13 --job-name ID_cnty slurm_batch_cnty.sh ID dem_gerrymander
sbatch --array=10-13 --job-name IL_cnty slurm_batch_cnty.sh IL dem_gerrymander
sbatch --array=10-13 --job-name IN_cnty slurm_batch_cnty.sh IN dem_gerrymander
sbatch --array=10-13 --job-name IA_cnty slurm_batch_cnty.sh IA dem_gerrymander
sbatch --array=10-13 --job-name KS_cnty slurm_batch_cnty.sh KS dem_gerrymander
sbatch --array=10-13 --job-name KY_cnty slurm_batch_cnty.sh KY dem_gerrymander
sbatch --array=10-13 --job-name LA_cnty slurm_batch_cnty.sh LA dem_gerrymander
sbatch --array=10-13 --job-name ME_cnty slurm_batch_cnty.sh ME dem_gerrymander
sbatch --array=10-13 --job-name MD_cnty slurm_batch_cnty.sh MD dem_gerrymander
sbatch --array=10-13 --job-name MA_cnty slurm_batch_cnty.sh MA dem_gerrymander
sbatch --array=10-13 --job-name MI_cnty slurm_batch_cnty.sh MI dem_gerrymander
sbatch --array=10-13 --job-name MN_cnty slurm_batch_cnty.sh MN dem_gerrymander
sbatch --array=10-13 --job-name MS_cnty slurm_batch_cnty.sh MS dem_gerrymander
sbatch --array=10-13 --job-name MO_cnty slurm_batch_cnty.sh MO dem_gerrymander
sbatch --array=10-13 --job-name MT_cnty slurm_batch_cnty.sh MT dem_gerrymander
sbatch --array=10-13 --job-name NE_cnty slurm_batch_cnty.sh NE dem_gerrymander
sbatch --array=10-13 --job-name NV_cnty slurm_batch_cnty.sh NV dem_gerrymander
sbatch --array=10-13 --job-name NH_cnty slurm_batch_cnty.sh NH dem_gerrymander
sbatch --array=10-13 --job-name NJ_cnty slurm_batch_cnty.sh NJ dem_gerrymander
sbatch --array=10-13 --job-name NM_cnty slurm_batch_cnty.sh NM dem_gerrymander
sbatch --array=10-13 --job-name NY_cnty slurm_batch_cnty.sh NY dem_gerrymander
sbatch --array=10-13 --job-name NC_cnty slurm_batch_cnty.sh NC dem_gerrymander
sbatch --array=10-13 --job-name ND_cnty slurm_batch_cnty.sh ND dem_gerrymander
sbatch --array=10-13 --job-name OH_cnty slurm_batch_cnty.sh OH dem_gerrymander
sbatch --array=10-13 --job-name OK_cnty slurm_batch_cnty.sh OK dem_gerrymander
sbatch --array=10-13 --job-name OR_cnty slurm_batch_cnty.sh OR dem_gerrymander
sbatch --array=10-13 --job-name PA_cnty slurm_batch_cnty.sh PA dem_gerrymander
sbatch --array=10-13 --job-name RI_cnty slurm_batch_cnty.sh RI dem_gerrymander
sbatch --array=10-13 --job-name SC_cnty slurm_batch_cnty.sh SC dem_gerrymander
sbatch --array=10-13 --job-name SD_cnty slurm_batch_cnty.sh SD dem_gerrymander
sbatch --array=10-13 --job-name TN_cnty slurm_batch_cnty.sh TN dem_gerrymander
sbatch --array=10-13 --job-name TX_cnty slurm_batch_cnty.sh TX dem_gerrymander
sbatch --array=10-13 --job-name UT_cnty slurm_batch_cnty.sh UT dem_gerrymander
sbatch --array=10-13 --job-name VT_cnty slurm_batch_cnty.sh VT dem_gerrymander
sbatch --array=10-13 --job-name VA_cnty slurm_batch_cnty.sh VA dem_gerrymander
sbatch --array=10-13 --job-name WA_cnty slurm_batch_cnty.sh WA dem_gerrymander
sbatch --array=10-13 --job-name WV_cnty slurm_batch_cnty.sh WV dem_gerrymander
sbatch --array=10-13 --job-name WI_cnty slurm_batch_cnty.sh WI dem_gerrymander
sbatch --array=10-13 --job-name WY_cnty slurm_batch_cnty.sh WY dem_gerrymander
mv *.out outfiles
mv *.*.out outfiles
squeue -A ravt