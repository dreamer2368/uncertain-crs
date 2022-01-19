import numpy as np
import crossSections as cross
from swarmParameters import bolsigOutput
from swarmData import kB, Td
from models import elastic_MERT

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

def GenerateCrossSection(theta,filename=None):
    testcrs = elastic_MERT(theta,Etarget)
    testcrs = np.append(Etarget[:,None],testcrs[:,None],axis=1)
    for k, c in enumerate(refcrs.crs):
        if ((c.colType==0) or (c.colType==1)):
            temp2 = np.append(temp,testcrs,axis=0)
            targetcrs.crs[k].data = temp2[temp2[:,0].argsort()]
    if (filename is not None):
        targetcrs.writeLXCatFile(filename)
    return targetcrs

def RunBolsig(rootDir=".", dataDir=".", verbose=False, check_time=False):
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

def ConvertBolsigData(expDataset, bolsigData):
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
