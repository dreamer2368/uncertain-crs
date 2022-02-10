import numpy as np
import crossSections as cross
from swarmParameters import bolsigOutput
from swarmData import kB, Td, swarmDatasets, swarmData
from input_writer import lxcatConfigs, writeInputFile
import models

expDatasets = []
for expDatafile in swarmDatasets:
    filename = "../swarm/" + expDatafile + ".txt"
    expDatasets += [swarmData(filename)]

inputList = ["transport300K","transport77K","transport90K","rate300K"]

# datasets
datasets = ["BSR"]
Nsets = len(datasets)
refset = datasets[0]
filename = "./crs/%s.txt" % refset
refcrs = cross.multipleCrossSections(filename)
targetcrs = cross.multipleCrossSections(filename)

Emax = 1.0e3
Nmax = 150
E_momentum = np.linspace(-4.0, 3.0, Nmax)
E_momentum = 10.0 ** E_momentum
E_momentum = np.append(np.array([1e-17]),E_momentum)

Nw = 50
wtest = np.linspace(-5,9.,Nw)
E_ion = np.exp(wtest) + models.E_ion[0]
E_ion = np.linspace(np.log(E_ion[0]), np.log(Emax), Nw)
E_ion = np.exp(E_ion)

Nw = 50
wtest = np.linspace(-5,9.,Nw)
E_exc = np.exp(wtest)

def generateCrossSection(inputs):

    theta, filename = inputs
    theta_momentum, theta_ion, theta_ext = theta

    crs_momentum = models.elastic_shifted_MERT(theta_momentum, E_momentum)
    crs_momentum = np.append(E_momentum[:,None],crs_momentum[:,None],axis=1)
    crs_momentum[0,0] = 0.0

    crs_ion = models.total_Ion_BED(theta_ion, E_ion)
    crs_ion = np.append(E_ion[:,None],crs_ion[:,None],axis=1)
    crs_ion = np.append(np.array([[models.E_ion[0], 0.0]]), crs_ion, axis=0)

    crs_ext = []
    for k in range(len(models.E_ext)):
        Etarget = E_exc + models.E_ext[k]
        if (k==0) or (k==2):
            tempcrs = models.Excite_metastable(k+1, theta_ext[k], Etarget)
        else:
            tempcrs = models.Excite_resonance_modified(k+1, theta_ext[k], Etarget)
        tempcrs = np.append(Etarget[:,None],tempcrs[:,None],axis=1)
        tempcrs = np.append(np.array([[models.E_ext[k], 0.0]]), tempcrs, axis=0)
        crs_ext += [np.copy(tempcrs)]

    threshold = np.floor( 10.0 * np.array(models.E_ext) ) / 10.0
    for k, c in enumerate(refcrs.crs):
        if ((c.colType==0) or (c.colType==1)):
            targetcrs.crs[k].data = crs_momentum
        elif ((c.colType==3)):
            targetcrs.crs[k].data = crs_ion
            targetcrs.crs[k].deltaE = models.E_ion[0]
        # elif ((c.colType==2) and (c.deltaE > threshold[0]) and (c.deltaE < threshold[1])):
        #     targetcrs.crs[k].data = crs_ext[0]
        #     targetcrs.crs[k].deltaE = models.E_ext[0]
        # elif ((c.colType==2) and (c.deltaE > threshold[1]) and (c.deltaE < threshold[2])):
        #     targetcrs.crs[k].data = crs_ext[1]
        #     targetcrs.crs[k].deltaE = models.E_ext[1]
        # elif ((c.colType==2) and (c.deltaE > threshold[2]) and (c.deltaE < threshold[3])):
        #     targetcrs.crs[k].data = crs_ext[2]
        #     targetcrs.crs[k].deltaE = models.E_ext[2]
        # elif ((c.colType==2) and (c.deltaE > threshold[3]) and (c.deltaE < threshold[3] + 0.1)):
        #     targetcrs.crs[k].data = crs_ext[3]
        #     targetcrs.crs[k].deltaE = models.E_ext[3]

    if (filename is not None):
        targetcrs.writeLXCatFile(filename)
    return targetcrs

def sampleCrossSection(sampleDir='.', crsDir='.', nSample=1):
    sample_momentum = np.fromfile('%s/crs.elastic.7param.dat' % sampleDir)
    sample_momentum = np.reshape(sample_momentum, [int(len(sample_momentum)/9), 9])

    inds = np.random.randint(len(sample_momentum), size=nSample)
    theta_momentum = np.squeeze(sample_momentum[inds,:7])

    sample_ion = np.fromfile('%s/crs.ionization.total.dat' % sampleDir)
    sample_ion = np.reshape(sample_ion, [int(len(sample_ion)/5), 5])

    inds = np.random.randint(len(sample_ion), size=nSample)
    theta_ion = np.squeeze(sample_ion[inds,:3])


    sample_ext = np.fromfile('%s/crs.excitation.1s5.dat' % sampleDir)
    sample_ext = np.reshape(sample_ext, [int(len(sample_ext)/4), 4])

    inds = np.random.randint(len(sample_ext), size=nSample)
    theta_ext1 = np.squeeze(sample_ext[inds,:2])

    sample_ext = np.fromfile('%s/crs.excitation.1s4.dat' % sampleDir)
    sample_ext = np.reshape(sample_ext, [int(len(sample_ext)/4), 4])

    inds = np.random.randint(len(sample_ext), size=nSample)
    theta_ext2 = np.squeeze(sample_ext[inds,:2])

    sample_ext = np.fromfile('%s/crs.excitation.1s3.dat' % sampleDir)
    sample_ext = np.reshape(sample_ext, [int(len(sample_ext)/4), 4])

    inds = np.random.randint(len(sample_ext), size=nSample)
    theta_ext3 = np.squeeze(sample_ext[inds,:2])

    sample_ext = np.fromfile('%s/crs.excitation.1s2.dat' % sampleDir)
    sample_ext = np.reshape(sample_ext, [int(len(sample_ext)/4), 4])

    inds = np.random.randint(len(sample_ext), size=nSample)
    theta_ext4 = np.squeeze(sample_ext[inds,:2])

    inputss = []
    for k in range(nSample):
        theta_ext = [theta_ext1[k], theta_ext2[k], theta_ext3[k], theta_ext4[k]]
        theta = [theta_momentum[k], theta_ion[k], theta_ext]
        filename = '%s/test.crs.%d.txt' % (crsDir, k)
        inputss += [[theta, filename]]
        # print(inputss)

    for inputt in inputss:
        generateCrossSection(inputt)

    return

def setupInputFiles(nSample, rootDir='.'):

    for name, lxcatconfig in lxcatConfigs.items():
        for k in range(nSample):
            inputFile = '%s/input/%s.%d.dat' % (rootDir, name, k)
            crsFile = '%s/crs/test.crs.%d.txt' % (rootDir, k)
            outputFile = '%s/output/%s.%d.dat' % (rootDir, name, k)
            writeInputFile(inputFile, lxcatconfig, crsFile, outputFile)

    return

def depositBolsigSamples(nSample, rootDir="."):

    for config in inputList:
        if (config[:9]=='transport'):
            nPoints = lxcatConfigs[config]['RUNSERIES'][3]
            mu = np.zeros([nSample,nPoints])
            DT = np.zeros([nSample,nPoints])
            DL = np.zeros([nSample,nPoints])
            for k in range(nSample):
                outputFilename = "%s/output/%s.%d.dat" % (rootDir, config, k)
                output = bolsigOutput(outputFilename)
                mu[k,:] = output.outputs[4].data[:,1]
                DT[k,:] = output.outputs[5].data[:,1]
                DL[k,:] = output.outputs[18].data[:,1]
            dataFilename = '%s/data/%s.muN.dat' % (rootDir,config)
            fID = open(dataFilename,'a+b')
            mu.tofile(fID)
            fID.close()
            dataFilename = '%s/data/%s.DTN.dat' % (rootDir,config)
            fID = open(dataFilename,'a+b')
            DT.tofile(fID)
            fID.close()
            dataFilename = '%s/data/%s.DLN.dat' % (rootDir,config)
            fID = open(dataFilename,'a+b')
            DL.tofile(fID)
            fID.close()
        else:
            nPoints = lxcatConfigs[config]['RUNSERIES'][3]
            rate1s5, rate1s4, rate1s3, rate1s2, rateIon = np.zeros([nSample,nPoints]), np.zeros([nSample,nPoints]), np.zeros([nSample,nPoints]), np.zeros([nSample,nPoints]), np.zeros([nSample,nPoints])
            mu = np.zeros([nSample,nPoints])
            # tags = ['C2','C3','C4','C5','C33']
            for k in range(nSample):
                outputFilename = "%s/output/%s.%d.dat" % (rootDir, config, k)
                output = bolsigOutput(outputFilename)
                mu[k,:] = output.outputs[4].data[:,1]
                for idx, table in output.outputs.items():
                    if( (table.collisionType=='Ionization') and (table.deltaE>15.7) and (table.deltaE<15.8) ):
                        rateIon[k,:] = table.data[:,1]
                    elif ( (table.collisionType=='Excitation') and (table.deltaE>11.5) and (table.deltaE<11.6) ):
                        rate1s5[k,:] = np.copy(table.data[:,1])
                    elif ( (table.collisionType=='Excitation') and (table.deltaE>11.6) and (table.deltaE<11.7) ):
                        rate1s4[k,:] = np.copy(table.data[:,1])
                    elif ( (table.collisionType=='Excitation') and (table.deltaE>11.7) and (table.deltaE<11.8) ):
                        rate1s3[k,:] = np.copy(table.data[:,1])
                    elif ( (table.collisionType=='Excitation') and (table.deltaE>11.8) and (table.deltaE<11.9) ):
                        rate1s2[k,:] = np.copy(table.data[:,1])

            dataFilename = '%s/data/%s.muN.dat' % (rootDir,config)
            fID = open(dataFilename,'a+b')
            mu.tofile(fID)
            fID.close()
            dataFilename = '%s/data/%s.ion.dat' % (rootDir,config)
            fID = open(dataFilename,'a+b')
            rateIon.tofile(fID)
            fID.close()
            dataFilename = '%s/data/%s.1s5.dat' % (rootDir,config)
            fID = open(dataFilename,'a+b')
            rate1s5.tofile(fID)
            fID.close()
            dataFilename = '%s/data/%s.1s4.dat' % (rootDir,config)
            fID = open(dataFilename,'a+b')
            rate1s4.tofile(fID)
            fID.close()
            dataFilename = '%s/data/%s.1s3.dat' % (rootDir,config)
            fID = open(dataFilename,'a+b')
            rate1s3.tofile(fID)
            fID.close()
            dataFilename = '%s/data/%s.1s2.dat' % (rootDir,config)
            fID = open(dataFilename,'a+b')
            rate1s2.tofile(fID)
            fID.close()

    return

if __name__ == "__main__":
    nSample=72
    #sampleCrossSection(sampleDir='../crs-Bayes-gpr/without-swarm', crsDir='./forward-propagate/crs', nSample=nSample)
    # setupInputFiles(nSample,rootDir='./forward-propagate')
    depositBolsigSamples(nSample, rootDir='./forward-propagate')
