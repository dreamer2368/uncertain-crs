# lxcat-review

- [Bayesian inference of cross-sections with a Gaussian-process systematic error model](#bayesian-inference-of-cross-sections-with-a-gaussian-process-systematic-error-model)
- [Workflow for cross-section uncertainty propagation](#workflow-for-cross-section-uncertainty-propagation)
  - [Set up input files for BOLSIG](#set-up-input-files-for-bolsig)
  - [Generating cross-section samples](#generating-cross-section-samples)
  - [Running BOLSIG](#running-bolsig)
  - [Storing transport and chemistry outputs](#storing-transport-and-chemistry-outputs)
- [Some useful files](#some-useful-files)

## Bayesian inference of cross-sections with a Gaussian-process systematic error model

Originally, Bayesian calibration of all cross-section model parameters was implemented on the notebook `bolsig/crs-exp-Bayes-gpu.ipynb`.
For a better visibility, this is split into multiple notebooks, each corresponding to a collision:
- `bolsig/UQ-elastic`
- `bolsig/UQ-ionization`
- `bolsig/UQ-stepwise-ionization`
- `bolsig/UQ-1s5`
- `bolsig/UQ-1s4`
- `bolsig/UQ-1s3`
- `bolsig/UQ-1s2`

Experimental measurement data of the cross-sections are stored in `crs-exp/`.
LXCat standard cross-section datasets are stored in `crs/`.
All the result cross-section model parameter samples are stored in `crs-Bayes-gpr/without-swarm/`.

## Workflow for cross-section uncertainty propagation

Forward propagation of cross-section uncertainties is executed via [`BOLSIG+`](https://us.lxcat.net/data/set_type.php) and [`flux`](https://computing.llnl.gov/projects/flux-building-framework-resource-management) on [quartz](https://hpc.llnl.gov/hardware/compute-platforms/quartz).
An example job script for glow-discharge configuration is in `bolsig/glow_discharge.flux`. 
Before running this job script, input files for `BOLSIG+` should be set up (see [Set up input files for BOLSIG+](#set-up-input-files-for-bolsig+)).
After the input file setup, run the job script on quartz:
```
cd bolsig
msub glow_discharge.flux
```
`glow_discharge.flux` is composed of three following stages:
- [Generating cross-section samples](#generating-cross-section-samples)
- [Running BOLSIG](#running-bolsig)
- [Storing transport and chemistry outputs](#storing-transport-and-chemistry-outputs)

### Set up input files for BOLSIG
In order to set up input files for `BOLSIG+`, run the following python file:
```
cd bolsig
python3 forward_propagater.py
```

This essentially does the following:
```
if __name__ == "__main__":
    nSample=720
    setupInputFiles(nSample, rootDir='./glow-discharge', configs=glowDischargeConfigs)
```
- `nSample`: the number of samples that will be run **at each iteration**. This is the number of input files that will be used at each iteration.
In this example, 720 corresponds to 720 processors running 10 times for 7200 samples.
- `rootDir`: the directory where `BOLSIG+` is run and the input/output files is stored.
- `configs`: the condition for `BOLSIG+` solver. For some pre-specified configuration, see `bolsig/input_writer.py`.

The following subdirectories must be manually created in `rootDir`:
```
rootDir
|- crs
|- input
|- output
|- crs-param-samples
|- data
```

### Generating cross-section samples

With `numProcs` the number of processors being used, the same number of cross-section samples are generated at the `k`-th iteration.
```
python3 -c "from forward_propagater import sampleCrossSection; sampleCrossSection(sampleDir='../crs-Bayes-gpr/without-swarm', crsDir='./glow-discharge/crs', nSample=$numProcs, crsParamDir='./glow-discharge/crs-param-samples', iteration=$k);"
```
Generated samples are stored in the directory specified with `crsDir`. Corresponding parameters are stored in the directory specified with `crsParamDir`.

### Running BOLSIG
For a concurrent execution of multiple `BOLSIG+`, we use `flux` framework built in quartz.
This stage requires the executable `bolsigminus` (or `bolsigminus-linux` for linux) in `bolsig` directory.
This corresponds to the command in `glow_discharge.flux`:
```
export commandFile='bolsig2glow.sh'
export FLUX='/usr/global/tools/flux/toss_3_x86_64_ib/default/bin/flux'
srun -N $SLURM_NNODES --mpi=none --mpibind=off $FLUX start ./$commandFile
```
The detailed script of submitting 720 `BOLSIG+` runs is stored in `bolsig/bolsig2glow.sh`.
Please note that this script needs to be manually changed depending on `nSample` or `configs`, mainly this for-loop:
```
JOBIDS=""
for proc in {0..719}
do
JOBIDS="$JOBIDS $(flux mini submit -n 1 --output=/p/lustre1/chung28/lxcat-review/bolsig/out/bolsig_result_${proc}.out ./bolsigminus-linux /p/lustre1/chung28/lxcat-review/bolsig/glow-discharge/input/reaction300K.${proc}.dat)"
###JOBIDS="$JOBIDS $(flux mini submit -n 1 --output=/p/lustre1/chung28/lxcat-review/bolsig/out/bolsig_result_${proc}.out ./bolsigminus-linux /p/lustre1/chung28/lxcat-review/bolsig/glow-discharge/input/reverse300K.${proc}.dat)"
done
```

### Storing transport and chemistry outputs
`BOLSIG+` outputs are post-processed into HDF5 files that can be used in [glowDischarge](https://github.com/pecos/glowDischarge) or [torch1d](https://github.com/pecos/torch1d).
These HDF5 files are stored in `rootDir/data`. This stage corresponds to the following command in `bolsig/glow_discharge.flux`:
```
let "idx=$numProcs*$k"
python3 -c "from forward_propagater import writeBolsigOutputSamples, glowDischargeConfigs; writeBolsigOutputSamples($numProcs, startSampleIndex=$idx, rootDir='./glow-discharge', configs=glowDischargeConfigs, comments='$COMMENTS');"
```
Since 4-specis/6-species mechanisms use lumped excited species, reaction rates are also summed up to represent the lumped states.
Details of this are in `writeBolsigOutputSamples` in `bolsig/forward_propagater.py`.

## Some useful files

### Data directories
- Experimental measurement data: `crs-exp/`
- Swarm-parameter experiment datasets: `swarm/`
- LXCat standard cross-section datasets: `crs/`
- Bayesian-calibrated model parameters: `crs-Bayes-gpr/without-swarm/`

### Python modules
- `bolsig/models.py`: includes all cross-section models.
- `bolsig/crossSections.py`: read/writes LXCat cross-section data files.
- `bolsig/swarmParameters.py`: reads `BOLSIG+` output file.
- `bolsig/crsData.py`: read experimental cross-section datasets in `crs-exp/`.
- `bolsig/swarmData.py`: read experimental swarm-parameter datasets in `swarm/`.
- `bolsig/input_writer.py`: can write `BOLSIG+` input file, with some presets available.
