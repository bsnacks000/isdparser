## isdparser 

The goal is to try to model the isd file format so that one can create some kind of data warehouse that is human/API-friendly. The 1 line string should be broken down into individual sections. This is not trivial since other then Control and Mandatatory Data sections there is a ton of missing/optional data as well as missing values within listed points.


-----------
objects:
* Measure 
* Section composed of multiple measures 


cli application:
* Create a registry of Sections/Measures and allow an interface to select which measures to track 
* Wrap an ftp client to pull data harmoniously for a given isd file (providing station_id start-end date and list of measures) 

api:
* mongo database: collection for tracked station / metadata and collection for the isd data 
* REST API with a single list view for fetching data by station, start and end date
* data loader that uses the cli application to pull data and update the backend


Below are each Section. This is taken from `ftp://ftp.ncdc.noaa.gov/pub/data/noaa/isd-format-document.pdf`. More details for each field can be found there.

Each file on the ftp for a station is broken down by year and contains a text file. Each `\n` denotes a record with identifiers for different sections.

Example file: `ftp://ftp.ncdc.noaa.gov/pub/data/noaa/2021/010010-99999-2021.gz`

----------------

Control Data Section - The beginning of each record provides information
about the report including date, time, and station location information. Data
fields will be in positions identified in the applicable data definition.
control data section is fixed length and is 60 characters long.

identifier `None`

fields:
* total-variable character (NOT USING)
* usaf id (str) 
* wban  (numeric)
* date (numeric - iso format -> YYYY-mm-dd) 
* time (numeric - HHMM, based on UTC) 
* data source flag (categorical) 
* latitude (numeric) 
* longitude (numeric) 
* code (categorical) 
* elevation (numeric) 
* call-letter-identifier (str) 
* quality-control-process (categorical) 

NOTES: this is the basic metadata for a record. The usaf-wban could be combined along with the datestamp and set at the top level of the object as a unique constraint.
--------- 

Mandatory Data Section - The mandatory data section contains meteorological
information on the basic elements such as winds, visibility, and temperature.
These are the most commonly reported parameters and are available most of the
time. The mandatory data section is fixed length and is 45 characters long.

identifier: `None` 

fields:
* wind-observation-direction-angle (numeric) 
* wind-observation-direction-quality-code (categorical) 
* wind-observation-type-code (categorical) 
* wind-observation-speed-rate (numeric) 
* wind-observation-speed-quality-code (categorical) 
* sky-condition-observation-ceiling-height-dimension (numeric) 
* sky-condition-observation-ceiling-quality-code (categorical) 
* sky-condition-observation-cavok-code (categorical) 
* visibility-observation-distance-dimension (numeric)
* visibility-observation-distance-quality-code (categorical)
* visibility-observation-variability-code (categorical)
* visibility-observation-variability-quality-code (categorical)
* air-temperature-observation-air-temperature (numeric) 
* air-temperature-observation-air-temperature-quality-code (categorical) 
* air-temperature-observation-dew-point-temperature (numeric) 
* air-temperature-observation-dew-point-quality-code (categorical)
* atmospheric-pressure-observation-sea-level-pressure (numeric)
* atmospheric-pressure-observation-sea-level-pressure-quality-code (categorical)


_NOTES_: This is the core measurement data seems to be fairly consistent across files. 

--------

Additional Data Section - Variable length data are provided after the
mandatory data. These additional data contain information of significance
and/or which are received with varying degrees of frequency. Identifiers are
used to note when data are present in the record. If all data fields in a
group are missing, the entire group is usually not reported. If no groups are
reported the section will be omitted. The additional data section is variable
in length with a minimum of 0 characters and a maximum of 637 (634 characters
plus a 3 character section identifier) characters.
Note: Specific information (where applicable) pertaining to each variable
group of data elements is provided in the data item definition.

identifier: `ADD`
reference starts: `page 13`

_NOTES_: ---- NOT USING in v0.x .. too inconsistent to try to parse

----------

Remarks Data - The numeric and character (plain language) remarks are
provided if they exist. The data will vary in length and are identified in
the applicable data definition. The remarks section has a maximum length of
515 (512 characters plus a 3 character section identifier) characters.

identifier: `REMARKS` 
reference starts: `page 127`

_NOTES_: ---- NOT USING in v0.x .. too inconsistent to try to parse

----------

Element Quality Data Section - The element quality data section contains
information on data that have been determined erroneous or suspect during
quality control procedures. Also, some of the original data source codes and
flags are stored here. This section is variable in length and contains 16
characters for each erroneous or suspect parameter. The section has a minimum
length of 0 characters and a maximum length of 1587 (1584 plus a 3 character
section identifier) characters.

identifier: `EQD` 
reference starts: `page 129`

NOTES ---- NOT USING in v0.x .. too inconsistent to try to parse
