import numpy as np

typeDictS2I = {"Electric field / N (Td)":               0,
               "Grid type":                             1,
               "Maximum energy":                        2,
               "Mean energy (eV)":                      3,
               "Mobility *N (1/m/V/s)":                 4,
               "Diffusion coefficient *N (1/m/s)":      5,
               "Energy mobility *N (1/m/V/s)":          6,
               "Energy diffusion coef. D*N (1/m/s)":    7,
               "Total collision freq. /N (m3/s)":       8,
               "Momentum frequency /N (m3/s)":          9,
               "Total ionization freq. /N (m3/s)":      10,
               "Townsend ioniz. coef. alpha/N (m2)":    11,
               "Power /N (eV m3/s)":                    12,
               "Elastic power loss /N (eV m3/s)":       13,
               "Inelastic power loss /N (eV m3/s)":     14,
               "Growth power /N (eV m3/s)":             15,
               "# of iterations":                       16,
               "# of grid trials":                      17 }
typeDictI2S = {0: "Electric field / N (Td)",
               1: "Grid type",
               2: "Maximum energy",
               3: "Mean energy (eV)",
               4: "Mobility *N (1/m/V/s)",
               5: "Diffusion coefficient *N (1/m/s)",
               6: "Energy mobility *N (1/m/V/s)",
               7: "Energy diffusion coef. D*N (1/m/s)",
               8: "Total collision freq. /N (m3/s)",
               8: "Momentum frequency /N (m3/s)",
               10: "Total ionization freq. /N (m3/s)",
               11: "Townsend ioniz. coef. alpha/N (m2)",
               12: "Power /N (eV m3/s)",
               13: "Elastic power loss /N (eV m3/s)",
               14: "Inelastic power loss /N (eV m3/s)",
               15: "Growth power /N (eV m3/s)",
               16: "# of iterations",
               17: "# of grid trials" }

class singleOutput:
    data = np.zeros((1,2))
    inputName = ''
    outputName = ''

    def printToScreen(self):
        print("{0:s}\t{1:s}".format(self.inputName,self.outputName))
        for k in range(self.data.shape[0]):
            print("{0:.6e}\t{1:.6e}".format(self.data[k,0], self.data[k,1]))
        print('\n')

class bolsigOutput:
    options = {}
    outputs = {}

    def __init__(self, filename):
        """Initialize by reading BOLSIG output file."""
        self.options = {}
        self.outputs = {}
        self.parseOutputFile(filename)

    def parseOutputFile(self, filename):
        """Read output file of BOLSIG."""

        with open(filename,'r') as fp:

            line = fp.readline().strip()
            # Skip the BOLSIG version and collision input data.
            while (not (line=='') and line[0] != ' '):
                print(line)
                line = fp.readline().strip()

            # Read until we find condition table.
            while (line == ''):
                line = fp.readline().strip()

            # Read conditions and store them in dictionaries. Omit this functionality for now.
            while (not (line=='') and line[0] != ' '):
                print(line)
                line = fp.readline().strip()

            # Read tables one by one.
            nOutputs = 0
            line = fp.readline()
            while (line != ''):
                if (line.strip() != ''):

                    # Read table. Split by tab.
                    left, right = line.split('\t')
                    dataType = typeDictS2I[right.strip()]
                    if dataType in self.outputs:
                        print("Warning: output '%s' already exists and will be overwritten." % typeDictI2S[dataType])
                    self.outputs.update({dataType: singleOutput()})
                    # self.outputs.append(singleOutput())
                    self.outputs[dataType].inputName = left.strip()
                    self.outputs[dataType].outputName = right.strip()
                    # Once we find numbers, read until we don't find a number
                    tmp = fp.readline().strip()
                    while (not (tmp=='') and tmp[0].isdigit()):
                        d = tmp.split()
                        self.outputs[dataType].data = \
                            np.append(self.outputs[dataType].data,
                                      [[np.double(d[0]), np.double(d[1])]], axis=0)
                        tmp = fp.readline().strip()

                    self.outputs[dataType].printToScreen
                    nOutputs += 1

                line = fp.readline()

            for c in self.outputs:
                self.outputs[c].printToScreen()
        return


if __name__ == '__main__':
    tmp = bolsigOutput('Biagi-transport.dat')
    np.savetxt('Biagi.muN.raw.txt',tmp.outputs[4].data, fmt='%1.15e')
