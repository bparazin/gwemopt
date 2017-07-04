
import numpy as np
import gwemopt.utils

def read_coverage(params, telescope, filename):

    nside = params["nside"]
    config_struct = params["config"][telescope]

    lines = [line.rstrip('\n') for line in open(filename)]
    lines = lines[1:]
    lines = filter(None,lines)

    coverage_struct = {}
    coverage_struct["data"] = np.empty((0,4))
    coverage_struct["filters"] = []
    coverage_struct["ipix"] = []

    for line in lines:
        lineSplit = line.split(",")
        ra = float(lineSplit[2])
        dec = float(lineSplit[3])
        mjd = float(lineSplit[4])
        filt = lineSplit[6]
        mag = float(lineSplit[7])

        coverage_struct["data"] = np.append(coverage_struct["data"],np.array([[ra,dec,mjd,mag]]),axis=0)
        coverage_struct["filters"].append(filt)

        expPixels, radecs = gwemopt.utils.getExpPixels(ra, dec, config_struct["FOV_coverage"], nside)
        coverage_struct["ipix"].append(expPixels)

    coverage_struct["filters"] = np.array(coverage_struct["filters"])
    coverage_struct["FOV"] = config_struct["FOV_coverage"]*np.ones((len(coverage_struct["filters"]),))

    return coverage_struct

def read_files(params):

    coverage_structs = []
    for telescope, dataFile in zip(params["telescopes"],params["dataFiles"]):
        coverage_struct = read_coverage(params,telescope,dataFile)
        coverage_structs.append(coverage_struct)

    coverage_struct_combined = {}
    coverage_struct_combined["data"] = np.empty((0,4))
    coverage_struct_combined["filters"] = np.empty((0,1))
    coverage_struct_combined["ipix"] = []
    coverage_struct_combined["FOV"] = np.empty((0,1))
    for coverage_struct in coverage_structs:
        coverage_struct_combined["data"] = np.append(coverage_struct_combined["data"],coverage_struct["data"],axis=0)
        coverage_struct_combined["filters"] = np.append(coverage_struct_combined["filters"],coverage_struct["filters"])
        coverage_struct_combined["ipix"] = coverage_struct_combined["ipix"] + coverage_struct["ipix"]
        coverage_struct_combined["FOV"] = np.append(coverage_struct_combined["FOV"],coverage_struct["FOV"])

    return coverage_struct_combined

