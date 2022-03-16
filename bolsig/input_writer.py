import numpy as np
from swarmData import swarmDatasets

order = ['READCOLLISIONS', 'CONDITIONS', 'RUN', 'RUNSERIES', 'SAVERESULTS']

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

transport300K = {'READCOLLISIONS': ['"test-crs.txt"', 'Ar', 1],
                 'CONDITIONS': [10., 0., 0., 300., 300., 0., 0., 1.0E18, 1., 1., 1, 1, 4, 0., 200, 0, 200., 1.0e-10, 1.0e-4, 1000, 1.0, 1],
                 'RUNSERIES': [1, 1.0e-4, 2000., 110, 3],
                 'SAVERESULTS': ['"transport.300K.dat"', 3, 1, 1, 0, 0, 0, 0, 0]
                 }

transport77K = {'READCOLLISIONS': ['"test-crs.txt"', 'Ar', 1],
                 'CONDITIONS': [10., 0., 0., 77., 77., 0., 0., 1.0E18, 1., 1., 1, 1, 4, 0., 200, 0, 200., 1.0e-10, 1.0e-4, 1000, 1.0, 1],
                 'RUNSERIES': [1, 1.0e-4, 1.0e-2, 30, 3],
                 'SAVERESULTS': ['"transport.300K.dat"', 3, 1, 1, 0, 0, 0, 0, 0]
                 }

transport90K = {'READCOLLISIONS': ['"test-crs.txt"', 'Ar', 1],
                 'CONDITIONS': [10., 0., 0., 90., 90., 0., 0., 1.0E18, 1., 1., 1, 1, 4, 0., 200, 0, 200., 1.0e-10, 1.0e-4, 1000, 1.0, 1],
                 'RUNSERIES': [1, 1.0e-4, 1.0e-1, 40, 3],
                 'SAVERESULTS': ['"transport.300K.dat"', 3, 1, 1, 0, 0, 0, 0, 0]
                 }

rate300K = {'READCOLLISIONS': ['"test-crs.txt"', 'Ar', 1],
             'CONDITIONS': [10., 0., 0., 300., 300., 0., 0., 1.0E18, 1., 1., 1, 1, 1, 0., 200, 0, 200., 1.0e-10, 1.0e-4, 1000, 1.0, 1],
             'RUNSERIES': [1, 1.0e0, 5.0e3, 50, 3],
             'SAVERESULTS': ['"transport.300K.dat"', 3, 1, 1, 1, 0, 0, 0, 0]
             }
rate273K = {'READCOLLISIONS': ['"test-crs.txt"', 'Ar', 1],
             'CONDITIONS': [10., 0., 0., 273.15, 273.15, 0., 0., 1.0E18, 1., 1., 1, 1, 1, 0., 200, 0, 200., 1.0e-10, 1.0e-4, 1000, 1.0, 1],
             'RUNSERIES': [1, 1.0e0, 5.0e3, 50, 3],
             'SAVERESULTS': ['"transport.300K.dat"', 3, 1, 1, 1, 0, 0, 0, 0]
             }
rate273K = {'READCOLLISIONS': ['"test-crs.txt"', 'Ar', 1],
             'CONDITIONS': [10., 0., 0., 273.15, 273.15, 0., 0., 1.0E18, 1., 1., 1, 1, 4, 0., 200, 0, 200., 1.0e-10, 1.0e-4, 1000, 1.0, 1],
             'RUNSERIES': [1, 1.0e0, 5.0e3, 50, 3],
             'SAVERESULTS': ['"transport.300K.dat"', 3, 1, 1, 1, 0, 0, 0, 0]
             }

reaction300K = {'READCOLLISIONS': ['"test-crs.txt"', 'Ar', 1],
             'CONDITIONS': [0., 0., 0., 300., 300., 0., 0., 1.0E18, 1., 1., 1, 1, 2, 0., 200, 0, 200., 1.0e-10, 1.0e-4, 1000, 1.0, 1],
             'RUNSERIES': [2, 5.0e-2, 50., 200, 1],
             'SAVERESULTS': ['"reaction_rate.300K.dat"', 3, 1, 1, 1, 0, 0, 0, 0]
             }

expConfigs = {'AlAminLucas1987': AlAminLucas1987,
              'MilloyCrompton1977': MilloyCrompton1977,
              'NakamuraKurachi1988': NakamuraKurachi1988}

lxcatConfigs = {'transport300K': transport300K,
                'transport77K': transport77K,
                'transport90K': transport90K,
                'rate300K': rate300K,
                'rate273K': rate273K}

glowDischargeConfigs = {'reaction300K': reaction300K}


def writeInputFile(inputFilename, expConfig, crsFile=None, outputFile=None, noscreen = True):
    content = ''
    if (not noscreen): content += '/'
    content += 'NOSCREEN\n\n'

    for key in order:
        if key not in expConfig: continue

        if ( (key == 'READCOLLISIONS') and (crsFile is not None) ):
            crsFile = '"' + crsFile + '"'
            expConfig[key][0] = crsFile
        elif ( (key == 'SAVERESULTS') and (outputFile is not None) ):
            outputFile = '"' + outputFile + '"'
            expConfig[key][0] = outputFile

        content += key + '\n'
        if (key == 'RUNSERIES'):
            temp = expConfig[key]
            content += str(temp[0]) + '\n'
            content += '%f  %f\n' % (temp[1], temp[2])
            content += str(temp[3]) + '\n'
            content += str(temp[4]) + '\n'
        else:
            for val in expConfig[key]:
                content += str(val) + '\n'
        content += '\n'

    fID = open(inputFilename,'w')
    fID.write(content)
    fID.close()

    return
