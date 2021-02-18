import pytest 
import unittest 
from isdparser.measures import Measure, Position, NumericMeasure, CategoricalMeasure, Section

tc = unittest.TestCase()

def test_position(): 
    Position(1,2)
    with pytest.raises(ValueError):
        Position(2,1)


def test_measure():
    m = Measure('my_measure', Position(1,2), missing='99')

    assert m.name == 'my_measure'
    assert m.start == 0   # important that this returns the idx python needs for correct slice
    assert m.end == 2 
    
    m.set_value('42')
    tc.assertDictEqual({'my_measure': '42'}, m.schema())

    m.set_value('99')
    tc.assertDictEqual({'my_measure': None }, m.schema())


def test_numeric_measure(): 

    m = NumericMeasure('my_measure', Position(1,2), missing='-9999', scaling_factor=10, unit='my_unit')

    m.set_value('100')
    expected = {
        'measure': 'my_measure', 
        'value': 10, 
        'unit' : 'my_unit'
    }
    tc.assertDictEqual(expected, m.schema())

    m.set_value('-9999')

    expected = {
        'measure':'my_measure', 
        'value': None, 
        'unit': 'my_unit'
    }

    tc.assertDictEqual(expected, m.schema())


def test_categorical_measure():

    test_mapping = {
        '1': 'One', 
        '2': 'Two', 
        '9': 'Missing'
    } 
    m = CategoricalMeasure('my_measure', Position(1,2), test_mapping, missing='9')
    m.set_value('1')

    expected = {
        'measure': 'my_measure', 
        'value': '1', 
        'description': 'One'
    }

    tc.assertDictEqual(expected, m.schema())

    m.set_value('2')
    expected['value'] = '2'
    expected['description'] = 'Two'

    tc.assertDictEqual(expected, m.schema())

    m.set_value('9')
    expected['value'] = None 
    expected['description'] = 'Missing'

    tc.assertDictEqual(expected, m.schema())


def test_section(mocker): 

    mocker.patch.object(NumericMeasure, 'schema', 
        return_value={'measure': 'my_measure', 'value': 42, 'unit': 'my_unit'})

    mocker.patch.object(CategoricalMeasure, 'schema', 
        return_value={'measure': 'my_other_measure', 'value': '1', 'description': 'One'})


    def factory(): 
        return [
            NumericMeasure('my_measure', Position(1,2)), 
            CategoricalMeasure('my_other_measure', Position(3,4), mapping={})
        ]

    Section('my_section', factory()) # check list 
    s = Section('my_section', factory)  # check callable

    assert s.name == 'my_section'

    for m in s.measures():
        assert isinstance(m, Measure)
    
    expected = {
        'name': 'my_section', 
        'measures': [
            {'measure': 'my_measure', 'value': 42, 'unit': 'my_unit'}, 
            {'measure': 'my_other_measure', 'value': '1', 'description': 'One'}
        ]
    }

    tc.assertDictEqual(expected, s.schema())