## isdparser 
[![CI](https://github.com/bsnacks000/isdparser/actions/workflows/CI.yaml/badge.svg)](https://github.com/bsnacks000/isdparser/actions/workflows/CI.yaml)


A utility package to help parse noaa isd files from `ftp://ftp.ncdc.noaa.gov/pub/data/noaa`

Turns this:
```
0130010230999992020010100004+69067+018533FM-12+007999999V0200501N001019999999N999999999-00291-00381099661
```

Into this:
```python
{'datestamp': datetime.datetime(2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
  'identifier': '010230-99999',
  'sections': [{'measures': [{'usaf': '010230'},
                             {'wban': '99999'},
                             {'date': '20200101'},
                             {'time': '0000'},
                             {'description': 'USAF SURFACE HOURLY observation',
                              'measure': 'data_source_flag',
                              'value': '4'},
                             {'measure': 'latitude',
                              'unit': 'angular_degrees',
                              'value': 69.067},
                             {'measure': 'longitude',
                              'unit': 'angular_degrees',
                              'value': 18.533},
                             {'description': 'SYNOP Report of surface '
                                             'observation form a fixed land '
                                             'station',
                              'measure': 'code',
                              'value': 'FM-12'},
                             {'measure': 'elevation_dimension',
                              'unit': 'meters',
                              'value': 79.0},
                             {'call_letter_identifier': None},
                             {'description': 'Automated Quality Control',
                              'measure': 'quality_control_process_name',
                              'value': 'V020'}],
                'name': 'control'},
               {'measures': [{'measure': 'wind_observation_direction_angle',
                              'unit': 'angular_degrees',
                              'value': 50.0},
                             {'description': 'Passed all quality control '
                                             'checks',
                              'measure': 'wind_observation_direction_quality_code',
                              'value': '1'},
                             {'description': 'Normal',
                              'measure': 'wind_observation_type_code',
                              'value': 'N'},
                             {'measure': 'wind_observation_speed_rate',
                              'unit': 'meters_per_second',
                              'value': 1.0},
                             {'description': 'Passed all quality control '
                                             'checks',
                              'measure': 'wind_observation_speed_quality_code',
                              'value': '1'},
                             {'measure': 'sky_condition_observation_ceiling_height_dimension',
                              'unit': 'meters',
                              'value': None},
                             {'description': 'Passed gross limits check if '
                                             'element is present',
                              'measure': 'sky_condition_observation_ceiling_quality_code',
                              'value': '9'},
                             {'description': 'Missing',
                              'measure': 'sky_condition_observation_ceiling_determination_code',
                              'value': '9'},
                             {'description': 'No',
                              'measure': 'sky_condition_observation_cavok_code',
                              'value': 'N'},
                             {'measure': 'visibility_observation_distance_dimension',
                              'unit': 'meters',
                              'value': None},
                             {'description': 'Passed gross limits check if '
                                             'element is present',
                              'measure': 'visibility_observation_distance_quality_code',
                              'value': '9'},
                             {'description': 'Missing',
                              'measure': 'visibility_observation_variability_code',
                              'value': '9'},
                             {'description': 'Passed gross limits check if '
                                             'element is present',
                              'measure': 'visibility_observation_quality_variability_code',
                              'value': '9'},
                             {'measure': 'air_temperature_observation_air_temperature',
                              'unit': 'degrees_celsius',
                              'value': -2.9},
                             {'description': 'Passed all quality control '
                                             'checks',
                              'measure': 'air_temperature_observation_air_temperature_quality_code',
                              'value': '1'},
                             {'measure': 'air_temperature_observation_dew_point_temperature',
                              'unit': 'degrees_celsius',
                              'value': -3.8},
                             {'description': 'Passed all quality control '
                                             'checks',
                              'measure': 'air_temperature_observation_dew_point_quality_code',
                              'value': '1'},
                             {'measure': 'atmospheric_pressure_observation_sea_level_pressure',
                              'unit': 'hectopascals',
                              'value': 996.6},
                             {'description': 'Passed all quality control '
                                             'checks',
                              'measure': 'atmospheric_pressure_observation_sea_level_pressure_quality_code',
                              'value': '1'}],
                'name': 'mandatory'}]},
```


### Notes 

The current version parses only the `control` and `mandatory` data sections of the isd record-string. The `additional` data section is extremely inconsistent between records and would require alot of work to properly map in a sane way.

The above schema was constructed with mongo in mind so feel free to fork and modify to your needs. Any changes or additions to the above schema will incur a minor version bump (see below for install).

Missing data for numerical measures are represented as `None` in the python schema. This should map to a database better then symbols like `-7777` or `+999999` which are used in the strings. 

All numerical data is also "scaled" and appropriately signed by the provided `scaling_factor` from the pdf.

I've included a `data-dictionary.md` and a copy of the isd documentation I used to write the parsers in the `extras` folder.

### Install 

For now install from here with pip. The master branch will contain the most up to date version.   
```
pip install git+https://github.com/bsnacks000/isdparser.git
```
or a specific version 
```
pip install git+https://github.com/bsnacks000/isdparser.git@v0.1.0
```

### Usage 


If you want to parse an isd with the default configuration which includes the mappings I created and all points from the `control` and `data` sections, then it is very simple. 

```python
from isdparser import ISDRecordFactory 

# assumes you downloaded a file but could also be a direct to ftp connection.
with open('010230-99999-2020.txt', 'r') as f:
    lines = f.readlines()

# create a list of record objects
records = [ISDRecordFactory().create(line) for line in lines]    

# build the schema 
schema = [r.schema() for r in records]

# do things...
```
This will produce the schema documented above. It can can serialized directly to json, offloaded to mongo or easily flattened and uploaded to a sql database. 

One caveat for using the high level factory is that it will make a root level key by looking up certain values in the control section. This is a convenience and assumes you want to have some easy to manage data integrity based on the usaf, wban and datestamp. These three fields will need to be given in the control section. If for some reason you don't want this behavior I recommend not using the high level factory and creating your own high level schema.

If you want to modify the API to parse less data then simply create new lists of `control` and `mandatory` measures and give these along with names to the `ISDRecordFactory`. You can do this either using a callable or explicitly with lists of Measures. 