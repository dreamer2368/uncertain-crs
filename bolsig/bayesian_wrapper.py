import numpy as np
import crossSections as cross
from swarmParameters import bolsigOutput
from swarmData import kB, Td, swarmDatasets, swarmData
from input_writer import expConfigs, writeInputFile
from models import elastic_MERT

expDatasets = []
for expDatafile in swarmDatasets:
    filename = "../swarm/" + expDatafile + ".txt"
    expDatasets += [swarmData(filename)]

inputList = ["AlAminLucas1987","MilloyCrompton1977","NakamuraKurachi1988"]

# datasets
datasets = ["Biagi"]
Nsets = len(datasets)
refset = datasets[0]
filename = "./crs/%s.txt" % refset
refcrs = cross.multipleCrossSections(filename)
targetcrs = cross.multipleCrossSections(filename)
for k, c in enumerate(refcrs.crs):
    if ((c.colType==0) or (c.colType==1)):
        mask = (c.data[:,0]>1.)
        temp = c.data[mask,:]

Etarget = np.linspace(-4.0,0.0,50)
Etarget = 10.0 ** Etarget

def generateCrossSection(theta,filename=None):
    testcrs = elastic_MERT(theta,Etarget)
    testcrs = np.append(Etarget[:,None],testcrs[:,None],axis=1)
    for k, c in enumerate(refcrs.crs):
        if ((c.colType==0) or (c.colType==1)):
            temp2 = np.append(temp,testcrs,axis=0)
            targetcrs.crs[k].data = temp2[temp2[:,0].argsort()]
    if (filename is not None):
        targetcrs.writeLXCatFile(filename)
    return targetcrs

def runBolsig(rootDir=".", dataDir=".", verbose=False, check_time=False):
    from os.path import exists, isdir
    import subprocess

    if (check_time):
        from time import perf_counter
        times = np.zeros((2,))

    if (not exists(rootDir + "/bolsigminus")):
        raise RuntimeError("Failed to find bolsigminus.")
    if (not (isdir(dataDir) and isdir(dataDir+"/input") and isdir(dataDir+"/output"))):
        raise RuntimeError("Failed to find input/output data directories.")

    bolsigOutputs = []
    for swarmdataset in inputList:
        inputFilename = "%s/input/input-%s.dat" % (dataDir, swarmdataset)
        command = "%s/bolsigminus %s" %(rootDir, inputFilename)

        if (check_time): tic = perf_counter()
        subprocess.check_call(command,shell=True)
        if (check_time):
            toc = perf_counter()
            times[0] += toc - tic

        outputFilename = "%s/output/output-%s.dat" % (dataDir, swarmdataset)

        if (check_time): tic = perf_counter()
        bolsigOutputs += [ bolsigOutput(outputFilename, verbose) ]
        if (check_time):
            toc = perf_counter()
            times[1] += toc - tic

    if (check_time):
        return bolsigOutputs, times
    else:
        return bolsigOutputs

def convertBolsigData(expDataset, bolsigData):
    bolsigVariables = {}

    for var in expDataset.variables:
        if ( (var == 'E/N') or (var[-4:] == '-rms') or (var[-4:] == '-max') ): continue

        # for index, refer to typeDictI2S in swarmParameters.py
        if ( var == 'W' ):
            bolsigVariables.update({var: bolsigData.outputs[4].data[:,0] / Td * bolsigData.outputs[4].data[:,1]})
        elif ( var == 'DT/mu' ):
            bolsigVariables.update({var: bolsigData.outputs[5].data[:,1] / bolsigData.outputs[4].data[:,1]})
        elif ( var == 'DLN' ):
            bolsigVariables.update({var: bolsigData.outputs[18].data[:,1]})

    return bolsigVariables

def log_likelihood_parallel(theta):
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    bdir = "./bayesian-bolsig"

    from os.path import exists
    from os import makedirs
    if (not exists('%s/%d/input' % (bdir, rank)) ): makedirs('%s/%d/input' % (bdir, rank))
    if (not exists('%s/%d/output' % (bdir, rank)) ): makedirs('%s/%d/output' % (bdir, rank))

    crsFilename = "%s/crs/test-crs.%d.txt" % (bdir, rank)
    # compute log-normal probability
    testcrs = generateCrossSection(theta,filename=crsFilename)
    for exp in swarmDatasets:
        inputFilename = "%s/%d/input/input-%s.dat" % (bdir, rank, exp)
        outputFilename = "%s/%d/output/output-%s.dat" % (bdir, rank, exp)
        writeInputFile(inputFilename, expConfigs[exp], crsFilename, outputFilename)

    outputs = runBolsig(dataDir="./bayesian-bolsig/%d" % rank)

    lk = 0.0
    for k, expData in enumerate(expDatasets): # per each experiment
        for expDataTable in expData.datasets: # per each table in an experiment
            bolsigData = convertBolsigData(expDataTable,outputs[k])
            for kk, var in enumerate(expDataTable.variables): # per each variable in a table
                if ( (var == 'E/N') or (var[-4:] == '-rms') or (var[-4:] == '-max') ): continue
                y = expDataTable.variables[var]
                yerr = expDataTable.variables[var+'-rms']
                sigma2 = np.log(1.0 + yerr / y) ** 2
                pred_y = bolsigData[var]
                lk += - 0.5 * np.sum( (np.log(y) - np.log(pred_y)) ** 2 / sigma2 )
                lk += - 0.5 * np.sum( np.log(2.0*np.pi*sigma2) )

    return lk

def log_prior(theta):
    theta_ref = np.array([-1.489, 65.0, -82.9, 0.881])
    sigma2 = ( 0.5 * theta_ref )**2
    return - 0.5 * np.sum( (theta - theta_ref)**2 / sigma2 + np.log(2.0*np.pi*sigma2) )

def log_posterior(theta):
    lp = log_prior(theta)
    lk = log_likelihood_parallel(theta)
    if (not np.isfinite(lp)) or (not np.isfinite(lk)):
        return - np.inf
    return lp + lk

if __name__ == "__main__":
    import sys
    from schwimmbad import MPIPool
    from mpi4py import MPI
    import emcee

    comm = MPI.COMM_WORLD
    with MPIPool(comm) as pool:
        if not pool.is_master():
            pool.wait()
            sys.exit(0)

        np.random.seed(42)
        nwalkers = 14
        theta_ref = np.array([-1.489, 65.0, -82.9, 0.881])
        ndim = len(theta_ref)
        pos = theta_ref * (1.0 + 0.1 * np.random.randn(nwalkers,ndim) )

        sampler = emcee.EnsembleSampler(
            nwalkers, ndim, log_posterior, pool=pool
        )
        sampler.run_mcmc(pos, 1500, progress=True);

    tau = sampler.get_autocorr_time()
    print(tau)
    maxtau = np.amax(tau)

    flat_samples = sampler.get_chain(discard=2*maxtau, thin=int(maxtau/2), flat=True)
    print(flat_samples.shape)

    flat_samples.tofile('./bayesian-bolsig/posterior_sample.dat')

    print("all is done.")
