import numpy as np

def readNumber(str):
    try:
        x = np.double(str)
    except ValueError:
        try:
            x = np.double(str[:-4] + 'E' + str[-4:])
        except ValueError:
            raise ValueError('Cannot read the number "%s".' % str)
    return x

# class singleVar:
#     name = ''
#     unit = ''
#     rms, max = 0., 0.
#
#     def __init__(self,name,unit,rms,max):
#         self.name = name
#         self.unit = unit
#         self.rms = rms          # not percent
#         self.max = max          # not percent
#         return

class singleData:
    data = [[]]
    variables = []
    Nvar = 0

    # def printToScreen(self):
    #     print("{0:s}\t{1:s}".format(self.inputName,self.outputName))
    #     for k in range(self.data.shape[0]):
    #         print("{0:.6e}\t{1:.6e}".format(self.data[k,0], self.data[k,1]))
    #     print('\n')

class swarmData:
    datasets = {}

    def __init__(self, filename):
        """Initialize by reading BOLSIG output file."""
        self.ref = ''
        self.datasets = []
        self.parseData(filename)

    def parseData(self, filename):
        """Read swarm data files."""

        with open(filename,'r') as fp:

            Ndata = 0

            line = fp.readline()
            while (line != ''):
                temp = line.strip()
                if ( temp == 'Reference' ):
                    self.ref = fp.readline().strip()
                elif ( temp == 'Data' ):
                    tmp = fp.readline().strip()
                    if ( tmp[0] == '#' ):
                        # read parameter values. Not implemented at this point.
                        tmp = fp.readline().strip()
                        while ( tmp[0] != '#' ):
                            tmp = fp.readline().strip()

                    self.datasets.append(singleData())
                    self.datasets[Ndata].variables = fp.readline().strip().split()
                    self.datasets[Ndata].Nvar = len(self.datasets[Ndata].variables)
                    tmp = fp.readline().strip()
                    if ( tmp[0] == '=' ):
                        tmp = fp.readline().strip()
                        d = tmp.split()
                        self.datasets[Ndata].data = [[readNumber(d[k]) for k in range(self.datasets[Ndata].Nvar)]]
                        tmp = fp.readline().strip()
                        while (tmp[0].isdigit() and not (tmp=='')):
                            d = tmp.split()
                            self.datasets[Ndata].data = np.append(self.datasets[Ndata].data, [[readNumber(d[k]) for k in range(self.datasets[Ndata].Nvar)]], axis=0)
                            tmp = fp.readline().strip()

                    Ndata += 1

                line = fp.readline()

            # for c in self.outputs:
            #     self.outputs[c].printToScreen()
        return


# if __name__ == '__main__':
