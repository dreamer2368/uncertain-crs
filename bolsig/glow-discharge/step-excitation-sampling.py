import numpy as np
import h5py
import argparse
import yaml

parser = argparse.ArgumentParser(description = "",
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('input_file', metavar='string', type=str,
                    help='filename for an input file.\n')

if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.input_file) as c:
        dict_ = yaml.safe_load(c)

    sampleDir = dict_['sample_directory']
    import os
    if (sampleDir != '.'): os.makedirs(sampleDir, exist_ok=True)

    f0 = h5py.File(dict_['nominal_file'], 'r')

    error = 1.0e-2 * dict_['relative_uncertainty']

    for k in range(dict_['sample_size']):
        sampleFile = '%s/%s.%08d.h5' % (sampleDir, dict_['prefix'], k)
        with h5py.File(sampleFile, 'w') as f:
            for dset in f0:
                f.copy(f0[dset], dset)
                factor = (1.0 + error) ** np.random.normal()
                f[dset][:,1] *= factor
        if (k%100 == 0):
            print("%d-th sample generated." % k)

    f0.close()
