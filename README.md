# uncertain-crs

- [License](#license)
- [Bayesian inference of cross-sections with a Gaussian-process systematic error model](#bayesian-inference-of-cross-sections-with-a-gaussian-process-systematic-error-model)
- [Workflow for cross-section uncertainty propagation](#workflow-for-cross-section-uncertainty-propagation)
  - [Set up input files for BOLSIG](#set-up-input-files-for-bolsig)
  - [Generating cross-section samples](#generating-cross-section-samples)
  - [Running BOLSIG](#running-bolsig)
  - [Storing transport and chemistry outputs](#storing-transport-and-chemistry-outputs)
- [Some useful files](#some-useful-files)

## License

This project is licensed under the **BSD 3-Clause License** — see the [LICENSE.md](LICENSE.md) file for details.

If you use this code, please cite:

> S. W. Chung, T. A. Oliver, L. L. Raja, and R. D. Moser,
> "Characterization of uncertainties in electron-argon collision cross sections,"
> *Plasma Sources Sci. Technol.* **34**, 025009 (2025).
> [https://doi.org/10.1088/1361-6595/adacd5](https://doi.org/10.1088/1361-6595/adacd5)

## Bayesian inference of cross-sections with a Gaussian-process systematic error model

Parametric uncertainties of cross-sections are calibrated via Bayesian inference based on the measurement data in:
- Experimental data: `crs-exp/`
- BSR dataset: `bolsig/crs/BSR.txt` (obtained from [LXCat](https://us.lxcat.net))

Originally, Bayesian calibration of all cross-section model parameters was implemented on the notebook `bolsig/crs-exp-Bayes-gpu.ipynb`.
For a better visibility, this is split into multiple notebooks, each corresponding to a collision:
- `bolsig/UQ-elastic.ipynb`
- `bolsig/UQ-ionization.ipynb`
- `bolsig/UQ-stepwise-ionization.ipynb`
- `bolsig/UQ-1s5.ipynb`
- `bolsig/UQ-1s4.ipynb`
- `bolsig/UQ-1s3.ipynb`
- `bolsig/UQ-1s2.ipynb`

The notebooks above read the measurement data and produce the parameter samples for corresponding cross-section models as:
- `bolsig/crs-Bayes-gpr/without-swarm/crs.elastic.7param.dat`
- `bolsig/crs-Bayes-gpr/without-swarm/crs.ionization.total.dat`
- `bolsig/crs-Bayes-gpr/without-swarm/crs.ionization.step-wise.dat`
- `bolsig/crs-Bayes-gpr/without-swarm/crs.excitation.1s5.dat`
- `bolsig/crs-Bayes-gpr/without-swarm/crs.excitation.1s4.dat`
- `bolsig/crs-Bayes-gpr/without-swarm/crs.excitation.1s3.dat`
- `bolsig/crs-Bayes-gpr/without-swarm/crs.excitation.1s2.dat`

More details are in the notebooks. **NOTE: running the notebook files above will overwrite the sample files in `bolsig/crs-Bayes-gpr/without-swarm/`.**

## Workflow for cross-section uncertainty propagation

Forward propagation of cross-section uncertainties is executed via [`BOLSIG+`](https://us.lxcat.net) and [`flux`](https://computing.llnl.gov/projects/flux-building-framework-resource-management) on [quartz](https://hpc.llnl.gov/hardware/compute-platforms/quartz).
An example job script for glow-discharge configuration is in `bolsig/glow_discharge.flux`. 
Before running this job script, input files for `BOLSIG+` should be set up (see [Set up input files for BOLSIG](#set-up-input-files-for-bolsig)).

### Set up input files for BOLSIG
All the commands will be executed on the `bolsig` directory. Prior to forward propagation sampling, some directories must be set up under the `bolsig` directory:
```
bolsig
|-out
|-rootDir
  |- crs
  |- input
  |- output
  |- crs-param-samples
  |- data
```
In the current repository, `rootDir` is set to be `glow-discharge`. With this hierarchy set, in order to set up input files for `BOLSIG+`, run the following python file:
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
- `configs`: the condition for `BOLSIG+` solver. See `bolsig/input_writer.py` for some pre-specified configuration.

For the example in the current repository, this command generates 720 BOLSIG+ input files:
- `bolsig/glow-discharge/input/reaction300K.0.txt`, `bolsig/glow-discharge/input/reaction300K.1.txt`, ...

The `k`-th input file `'bolsig/glow-discharge/input/reaction300K.%d.txt' % k` is set up to:
- read the cross-section file `'bolsig/glow-discharge/crs/test.crs.%d.txt' % k`
- write the output file `'bolsig/glow-discharge/output/reaction300K.%d.txt' % k`

After the input file setup, run the job script on quartz:
```
cd bolsig
msub glow_discharge.flux
```
`glow_discharge.flux` is composed of three following stages:
- [Generating cross-section samples](#generating-cross-section-samples)
- [Running BOLSIG](#running-bolsig)
- [Storing transport and chemistry outputs](#storing-transport-and-chemistry-outputs)

### Generating cross-section samples

The first stage of `glow_discharge.flux` is the following python command:
```
python3 -c "from forward_propagater import sampleCrossSection; sampleCrossSection(sampleDir='../crs-Bayes-gpr/without-swarm', crsDir='./glow-discharge/crs', nSample=$numProcs, crsParamDir='./glow-discharge/crs-param-samples', iteration=$k);"
```
Where, with the `numProcs` number of processors being used, the same number of cross-section samples are generated at the `k`-th iteration.
Generated samples are stored in the directory specified with `crsDir`. Corresponding parameters are stored in the directory specified with `crsParamDir`.

For the example in the current repository, this command generates:
- sample cross-section files: `bolsig/glow-discharge/crs/test.crs.0.txt`, `bolsig/glow-discharge/crs/test.crs.1.txt`, ...
- corresponding model parameter: `bolsig/glow-discharge/crs-param-samples/crs-params.00000000.h5`, `bolsig/glow-discharge/crs-param-samples/crs-params.00000001.h5`, ...


### Running BOLSIG
We run BOLSIG simulations with
- the input files set up in [Set up input files for BOLSIG](#set-up-input-files-for-bolsig)
- the cross-section files set up in [Generating cross-section samples](#generating-cross-section-samples)

For a concurrent execution of multiple `BOLSIG+`, we use `flux` framework built in quartz.
This stage requires the executable `bolsigminus` (or `bolsigminus-linux` for linux) in `bolsig` directory.
This corresponds to the command in `glow_discharge.flux`:
```
export commandFile='bolsig2glow.sh'
export FLUX='/usr/global/tools/flux/toss_3_x86_64_ib/default/bin/flux'
srun -N $SLURM_NNODES --mpi=none --mpibind=off $FLUX start ./$commandFile
```
The detailed script of submitting 720 `BOLSIG+` runs is stored in `bolsig/bolsig2glow.sh`.
**Please note that the input/output path in this script needs to be manually changed depending on the setup, mainly this for-loop:**
```
JOBIDS=""
for proc in {0..719}   ### <--- CHANGE THE NUMBER BASED ON NSAMPLE
do
### CHANGE INPUT / OUTPUT PATH
JOBIDS="$JOBIDS $(flux mini submit -n 1 --output=./out/bolsig_result_${proc}.out ./bolsigminus-linux ./glow-discharge/input/reaction300K.${proc}.dat)"
done
```

If run successfully, this command generates the BOLSIG+ output files:
- `bolsig/glow-discharge/output/reaction300K.0.txt`, `bolsig/glow-discharge/output/reaction300K.1.txt`, ...

### Storing transport and chemistry outputs
`BOLSIG+` outputs from [Running BOLSIG](#running-bolsig) are post-processed into HDF5 files that can be used in [glowDischarge](https://github.com/pecos/glowDischarge) or [torch1d](https://github.com/pecos/torch1d).
These HDF5 files are stored in `rootDir/data`. This stage corresponds to the following command in `bolsig/glow_discharge.flux`:
```
let "idx=$numProcs*$k"
python3 -c "from forward_propagater import writeBolsigOutputSamples, glowDischargeConfigs; writeBolsigOutputSamples($numProcs, startSampleIndex=$idx, rootDir='./glow-discharge', configs=glowDischargeConfigs, comments='$COMMENTS');"
```
Since 4-specis/6-species mechanisms use lumped excited species, reaction rates are also summed up to represent the lumped states.
Details of this are in `writeBolsigOutputSamples` in `bolsig/forward_propagater.py`.

If run successfully, this command generates HDF5-formatted table files:
- Transport properties: `bolsig/glow-discharge/data/Transport.00000000.h5`, ...
- Ionization rate: `bolsig/glow-discharge/data/Ionization.00000000.h5`, ...
- Stepwise Ionization rate: `bolsig/glow-discharge/data/StepIonization.00000000.h5`, ...
- 1s-lumped state excitation rate (4-species mechanism): `bolsig/glow-discharge/data/1s-lumped.00000000.h5`, ...
- 1s-metastable excitation rate (6-species mechanism): `bolsig/glow-discharge/data/1s-metastable.00000000.h5`, ...
- 1s-resonance excitation rate (6-species mechanism): `bolsig/glow-discharge/data/1s-resonance.00000000.h5`, ...
- 2p-lumped state excitation rate (6-species mechanism): `bolsig/glow-discharge/data/2p-lumped.00000000.h5`, ...

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
- `bolsig/forward_propagater.py`: modules for uncertainty propagation.
