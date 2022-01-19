import numpy as np
from swarmData import swarmDatasets

order = ['READCOLLISIONS', 'CONDITIONS', 'RUN', 'SAVERESULTS']

AlAminLucas1987 = {'READCOLLISIONS': ['"test-crs.txt"', 'Ar', 1],
                   'CONDITIONS': ['VAR', 0., 0., 300., 300., 0., 0., 1.0E18, 1., 1., 1, 1, 1, 0., 200, 0, 200., 1.0e-10, 1.0e-4, 1000, 1.0, 1],
                   'RUN': [56.5, 84.8, 113, 141, 198, 254, 424, 565, 678, 848, 1130, 1413, 1695, 1978, 2260, 2825, 3390, 4238, 5650],
                   'SAVERESULTS': ['"output-AlAminLucas1987.dat"', 3, 1, 1, 0, 0, 0, 0, 0]
                   }
MilloyCrompton1977 = {'READCOLLISIONS': ['"test-crs.txt"', 'Ar', 1],
                      'CONDITIONS': ['VAR', 0., 0., 294., 294., 0., 0., 1.0E18, 1., 1., 1, 1, 1, 0., 200, 0, 200., 1.0e-10, 1.0e-4, 1000, 1.0, 1],
                      'RUN': [0.0010, 0.0012, 0.0014, 0.0017, 0.0020, 0.0025, 0.0030, 0.0035, 0.0040, 0.0050, 0.0060, 0.0080, 0.010, 0.012, 0.014, 0.017, 0.020, 0.025, 0.030, 0.035, 0.040, 0.050, 0.060, 0.080, 0.100],
                      'SAVERESULTS': ['"output-MilloyCrompton1977.dat"', 3, 1, 1, 0, 0, 0, 0, 0]
                      }
NakamuraKurachi1988 = {'READCOLLISIONS': ['"test-crs.txt"', 'Ar', 1],
                       'CONDITIONS': ['VAR', 0., 0., 300., 300., 0., 0., 1.0E18, 1., 1., 1, 1, 4, 0., 200, 0, 200., 1.0e-10, 1.0e-4, 1000, 1.0, 1],
                       'RUN': [0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.4, 1.7, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 14.0, 17.0, 20.0, 25.0, 30.0, 35.0, 40.0, 50.0],
                       'SAVERESULTS': ['"output-NakamuraKurachi1988.dat"', 3, 1, 1, 0, 0, 0, 0, 0]
                       }
expConfigs = {'AlAminLucas1987': AlAminLucas1987,
              'MilloyCrompton1977': MilloyCrompton1977,
              'NakamuraKurachi1988': NakamuraKurachi1988}

def writeInputFile(inputFilename, expConfig, crsFile=None, outputFile=None, noscreen = True):
    content = ''
    if (not noscreen): content += '/'
    content += 'NOSCREEN\n\n'

    for key in order:
        if ( (key == 'READCOLLISIONS') and (crsFile is not None) ):
            crsFile = '"' + crsFile + '"'
            expConfig[key][0] = crsFile
        elif ( (key == 'SAVERESULTS') and (outputFile is not None) ):
            outputFile = '"' + outputFile + '"'
            expConfig[key][0] = outputFile

        content += key + '\n'
        for val in expConfig[key]:
            content += str(val) + '\n'
        content += '\n'

    fID = open(inputFilename,'w')
    fID.write(content)
    fID.close()

    return
