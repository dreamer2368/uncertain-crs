import numpy as np
import crossSections as cross
import swarmParameters as swarm

# datasets
datasets = ["Biagi","BSR","Hayashi","IST-Lisbon","Morgan","Phelps","Puech","SIGLO","TRINITI"]
Nsets = len(datasets)

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

for dataset in datasets[1:-2]:
    tmp = swarm.bolsigOutput('%s-%s.transport.dat' % (dataset,refset))
    np.savetxt('./output/%s-%s.muN.raw.txt' % (dataset,refset),tmp.outputs[4].data, fmt='%1.15e')
    np.savetxt('./output/%s-%s.DN.raw.txt' % (dataset,refset),tmp.outputs[5].data, fmt='%1.15e')
    np.savetxt('./output/%s-%s.DLN.raw.txt' % (dataset,refset),tmp.outputs[18].data, fmt='%1.15e')
