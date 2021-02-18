""" This module contains mappings that should be passed to CategoricalMeasures taken directly from the isd-document.pdf.
"""

DATA_SOURCE_FLAG = {
    '1': """USAF SURFACE HOURLY observation, candidate for merge with NCEI SURFACE HOURLY (not yet merged,
element cross-checks)""", 
    '2': """NCEI SURFACE HOURLY observation, candidate for merge with USAF SURFACE HOURLY (not yet merged,
failed element cross-checks)""", 
    '3': """USAF SURFACE HOURLY/NCEI SURFACE HOURLY merged observation""", 
    '4': """USAF SURFACE HOURLY observation""", 
    '5': """NCEI SURFACE HOURLY observation""", 
    '6': 'ASOS/AWOS observation from NCEI', 
    '7': 'ASOS/AWOS observation merged with USAF SURFACE HOURLY observation', 
    '8': 'MAPSO observation (NCEI)',
    'A': """USAF SURFACE HOURLY/NCEI HOURLY PRECIPITATION merged observation, candidate for merge with
NCEI SURFACE HOURLY (not yet merged, failed element cross-checks)""", 
    'B': """NCEI SURFACE HOURLY/NCEI HOURLY PRECIPITATION merged observation, candidate for merge with
USAF SURFACE HOURLY (not yet merged, failed element cross-checks)""", 
    'C': """USAF SURFACE HOURLY/NCEI SURFACE HOURLY/NCEI HOURLY PRECIPITATION merged observation""",
    'D' : 'USAF SURFACE HOURLY/NCEI HOURLY PRECIPITATION merged observation',
    'E' : 'NCEI SURFACE HOURLY/NCEI HOURLY PRECIPITATION merged observation',
    'F' : 'Form OMR/1001 – Weather Bureau city office (keyed data)',
    'G' : 'SAO surface airways observation, pre-1949 (keyed data)',
    'H' : 'SAO surface airways observation, 1965-1981 format/period (keyed data)',  
    'I' : 'Climate Reference Network observation',
    'J' : 'Cooperative Network observation',
    'K' : 'Radiation Network observation',
    'L' : 'Data from Climate Data Modernization Program (CDMP) data source',
    'M' : 'Data from National Renewable Energy Laboratory (NREL) data source',
    'N' : 'NCAR / NCEI cooperative effort (various national datasets)',
    'O': """Summary observation created by NCEI using hourly observations that may not share the same data source flag.""",
    '9': 'Missing'
}


GEOPHYSICAL_REPORT_CODES = {
    'AERO' : 'Aerological report',
    'AUST' : 'Dataset from Australia',
    'AUTO' : 'Report from an automatic station',
    'BOGUS' : 'Bogus report',
    'BRAZ' : 'Dataset from Brazil',
    'COOPD' : 'US Cooperative Network summary of day report',
    'COOPS' : 'US Cooperative Network soil temperature report',
    'CRB' : 'Climate Reference Book data from CDMP',
    'CRN05': 'Climate Reference Network report, with 5-minute reporting interval',
    'CRN15': 'Climate Reference Network report, with 15-minute reporting interval',
    'FM-12': 'SYNOP Report of surface observation form a fixed land station',
    'FM-13': 'SHIP Report of surface observation from a sea station',
    'FM-14': 'SYNOP MOBIL Report of surface observation from a mobile land station',
    'FM-15': 'METAR Aviation routine weather report',
    'FM-16': 'SPECI Aviation selected special weather report',
    'FM-18': 'BUOY Report of a buoy observation',
    'GREEN': 'Dataset from Greenland',
    'MESOH': 'Hydrological observations from MESONET operated civilian or government agency',
    'MESOS': 'MESONET operated civilian or government agency',
    'MESOW': 'Snow observations from MESONET operated civilian or government agency',
    'MEXIC': 'Dataset from Mexico',
    'NSRDB':' National Solar Radiation Data Base',
    'PCP15': 'US 15-minute precipitation network report',
    'PCP60': 'US 60-minute precipitation network report',
    'S-S-A': 'Synoptic, airways, and auto merged report',
    'SA-AU': 'Airways and auto merged report',
    'SAO': 'Airways report (includes record specials)',
    'SAOSP': 'Airways special report (excluding record specials)',
    '6SHEF': 'Standard Hydrologic Exchange Format',
    'SMARS': 'Supplementary airways station report',
    'SOD': 'Summary of day report from U.S. ASOS or AWOS station',
    'SOM': 'Summary of month report from U.S. ASOS or AWOS station',
    'SURF': 'Surface Radiation Network report',
    'SY-AE': 'Synoptic and aero merged report',
    'SY-AU': 'Synoptic and auto merged report',
    'SY-MT': 'Synoptic and METAR merged report',
    'SY-SA': 'Synoptic and airways merged report',
    'WBO': 'Weather Bureau Office',
    'WNO': 'Washington Naval Observatory',
    '99999': 'Missing'
}

QUALITY_CONTROL_PROCESS = {
    'V010': 'No A or M Quality Control applied', 
    'V020': 'Automated Quality Control', 
    'V030': 'subjected to Quality Control'
}


NUMERICS = {
    '0': 'Passed gross limits check',
    '1': 'Passed all quality control checks',
    '2': 'Suspect',
    '3': 'Erroneous',
    '4':'Passed gross limits check, data originate from an NCEI data source',
    '5': 'Passed all quality control checks, data originate from an NCEI data source',
    '6': 'Suspect, data originate from an NCEI data source',
    '7': 'Erroneous, data originate from an NCEI data source',
    '9': 'Passed gross limits check if element is present',
    'A': 'Data value flagged as suspect, but accepted as a good value',
    'C': """Temperature and dew point received from Automated Weather Observing System (AWOS) are 
reported in whole degrees Celsius. Automated QC flags these values, but they are accepted as valid.""",
    'I': 'Data value not originally in data, but inserted by validator',
    'M': 'Manual changes made to value based on information provided by NWS or FAA',
    'P': 'Data value not originally flagged as suspect, but replaced by validator',
    'R': 'Data value replaced with value computed by NCEI software',
    'U': 'Data value replaced with edited value'
}

WIND_OBS_TYPE_CODE = {
    'A': 'Abridged Beaufort',
    'B': 'Beaufort',
    'C': 'Calm',
    'H': '5-Minute Average Speed',
    'N': 'Normal',
    'R': '60-Minute Average Speed',
    'Q': 'Squall',
    'T': '180 Minute Average Speed',
    'V': 'Variable',
    '9': 'Missing',
}

CEILING_DETERMINATION_CODE = {
    'A': 'Aircraft',
    'B': 'Balloon',
    'C': 'Statistically derived',
    'D': 'Persistent cirriform ceiling (pre-1950 data)',
    'E': 'Estimated',
    'M': 'Measured',
    'P': 'Precipitation ceiling (pre-1950 data)',
    'R': 'Radar',
    'S': 'ASOS augmented',
    'U': 'Unknown ceiling (pre-1950 data)',
    'V': 'Variable ceiling (pre-1950 data)',
    'W': 'Obscured',
    '9': 'Missing'
}


CAVOK_CODE = {
    'N': 'No', 
    'Y': 'Yes', 
    '9': 'Missing'
}

VARIABLITY_CODE = {
    'N': 'Not Variable', 
    'V': 'Variable', 
    '9': 'Missing'
}