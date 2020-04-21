from veroviz._common import *

from veroviz._queryORS import orsGetElevation
from veroviz._queryUSGS import usgsGetElevation
from veroviz._queryElevationapiio import elevapiGetElevation
# from veroviz._queryHere import hereGetElevation

def privGetElevationLocs(locs, dataProvider, dataProviderArgs):
	"""
	FIXME
	
	"""

	try:
		dataProvider = dataProvider.lower()
	except:
		pass

	# NOTE:  Neither mapquest, pgRouting, nor OSRM are supported.
	# FIXME -- None is not allowed    

	if (elevDataProviderDictionary[dataProvider] == 'ors-online'):
		locsWithAlt = orsGetElevation(locs, dataProviderArgs['APIkey'])
		return locsWithAlt
	elif (elevDataProviderDictionary[dataProvider] == 'usgs'):
		locsWithAlt = usgsGetElevation(locs)
		return locsWithAlt
	elif (elevDataProviderDictionary[dataProvider] == 'elevapi'):
		locsWithAlt = elevapiGetElevation(locs, dataProviderArgs['APIkey'])
		return locsWithAlt


def privGetElevationNodes(dataframe, dataProvider, dataProviderArgs):
	df = dataframe[dataframe['elevMeters'].isin([None])][['lat', 'lon']]
	indices = list(df.index)
	locs = list(map(list, zip(df.lat, df.lon)))

	locsWithAlt = privGetElevationLocs(locs, dataProvider, dataProviderArgs)

	if (len(locsWithAlt) != len(indices)):
		print("Error: Something went wrong with the request.  Sorry.")
	else:
		for i in range(0, len(indices)):
			dfIndex = indices[i]
			dataframe.loc[dfIndex, 'elevMeters'] = locsWithAlt[i][2]
			
	return dataframe
	
def privGetElevationArcsAsgn(dataframe, dataProvider, dataProviderArgs):

	# Start with starting location:
	df = dataframe[dataframe['startElevMeters'].isin([None])][['startLat', 'startLon']]
	indices = list(df.index)
	locs = list(map(list, zip(df.startLat, df.startLon)))

	locsWithAlt = privGetElevationLocs(locs, dataProvider, dataProviderArgs)

	if (len(locsWithAlt) != len(indices)):
		print("Error: Something went wrong with the request.  Sorry.")
	else:
		for i in range(0, len(indices)):
			dfIndex = indices[i]
			dataframe.loc[dfIndex, 'startElevMeters'] = locsWithAlt[i][2]

	# Repeat the process for ending location:
	df = dataframe[dataframe['endElevMeters'].isin([None])][['endLat', 'endLon']]
	indices = list(df.index)
	locs = list(map(list, zip(df.endLat, df.endLon)))

	locsWithAlt = privGetElevationLocs(locs, dataProvider, dataProviderArgs)

	if (len(locsWithAlt) != len(indices)):
		print("Error: Something went wrong with the request.  Sorry.")
	else:
		for i in range(0, len(indices)):
			dfIndex = indices[i]
			dataframe.loc[dfIndex, 'endElevMeters'] = locsWithAlt[i][2]

	return dataframe
