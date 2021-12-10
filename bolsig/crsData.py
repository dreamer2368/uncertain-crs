import numpy as np

typeDictS2I = {"Excitation, level 1":                   0,
               "Excitation, level 2":                   1,
               "Excitation, level 3":                   2,
               "Excitation, level 4":                   3}
typeDictI2S = {0: "Excitation, level 1",
               1: "Excitation, level 2",
               2: "Excitation, level 3",
               3: "Excitation, level 4" }

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

class crsData:
    datasets = {}
    Nsets = 0
    variables = {}

    def __init__(self, filename):
        """Initialize by reading crs-exp measurment file."""
        self.ref = ''
        self.datasets = {}
        self.Nsets = 0
        self.variables = {}
        self.parseData(filename)

    def parseData(self, filename):
        """Read crs data files."""

        with open(filename,'r') as fp:

            line = fp.readline()
            while (line != ''):
                temp = line.strip()
                if ( temp == 'Reference' ):
                    self.ref = fp.readline().strip()
                elif ( temp == 'Variables (Var,Unit,Rms,Max)' ):
                    tmp = fp.readline().strip()
                    if ( tmp[0] == '*' ):
                        tmp = fp.readline().strip()
                        while ( tmp[0] != '*' ):
                            item = tmp.split()
                            self.variables.update({item[0]: item[1:]})
                            tmp = fp.readline().strip()
                elif ( temp == 'Data' ):
                    tmp = fp.readline().strip()
                    if ( tmp[0] == '#' ):
                        # read parameter values. Not implemented at this point.
                        tmp = fp.readline().strip()
                        if tmp not in typeDictS2I:
                            nDict = len(typeDictS2I)
                            typeDictS2I[tmp] = nDict
                            typeDictI2S[nDict] = tmp
                        dataType = typeDictS2I[tmp.strip()]
                        if dataType in self.datasets:
                            print("Warning: output '%s' already exists and will be overwritten." % typeDictI2S[dataType])
                        while ( tmp[0] != '#' ):
                            tmp = fp.readline().strip()

                    self.datasets.update({dataType: singleData()})
                    self.datasets[dataType].variables = fp.readline().strip().split()
                    self.datasets[dataType].Nvar = len(self.datasets[dataType].variables)
                    tmp = fp.readline().strip()
                    if ( tmp[0] == '=' ):
                        tmp = fp.readline().strip()
                        d = tmp.split()
                        self.datasets[dataType].data = [[readNumber(d[k]) for k in range(self.datasets[dataType].Nvar)]]
                        tmp = fp.readline().strip()
                        while (tmp[0].isdigit() and not (tmp=='')):
                            d = tmp.split()
                            self.datasets[dataType].data = np.append(self.datasets[dataType].data, [[readNumber(d[k]) for k in range(self.datasets[dataType].Nvar)]], axis=0)
                            tmp = fp.readline().strip()
                    self.Nsets += 1

                line = fp.readline()

            # for c in self.outputs:
            #     self.outputs[c].printToScreen()
        return


# if __name__ == '__main__':
