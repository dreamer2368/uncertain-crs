#!/bin/bash
#MSUB -l nodes=2
#MSUB -l partition=quartz
#MSUB -l walltime=0:10:00
#MSUB -m be
#MSUB -N bolsig-forward
#MSUB -V
#MSUB -j oe -o result-%j.log
#MSUB -q pdebug

ppn=36
numProcs=$(($SLURM_NNODES*$ppn))
export commandFile='runBolsig.sh'
export FLUX='/usr/global/tools/flux/toss_3_x86_64_ib/default/bin/flux'
###export FLUX='/usr/global/tools/flux/toss_3_x86_64_ib/flux-0.17.0-pre-ft/bin/flux'
###export LD_PRELOAD=/usr/global/tools/flux/toss_3_x86_64_ib/flux-0.17.0-pre-ft/lib/flux/libpmi2.so.0

scontrol show job $SLURM_JOBID

chmod u+x $commandFile

for k in {1..1}
do
    python3 -c "from forward_propagater import sampleCrossSection; sampleCrossSection(sampleDir='../crs-Bayes-gpr/without-swarm', crsDir='./forward-propagate/crs', nSample=$numProcs);"
    if [ $? -ne 0 ]; then
        echo "writing crs-sections is not run successfully."
        exit -1
    fi
    ###setupInputFiles(nSample,rootDir='./forward-propagate')
    #depositBolsigSamples(2, rootDir='./forward-propagate')
    scontrol show job $SLURM_JOBID

    srun -N $SLURM_NNODES --mpi=none --mpibind=off $FLUX start ./$commandFile
    if [ $? -ne 0 ]; then
        echo "$commandFile is not run successfully."
        exit -1
    fi
    scontrol show job $SLURM_JOBID

    python3 -c "from forward_propagater import depositBolsigSamples; depositBolsigSamples($numProcs, rootDir='./forward-propagate');"
    if [ $? -ne 0 ]; then
        echo "depositing samples is not run successfully."
        exit -1
    fi
    scontrol show job $SLURM_JOBID
done

scontrol show job $SLURM_JOBID
