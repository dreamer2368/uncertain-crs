import numpy as np

typeDictS2I = {"Excitation, level 1":                   0,
               "Excitation, level 2":                   1,
               "Excitation, level 3":                   2,
               "Excitation, level 4":                   3,
               "Ionization, 1+":                        4,
               "Ionization, total":                     5,
               "Ionization, 2+":                        6,
               "Ionization, 3+":                        7,
               "Ionization, 4+":                        8,
               "Elastic, integral":                     9,
               "Elastic, momentum":                     10,
               "Step-wize Ionization, 1+":              11}
typeDictI2S = {}
for key, value in typeDictS2I.items():
    typeDictI2S.update({value: key})
# typeDictI2S = {0: "Excitation, level 1",
#                1: "Excitation, level 2",
#                2: "Excitation, level 3",
#                3: "Excitation, level 4" }

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
    error_provided = False

    def __init__(self):
        self.data = [[]]
        self.variables = []
        self.Nvar = 0
        error_provided = False

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
        self.convertData()

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

    def convertData(self):

        for dataType, dataset in self.datasets.items():
            temp = np.copy(dataset.data)
            var1 = dataset.variables[1]
            dataset.error_provided = True

            if ( self.variables[var1][0] == 'cm2' ):
                temp[:,1] *= 1e-4
            elif ( self.variables[var1][0] == 'cm2eV' ):
                temp[:,1] *= 1e-4
                temp[:,1] /= temp[:,0]

            if ( self.variables[var1][1]!='n/a' ):
                error = temp[:,1][...,None] * 1e-2 * readNumber(self.variables[var1][1][:-1])
                temp = np.append( temp, error, axis=1)
            elif (self.variables[var1][2]!='n/a'):
                error = temp[:,1][...,None] * 1e-2 / 3.0 * readNumber(self.variables[var1][2][:-1])
                temp = np.append( temp, error, axis=1)
            elif (len(dataset.variables)>2):
                var2 = dataset.variables[2]
                if ( self.variables[var2][0] == '%' ):
                    temp[:,2] *= 1e-2 * temp[:,1]
                elif ( self.variables[var2][0] == 'cm2' ):
                    temp[:,2] *= 1e-4
                if ( var2[-3:] == 'max' ):
                    temp[:,2] *= 1.0 / 3.0
            else:
                error = temp[:,1][...,None] * 0.5
                temp = np.append( temp, error, axis=1)
                dataset.error_provided = False

            self.datasets[dataType].data = np.copy(temp)

        return


# if __name__ == '__main__':
