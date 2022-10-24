#!/bin/bash
#MSUB -l nodes=20
#MSUB -l partition=quartz
#MSUB -l walltime=18:00:00
#MSUB -m be
#MSUB -N bolsig-forward
#MSUB -V
#MSUB -j oe -o result-%j.log
#MSUB -q pbatch

ppn=36
numProcs=$(($SLURM_NNODES*$ppn))
export commandFile='bolsig2glow.sh'
export FLUX='/usr/global/tools/flux/toss_3_x86_64_ib/default/bin/flux'
###export FLUX='/usr/global/tools/flux/toss_3_x86_64_ib/flux-0.17.0-pre-ft/bin/flux'
###export LD_PRELOAD=/usr/global/tools/flux/toss_3_x86_64_ib/flux-0.17.0-pre-ft/lib/flux/libpmi2.so.0

export COMMENTS='This is sample reaction rate computed from bolsig, with glow-discharge nominal configuration. cross section samples are taken from models with Bayesian-inferred params.'

scontrol show job $SLURM_JOBID

chmod u+x $commandFile

for k in {0..9}
do
    python3 -c "from forward_propagater import sampleCrossSection; sampleCrossSection(sampleDir='../crs-Bayes-gpr/without-swarm', crsDir='./glow-discharge/crs', nSample=$numProcs, crsParamDir='./glow-discharge/crs-param-samples', iteration=$k);"
    if [ $? -ne 0 ]; then
        echo "writing crs-sections is not run successfully."
        exit -1
    fi

    srun -N $SLURM_NNODES --mpi=none --mpibind=off $FLUX start ./$commandFile
    if [ $? -ne 0 ]; then
        echo "$commandFile is not run successfully."
        exit -1
    fi

    let "idx=$numProcs*$k"
    python3 -c "from forward_propagater import writeBolsigOutputSamples, glowDischargeConfigs; writeBolsigOutputSamples($numProcs, startSampleIndex=$idx, rootDir='./glow-discharge', configs=glowDischargeConfigs, comments='$COMMENTS');"
    if [ $? -ne 0 ]; then
        echo "depositing samples is not run successfully."
        exit -1
    fi
###    python3 -c "from forward_propagater import depositBolsigSamples, glowDischargeConfigs; depositBolsigSamples($numProcs, rootDir='./glow-discharge', configs=glowDischargeConfigs);"
###    if [ $? -ne 0 ]; then
###        echo "depositing samples is not run successfully."
###        exit -1
###    fi
    scontrol show job $SLURM_JOBID
done

scontrol show job $SLURM_JOBID
