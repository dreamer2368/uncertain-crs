import numpy as np
import crossSections as cross
from swarmParameters import bolsigOutput
from swarmData import kB, Td, swarmDatasets, swarmData
from input_writer import lxcatConfigs, glowDischargeConfigs, writeInputFile
import models

paschen = {'1s5': 0, '1s4': 1, '1s3': 2, '1s2': 3,
           '2p10': 4, '2p9': 5, '2p8': 6, '2p7': 7, '2p6': 8, '2p5': 9, '2p4': 10, '2p3': 11, '2p2': 12, '2p1': 13 }
nExcitation = 14
excitationTags = ['C%d' % (k+2) for k in range(nExcitation)]

# Einstein's transition probability (s^-1), from 2p levels to 1s levels
Akl = np.zeros([4,10])
Akl[0,:] = 1.0e8 * np.array([0.212, 0.366, 0.096, 0.057, 0.274, 0.0, 0.0065, 0.0395, 0.067, 0.0])
Akl[1,:] = 1.0e8 * np.array([0.060, 0.0, 0.233, 0.277, 0.0468, 0.430, 2.5e-4, 0.087, 0.02, 0.00241])
Akl[2,:] = 1.0e8 * np.array([0.0117, 0.0, 0.0, 0.028, 0.0, 0.0, 0.196, 0.0, 0.127, 0.0])
Akl[3,:] = 1.0e8 * np.array([0.0025, 0.0, 0.0161, 0.0115, 0.059, 0.0, 0.147, 0.244, 0.168, 0.472])

expDatasets = []
for expDatafile in swarmDatasets:
    filename = "../swarm/" + expDatafile + ".txt"
    expDatasets += [swarmData(filename)]

inputList = ["transport300K","transport77K","transport90K","rate300K","rate273K"]

# datasets
datasets = ["Biagi+step"]
Nsets = len(datasets)
refset = datasets[0]
filename = "./crs/%s.txt" % refset
refcrs = cross.multipleCrossSections(filename)
exciteIdx = []
for k, c in enumerate(refcrs.crs):
    if (c.colType==2):
        exciteIdx += [ k ]
        # print("reference, %d-th excitation: %.8E" % (k, c.deltaE))
        # print("target, %d-th excitation: %.8E" % (k, targetcrs.crs[k].deltaE))
targetcrs = cross.multipleCrossSections(filename)

nExcitation = 14

Emax = 1.0e3
Nmax = 150
E_momentum = np.linspace(-4.0, 3.0, Nmax)
E_momentum = 10.0 ** E_momentum
E_momentum = np.append(np.array([1e-17]),E_momentum)

Nw = 50
wtest = np.linspace(-5,9.,Nw)
# E_ion = np.exp(wtest) + models.E_ion[0]
E_ion = np.exp(wtest)
E_ion = np.linspace(np.log(E_ion[0]), np.log(Emax), Nw)
E_ion = np.exp(E_ion)

Nw = 50
wtest = np.linspace(-5,9.,Nw)
E_exc = np.exp(wtest)

def addCascadeContribution(inputcrs):
    exciteIdx_ = []
    for k, c in enumerate(inputcrs.crs):
        if (c.colType==2):
            exciteIdx_ += [ k ]
            print("%d-th crs: %.8E" % (k, c.deltaE))
    for s in range(4):
        sLevel = exciteIdx_[s]
        temp = np.copy(inputcrs.crs[sLevel].data)
        for p in range(10):
            pLevel = exciteIdx_[p+4]
            ll = inputcrs.crs[pLevel].data.shape[0]
            # for kk in range(ll):
            #     print(temp[-kk-1,0], ": ", inputcrs.crs[pLevel].data[-kk-1,0])
            temp[-(ll-1):,1] += inputcrs.crs[pLevel].data[1:,1] * Akl[s,p] / np.sum(Akl[:,p])
        inputcrs.crs[sLevel].data = np.copy(temp)

    return inputcrs

def generateCrossSection(inputs):

    theta, filename = inputs
    theta_momentum, theta_ion, theta_ext, theta_step_ion = theta

    crs_momentum = models.elastic_shifted_MERT(theta_momentum, E_momentum)
    crs_momentum = np.append(E_momentum[:,None],crs_momentum[:,None],axis=1)
    crs_momentum[0,0] = 0.0

    Etarget = E_ion + models.E_ion[0]
    crs_ion = models.total_Ion_BED(theta_ion, Etarget)
    crs_ion = np.append(Etarget[:,None],crs_ion[:,None],axis=1)
    crs_ion = np.append(np.array([[models.E_ion[0], 0.0]]), crs_ion, axis=0)

    Etarget = E_ion + models.E_step_ion[0]
    crs_step_ion = models.total_Ion_BED(theta_step_ion, Etarget)
    crs_step_ion = np.append(Etarget[:,None],crs_step_ion[:,None],axis=1)
    crs_step_ion = np.append(np.array([[models.E_step_ion[0], 0.0]]), crs_step_ion, axis=0)

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
    threshold_ion = np.floor( 10.0 * np.array(models.E_ion) ) / 10.0
    for k, c in enumerate(refcrs.crs):
        if ((c.colType==0) or (c.colType==1)):
            targetcrs.crs[k].data = crs_momentum
        elif ((c.colType==3)):
            if ((c.deltaE > threshold_ion[0]) and (c.deltaE < threshold_ion[0] + 0.1)):
                targetcrs.crs[k].data = crs_ion
                targetcrs.crs[k].deltaE = models.E_ion[0]
            else:
                targetcrs.crs[k].data = crs_step_ion
                targetcrs.crs[k].deltaE = models.E_step_ion[0]
        elif ((c.colType==2) and (c.deltaE > threshold[0]) and (c.deltaE < threshold[1])):
            targetcrs.crs[k].data = crs_ext[0]
            targetcrs.crs[k].deltaE = models.E_ext[0]
        elif ((c.colType==2) and (c.deltaE > threshold[1]) and (c.deltaE < threshold[2])):
            targetcrs.crs[k].data = crs_ext[1]
            targetcrs.crs[k].deltaE = models.E_ext[1]
        elif ((c.colType==2) and (c.deltaE > threshold[2]) and (c.deltaE < threshold[3])):
            targetcrs.crs[k].data = crs_ext[2]
            targetcrs.crs[k].deltaE = models.E_ext[2]
        elif ((c.colType==2) and (c.deltaE > threshold[3]) and (c.deltaE < threshold[3] + 0.1)):
            targetcrs.crs[k].data = crs_ext[3]
            targetcrs.crs[k].deltaE = models.E_ext[3]

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

    sample_step_ion = np.fromfile('%s/crs.ionization.step-wise.dat' % sampleDir)
    sample_step_ion = np.reshape(sample_step_ion, [int(len(sample_step_ion)/3), 3])

    inds = np.random.randint(len(sample_step_ion), size=nSample)
    theta_step_ion = np.squeeze(sample_step_ion[inds,:])


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
        theta = [theta_momentum[k], theta_ion[k], theta_ext, theta_step_ion[k]]
        filename = '%s/test.crs.%d.txt' % (crsDir, k)
        inputss += [[theta, filename]]
        # print(inputss)

    for inputt in inputss:
        generateCrossSection(inputt)

    return

def setupInputFiles(nSample, rootDir='.', configs = lxcatConfigs):

    for name, config in configs.items():
        for k in range(nSample):
            inputFile = '%s/input/%s.%d.dat' % (rootDir, name, k)
            crsFile = '%s/crs/test.crs.%d.txt' % (rootDir, k)
            outputFile = '%s/output/%s.%d.dat' % (rootDir, name, k)
            writeInputFile(inputFile, config, crsFile, outputFile)

    return

def getReactionFromBolsig(outputFilename, collisionType, deltaE, deltaERange = 0.5, inputIndex = 3):
    output = bolsigOutput(outputFilename)

    nPoints = output.outputs[0].data.shape[0]
    outputTable = np.zeros([nPoints, 2])

    if inputIndex in output.typeDictI2S:
        print("Input variable: %s" % (output.typeDictI2S[inputIndex]))
    else:
        raise RuntimeError("Input index %d does not exist in output file %s!" % (inputIndex, outputFilename))

    outputTable[:, 0] = output.outputs[inputIndex].data[:, 1]
    for idx, table in output.outputs.items():
        if( (table.collisionType == collisionType) and (table.deltaE > deltaE - deltaERange) and (table.deltaE < deltaE + deltaERange)):
            print ("Output collision type: %s" % table.collisionType)
            print ("Output reaction energy: %.8E" % table.deltaE)
            outputTable[:, 1] = table.data[:, 1]
            return outputTable

    raise RuntimeError("No collision exists for collision type %s and reaction energy %.5E eV!" % (collisionType, deltaE))
    return

def depositBolsigSamples(nSample, rootDir=".", configs = lxcatConfigs):

    for name, config in configs.items():
        if (name[:9]=='transport'):
            nPoints = config['RUNSERIES'][3]
            Te = np.zeros([nSample,nPoints])
            mu = np.zeros([nSample,nPoints])
            DT = np.zeros([nSample,nPoints])
            DL = np.zeros([nSample,nPoints])
            for k in range(nSample):
                outputFilename = "%s/output/%s.%d.dat" % (rootDir, name, k)
                output = bolsigOutput(outputFilename)
                Te[k,:] = output.outputs[3].data[:,1]
                mu[k,:] = output.outputs[4].data[:,1]
                DT[k,:] = output.outputs[5].data[:,1]
                DL[k,:] = output.outputs[18].data[:,1]
            dataFilename = '%s/data/%s.Te.dat' % (rootDir,name)
            fID = open(dataFilename,'a+b')
            Te.tofile(fID)
            fID.close()
            dataFilename = '%s/data/%s.muN.dat' % (rootDir,name)
            fID = open(dataFilename,'a+b')
            mu.tofile(fID)
            fID.close()
            dataFilename = '%s/data/%s.DTN.dat' % (rootDir,name)
            fID = open(dataFilename,'a+b')
            DT.tofile(fID)
            fID.close()
            dataFilename = '%s/data/%s.DLN.dat' % (rootDir,name)
            fID = open(dataFilename,'a+b')
            DL.tofile(fID)
            fID.close()
        else:
            nPoints = config['RUNSERIES'][3]
            rateExcite, rateIon = np.zeros([nSample, nExcitation, nPoints]), np.zeros([nSample,nPoints])
            rateStepIon = np.copy(rateIon)
            Te = np.zeros([nSample,nPoints])
            mu = np.zeros([nSample,nPoints])
            excitationTags = ['C%d' % (k+2) for k in range(nExcitation)]
            for k in range(nSample):
                outputFilename = "%s/output/%s.%d.dat" % (rootDir, name, k)
                output = bolsigOutput(outputFilename)
                Te[k,:] = output.outputs[3].data[:,1]
                mu[k,:] = output.outputs[4].data[:,1]
                for ktag, tag in enumerate(excitationTags):
                    dataType = output.typeDictS2I[tag]
                    rateExcite[k, ktag, :] = output.outputs[dataType].data[:,1]
                for idx, table in output.outputs.items():
                    if( (table.collisionType=='Ionization') and (table.deltaE>15.7) and (table.deltaE<15.8) ):
                        rateIon[k,:] = table.data[:,1]
                if 'C47' in output.typeDictS2I:
                    dataType = output.typeDictS2I['C47']
                    rateStepIon[k, :] = output.outputs[dataType].data[:,1]
                    

            dataFilename = '%s/data/%s.Te.dat' % (rootDir,name)
            fID = open(dataFilename,'a+b')
            Te.tofile(fID)
            fID.close()
            dataFilename = '%s/data/%s.muN.dat' % (rootDir,name)
            fID = open(dataFilename,'a+b')
            mu.tofile(fID)
            fID.close()
            dataFilename = '%s/data/%s.ion.dat' % (rootDir,name)
            fID = open(dataFilename,'a+b')
            rateIon.tofile(fID)
            fID.close()
            dataFilename = '%s/data/%s.excite.dat' % (rootDir,name)
            fID = open(dataFilename,'a+b')
            rateExcite.tofile(fID)
            fID.close()
            dataFilename = '%s/data/%s.step_ion.dat' % (rootDir,name)
            fID = open(dataFilename,'a+b')
            rateStepIon.tofile(fID)
            fID.close()

    return

if __name__ == "__main__":
#    testcrs = addCascadeContribution(refcrs)
#    testcrs.writeLXCatFile("./crs/IST-Lisbon.cascade.txt")
    nSample=72
    #sampleCrossSection(sampleDir='../crs-Bayes-gpr/without-swarm', crsDir='./forward-propagate/crs', nSample=3)
    #setupInputFiles(nSample,rootDir='./forward-propagate')
    setupInputFiles(nSample, rootDir='./glow-discharge', configs=glowDischargeConfigs)
    #depositBolsigSamples(nSample, rootDir='./forward-propagate')
