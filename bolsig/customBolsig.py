import numpy as np
import crossSections as cross
import swarmParameters as swarm

# datasets
datasets = ["Biagi","BSR","Hayashi","IST-Lisbon","Morgan","Phelps","Puech","SIGLO","TRINITI"]
Nsets = len(datasets)

# cross sections.
for dataset in datasets[:-2]:
    filename = "./crs/%s.txt" % dataset
    print("="*50)
    print("  Dataset = {0:s}".format(dataset))
    print("="*50)
    tmp = cross.multipleCrossSections(filename)
    for c in tmp.crs:
        # if ((c.colType==0) or (c.colType==1)):
        if ((c.colType==2)):
            targetmf = c
            filename = './crs/excite-raw/%s.raw.excitation.txt' % (dataset)
            np.savetxt(filename,c.data)

refset = datasets[0]
filename = "./crs/%s.txt" % refset
ref = cross.multipleCrossSections(filename)
# for c in ref.crs:
#     if ((c.colType==0) or (c.colType==1)):
#         refmf = c

## Fixed inelastic collisions.
# for dataset in datasets[1:-2]:
#     filename = "./crs/%s.txt" % dataset
#     print("="*50)
#     print("  Dataset = {0:s}".format(dataset))
#     print("="*50)
#     tmp = cross.multipleCrossSections(filename)
#     for c in tmp.crs:
#         if ((c.colType==0) or (c.colType==1)):
#             targetmf = c
#     for k, c in enumerate(ref.crs):
#         if ((c.colType==0) or (c.colType==1)):
#             ref.crs[k] = targetmf
#     filename = './crs/%s-%s.txt' % (dataset,refset)
#     ref.writeLXCatFile(filename)

# # Variation in Ramsauer minimum
# for k, c in enumerate(ref.crs):
#     if ((c.colType==0) or (c.colType==1)):
#         mask = ((c.data[:,0]<0.04) | (c.data[:,0]>2.))
#         temp = c.data[mask,:]
#
# for dataset in datasets[1:-2]:
#     filename = "./crs/%s.txt" % dataset
#     print("="*50)
#     print("  Dataset = {0:s}".format(dataset))
#     print("="*50)
#     tmp = cross.multipleCrossSections(filename)
#     for c in tmp.crs:
#         if ((c.colType==0) or (c.colType==1)):
#             mask = ((c.data[:,0]>=0.04) & (c.data[:,0]<=2.))
#             targetmf = c.data[mask,:]
#     for k, c in enumerate(ref.crs):
#         if ((c.colType==0) or (c.colType==1)):
#             temp2 = np.append(temp,targetmf,axis=0)
#             ref.crs[k].data = temp2[temp2[:,0].argsort()]
#     filename = './crs/Ramsauer-minimum-variation/%s-%s.txt' % (dataset,refset)
#     ref.writeLXCatFile(filename)

# # Variation at the peak
# for k, c in enumerate(ref.crs):
#     if ((c.colType==0) or (c.colType==1)):
#         mask = ((c.data[:,0]<2.) | (c.data[:,0]>20.))
#         temp = c.data[mask,:]
#
# for dataset in datasets[1:-2]:
#     filename = "./crs/%s.txt" % dataset
#     print("="*50)
#     print("  Dataset = {0:s}".format(dataset))
#     print("="*50)
#     tmp = cross.multipleCrossSections(filename)
#     for c in tmp.crs:
#         if ((c.colType==0) or (c.colType==1)):
#             mask = ((c.data[:,0]>=2.) & (c.data[:,0]<=20.))
#             targetmf = c.data[mask,:]
#     for k, c in enumerate(ref.crs):
#         if ((c.colType==0) or (c.colType==1)):
#             temp2 = np.append(temp,targetmf,axis=0)
#             ref.crs[k].data = temp2[temp2[:,0].argsort()]
#     filename = './crs/peak/%s-%s.txt' % (dataset,refset)
#     ref.writeLXCatFile(filename)

# # Variation at the lower limit
# for k, c in enumerate(ref.crs):
#     if ((c.colType==0) or (c.colType==1)):
#         mask = ((c.data[:,0]>0.04))
#         temp = c.data[mask,:]
#
# for dataset in datasets[1:-2]:
#     filename = "./crs/%s.txt" % dataset
#     print("="*50)
#     print("  Dataset = {0:s}".format(dataset))
#     print("="*50)
#     tmp = cross.multipleCrossSections(filename)
#     for c in tmp.crs:
#         if ((c.colType==0) or (c.colType==1)):
#             mask = ((c.data[:,0]<=0.04))
#             targetmf = c.data[mask,:]
#     for k, c in enumerate(ref.crs):
#         if ((c.colType==0) or (c.colType==1)):
#             temp2 = np.append(temp,targetmf,axis=0)
#             ref.crs[k].data = temp2[temp2[:,0].argsort()]
#     filename = './crs/lowE/%s-%s.txt' % (dataset,refset)
#     ref.writeLXCatFile(filename)

# # Read bolsig output files.
# for dataset in datasets[1:-2]:
#     tmp = swarm.bolsigOutput('./output/lowE/%s-%s.transport.dat' % (dataset,refset))
#     np.savetxt('./output/lowE/%s-%s.muN.raw.txt' % (dataset,refset),tmp.outputs[4].data, fmt='%1.15e')
#     np.savetxt('./output/lowE/%s-%s.DN.raw.txt' % (dataset,refset),tmp.outputs[5].data, fmt='%1.15e')
#     np.savetxt('./output/lowE/%s-%s.DLN.raw.txt' % (dataset,refset),tmp.outputs[18].data, fmt='%1.15e')
