import pytest 
import datetime 
import unittest 
tc = unittest.TestCase()

from isdparser.measures import Measure, Section
from isdparser.record import ISDRecord, ISDRecordFactory
import copy

def test_isdrecord(mocker): 

    mocker.patch.object(Section, 'schema', return_value={
        'data': 'goes here'
    })

    mocker.patch.object(Measure, 'schema', return_value={
        'more': 'data goes here'
    })

    sections = [Section('', [Measure('',None) for _ in range(3)]) for _ in range(3)]

    # mocker.patch.object(NumericMeasure, 'schema', 
    #     return_value={'measure': 'my_measure', 'value': 42, 'unit': 'my_unit'})


    d = datetime.datetime(2021,1,1,0,0)
    
    with pytest.raises(ValueError):
        ISDRecord(d, 'my-id', [])
    
    record = ISDRecord(d, 'my-id', sections)
    expected = {
        'datestamp': d, 
        'identifier': 'my-id', 
        'sections': [s.schema() for s in sections]
    }

    tc.assertDictEqual(expected, record.schema())


def test_isdrecordfactory_static_methods():

    fac = ISDRecordFactory((),())
    assert fac.parse_line('abcde', 3, 4) == 'd'

    assert fac.make_station_identifier('usaf', 'wban') == 'usaf-wban'

    assert fac.make_datestamp('20210101', '0115'), datetime.datetime(2021,1,1,1,15)



def test_isdrecordfactory_on_record_string(isd_record_strings_list):
    

    result = [ISDRecordFactory().create(line) for line in isd_record_strings_list]

    exp0 = {
        'datestamp': datetime.datetime(2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), 
        'identifier': '010230-99999', 
        'sections': [
            {
                'name': 'control', 
                'measures': [
                    {'measure': 'usaf', 'value':'010230'}, 
                    {'measure': 'wban', 'value': '99999'}, 
                    {'measure': 'date', 'value': '20200101'}, 
                    {'measure': 'time', 'value': '0000'}, 
                    {'measure': 'data_source_flag', 'value': '4', 'description': 'USAF SURFACE HOURLY observation'}, 
                    {'measure': 'latitude', 'value': 69.067, 'unit': 'angular_degrees'}, 
                    {'measure': 'longitude', 'value': 18.533, 'unit': 'angular_degrees'}, 
                    {'measure': 'code', 'value': 'FM-12', 'description': 'SYNOP Report of surface observation form a fixed land station'}, 
                    {'measure': 'elevation_dimension', 'value': 79.0, 'unit': 'meters'}, 
                    {'measure': 'call_letter_identifier', 'value': None}, 
                    {'measure': 'quality_control_process_name', 'value': 'V020', 'description': 'Automated Quality Control'}]}, 
            {
                'name': 'mandatory', 
                'measures': [
                    {'measure': 'wind_observation_direction_angle', 'value': 50.0, 'unit': 'angular_degrees'}, 
                    {'measure': 'wind_observation_direction_quality_code', 'value': '1', 'description': 'Passed all quality control checks'}, 
                    {'measure': 'wind_observation_type_code', 'value': 'N', 'description': 'Normal'}, 
                    {'measure': 'wind_observation_speed_rate', 'value': 1.0, 'unit': 'meters_per_second'}, 
                    {'measure': 'wind_observation_speed_quality_code', 'value': '1', 'description': 'Passed all quality control checks'}, 
                    {'measure': 'sky_condition_observation_ceiling_height_dimension', 'value': None, 'unit': 'meters'}, 
                    {'measure': 'sky_condition_observation_ceiling_quality_code', 'value': '9', 'description': 'Passed gross limits check if element is present'}, 
                    {'measure': 'sky_condition_observation_ceiling_determination_code', 'value': None, 'description': 'Missing'}, 
                    {'measure': 'sky_condition_observation_cavok_code', 'value': 'N', 'description': 'No'}, 
                    {'measure': 'visibility_observation_distance_dimension', 'value': None, 'unit': 'meters'}, 
                    {'measure': 'visibility_observation_distance_quality_code', 'value': '9', 'description': 'Passed gross limits check if element is present'}, 
                    {'measure': 'visibility_observation_variability_code', 'value': None, 'description': 'Missing'}, 
                    {'measure': 'visibility_observation_quality_variability_code', 'value': '9', 'description': 'Passed gross limits check if element is present'}, 
                    {'measure': 'air_temperature_observation_air_temperature', 'value': -2.9, 'unit': 'degrees_celsius'},
                    {'measure': 'air_temperature_observation_air_temperature_quality_code', 'value': '1', 'description': 'Passed all quality control checks'}, 
                    {'measure': 'air_temperature_observation_dew_point_temperature', 'value': -3.8, 'unit': 'degrees_celsius'}, 
                    {'measure': 'air_temperature_observation_dew_point_quality_code', 'value': '1', 'description': 'Passed all quality control checks'}, 
                    {'measure': 'atmospheric_pressure_observation_sea_level_pressure', 'value': 996.6, 'unit': 'hectopascals'}, 
                    {'measure': 'atmospheric_pressure_observation_sea_level_pressure_quality_code', 'value': '1', 'description': 'Passed all quality control checks'}
                ]
            }
        ]
    }

    exp1 = copy.deepcopy(exp0)
    exp1['datestamp'] = datetime.datetime(2020, 2, 1, 0, 0, tzinfo=datetime.timezone.utc)
    exp1['sections'][0]['measures'][2]['value'] = '20200201'

    exp2 = copy.deepcopy(exp0)
    exp2['datestamp'] = datetime.datetime(2020, 3, 1, 0, 0, tzinfo=datetime.timezone.utc)
    exp2['sections'][0]['measures'][2]['value'] = '20200301'

    expected = [exp0, exp1, exp2]

    for res in result:
        datestamp = res.schema()['datestamp']
        exp = list(filter(lambda x: x['datestamp'] == datestamp, expected))[0]
        tc.assertDictEqual(exp, res.schema())