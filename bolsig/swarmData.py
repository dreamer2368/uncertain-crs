import numpy as np

MaxPoints = 1000
kB, Td = 1.38064852e-23, 1.0e21

# datasets
swarmDatasets = ["AlAminLucas1987","MilloyCrompton1977","NakamuraKurachi1988"]

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
    variables = {}
    Nvar = 0
    parameters = {}

    def __init__(self):
        self.parameters = {}
        self.variables = {}

    # def printToScreen(self):
    #     print("{0:s}\t{1:s}".format(self.inputName,self.outputName))
    #     for k in range(self.data.shape[0]):
    #         print("{0:.6e}\t{1:.6e}".format(self.data[k,0], self.data[k,1]))
    #     print('\n')

class swarmData:
    datasets = []
    Ndatasets = 0
    variables = {}

    def __init__(self, filename):
        """Initialize by reading BOLSIG output file."""
        self.ref = ''
        self.datasets = []
        self.Ndatasets = 0
        self.variables = {}
        self.parseData(filename)
        self.ConvertData()

    def parseData(self, filename):
        """Read swarm data files."""

        with open(filename,'r') as fp:

            Ndata = 0

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
                    self.datasets.append(singleData())

                    tmp = fp.readline().strip()
                    if ( tmp[0] == '#' ):
                        # read parameter values. Not implemented at this point.
                        tmp = fp.readline().strip()
                        while ( tmp[0] != '#' ):
                            left, right = tmp.split()
                            self.datasets[Ndata].parameters[left] = right
                            tmp = fp.readline().strip()

                    variables = fp.readline().strip().split()
                    Nvar = len(variables)
                    tempData = np.zeros([MaxPoints,Nvar])
                    pt = 0
                    # self.datasets[Ndata].variables = fp.readline().strip().split()
                    # self.datasets[Ndata].Nvar = len(self.datasets[Ndata].variables)
                    tmp = fp.readline().strip()
                    if ( tmp[0] == '=' ):
                        tmp = fp.readline().strip()
                        while (tmp[0].isdigit() and not (tmp=='')):
                            d = tmp.split()
                            tempData[pt,:] = np.array([readNumber(d[k]) for k in range(Nvar)])
                            pt += 1
                            tmp = fp.readline().strip()
                    self.datasets[Ndata].Nvar = Nvar
                    for k in range(Nvar):
                        self.datasets[Ndata].variables.update({variables[k]: tempData[:pt,k]})
                        # d = tmp.split()
                        # self.datasets[Ndata].data = [[readNumber(d[k]) for k in range(self.datasets[Ndata].Nvar)]]
                        # tmp = fp.readline().strip()
                        # while (tmp[0].isdigit() and not (tmp=='')):
                        #     d = tmp.split()
                        #     self.datasets[Ndata].data = np.append(self.datasets[Ndata].data, [[readNumber(d[k]) for k in range(self.datasets[Ndata].Nvar)]], axis=0)
                        #     tmp = fp.readline().strip()

                    Ndata += 1

                line = fp.readline()

            self.Ndatasets = Ndata
            # for c in self.outputs:
            #     self.outputs[c].printToScreen()
        return

    def ConvertData(self):

        for dataset in self.datasets:
            for var in list(dataset.variables):
                if ( (var[-4:] == '-rms') or (var[-4:] == '-max') ): continue

                if ( (var == 'E/N') and (not (self.variables[var][0] == 'Td')) ):
                    if (self.variables[var][0] == 'Vcm2'):
                        dataset.variables[var] *= 1.0e-4 * Td
                elif ( var == 'E/p' ):
                    if (self.variables[var][0] == 'V/cm/mmHg'):
                        temperature = readNumber(dataset.parameters['T'])
                        dataset.variables[var] *= 100. / 133.322 * kB * temperature * Td
                elif ( var == 'W' ):
                    if (self.variables[var][0] == 'cm/s'):
                        dataset.variables[var] *= 1.0e-2

                    if (self.variables[var][1] != 'n/a'):
                        error = dataset.variables[var] * 1e-2 * readNumber(self.variables[var][1][:-1])
                        dataset.variables.update({var+'-rms': error})
                    elif (self.variables[var][2] != 'n/a'):
                        error = dataset.variables[var] * 1e-2 / 3.0 * readNumber(self.variables[var][2][:-1])
                        dataset.variables.update({var+'-rms': error})
                    else:
                        if (var+'-rms') in dataset.variables:
                            if ( self.variables[var+'-rms'][0] == '%' ):
                                dataset.variables[var+'-rms'] *= 1e-2 * dataset.variables[var]
                        elif (var+'-max') in dataset.variables:
                            if ( self.variables[var+'-max'][0] == '%' ):
                                dataset.variables[var+'-max'] *= 1e-2 / 3.0 * dataset.variables[var]
                                dataset.variables[var+'-rms'] = dataset.variables.pop(var+'-max')
                elif ( var == 'DLN' ):
                    if (self.variables[var][0] == '1/cm/s'):
                        dataset.variables[var] *= 1.0e2

                    if (self.variables[var][1] != 'n/a'):
                        error = dataset.variables[var] * 1e-2 * readNumber(self.variables[var][1][:-1])
                        dataset.variables.update({var+'-rms': error})
                    elif (self.variables[var][2] != 'n/a'):
                        error = dataset.variables[var] * 1e-2 / 3.0 * readNumber(self.variables[var][2][:-1])
                        dataset.variables.update({var+'-rms': error})
                    else:
                        if (var+'-rms') in dataset.variables:
                            if ( self.variables[var+'-rms'][0] == '%' ):
                                dataset.variables[var+'-rms'] *= 1e-2 * dataset.variables[var]
                        elif (var+'-max') in dataset.variables:
                            if ( self.variables[var+'-max'][0] == '%' ):
                                dataset.variables[var+'-max'] *= 1e-2 / 3.0 * dataset.variables[var]
                                dataset.variables[var+'-rms'] = dataset.variables.pop(var+'-max')
                elif ( var == 'DT/mu' ):
                    # if (self.variables[var][0] == '1/cm/s'):
                    #     dataset.variables[var] *= 1.0e2

                    if (self.variables[var][1] != 'n/a'):
                        error = dataset.variables[var] * 1e-2 * readNumber(self.variables[var][1][:-1])
                        dataset.variables.update({var+'-rms': error})
                    elif (self.variables[var][2] != 'n/a'):
                        error = dataset.variables[var] * 1e-2 / 3.0 * readNumber(self.variables[var][2][:-1])
                        dataset.variables.update({var+'-rms': error})
                    else:
                        if (var+'-rms') in dataset.variables:
                            if ( self.variables[var+'-rms'][0] == '%' ):
                                dataset.variables[var+'-rms'] *= 1e-2 * dataset.variables[var]
                        elif (var+'-max') in dataset.variables:
                            if ( self.variables[var+'-max'][0] == '%' ):
                                dataset.variables[var+'-max'] *= 1e-2 / 3.0 * dataset.variables[var]
                                dataset.variables[var+'-rms'] = dataset.variables.pop(var+'-max')

        return

# if __name__ == '__main__':
