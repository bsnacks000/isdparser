
from . import mappings 
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union


class Position(object): 
    __slots__ = ('start', 'end')
    
    def __init__(self, start: int, end: int) -> None:
        """Container object for the position in the isd file. This should 
        be the exact position as found in the documentation.

        Args:
            start (int): start pos
            end (int): end pos
        Raises:
            ValueError: If start date is greater then end.
        """
        if start > end: 
            raise ValueError("`start` cannot be `greater` then end.")
        self.start = start
        self.end = end


class Measure(object):
    __slots__ = ('_name', '_position', '_missing', '_value')
    
    def __init__(self, name: str, position: Position, missing: Optional[str]=None) -> None:
        """A basic measure found in the isd string, represented as 

        Args:
            name (str): The name of the measure
            position (Position): A position object.
            missing (str, optional): If provided, the value represented as missing.
                Often something like `9999`. Defaults to None.
        """
        self._name = name 
        self._position = position # easier to map  
        self._missing = missing 
        self._value = None
        
    @property 
    def name(self) -> str:
        """Get the name of the Measure

        Returns:
            str: The name of the Measure
        """
        return self._name
    
    @property 
    def start(self) -> int:
        """Retrieve the start from the underlying position. Subtracts 1 from this
        value to give the python list position for a slice.

        Returns:
            int: Provided start position - 1
        """
        return self._position.start - 1 

    @property 
    def end(self) -> int:
        """Retrieve end from the underlying position.

        Returns:
            int: [description]
        """
        return self._position.end
    
    def schema(self) -> Dict[str, Any]:
        """Return the schema as a dictionary mapped name : value

        Returns:
            Dict[str, Any]: A dictionary mapped name value.
        """
        if self._missing is not None and self._value == self._missing:
            val = None
        else:
            val = self._value
        return { 'measure': self._name, 'value': val }
    

    def set_value(self, value: str) -> "Measure":
        """Set the value of the string on the Measure instance returning self.

        Returns:
            Measure: the instance.
        """
        self._value = value.strip() if type(value) is str else value
        return self


class NumericMeasure(Measure):
    
    __slots__ = ('_name', '_position', '_missing', '_value', '_scaling_factor', '_unit')
    
    def __init__(self, 
        name: str, 
        position: Position, 
        missing: Optional[str]=None, 
        scaling_factor: int=1, 
        unit: str='') -> None:
        """Describes a Numeric measure from the isd documentation

        Args:
            name (str): The name of the measure
            position (Position): Measure position
            missing (Optional[str], optional): The repr of a missing value if provided. Defaults to None.
            scaling_factor (int, optional): The scaling factor used to create a float. Defaults to 1.
            unit (str, optional): The unit of measure. Defaults to ''.
        """
        super().__init__(name, position, missing)
        self._scaling_factor = scaling_factor
        self._unit = unit
        
    def schema(self) -> Dict[str, Any]:
        """Return the schema as a dictionary, calculating any values from the string value.

        Returns:
            Dict[str, Any]: Resulting schema mapped measure: name, value: val and unit: unit
        """
        if self._missing is not None and self._value == self._missing: 
            val = None 
        else:
            val = float(self._value) / self._scaling_factor 
        return {
            'measure': self._name, 
            'value': val,
            'unit': self._unit
        }
    

class CategoricalMeasure(Measure): 
    __slots__ = ('_name', '_position', '_missing', '_value', '_mapping')
    
    def __init__(self, 
        name: str, 
        position: Position, 
        mapping: Dict[str, str], 
        missing: Optional[str]=None) -> None:
        """ A CategoricalMeasure. A dictionary mapping values to descriptions must be provided based on the isd docs.

        Args:
            name (str): The name of the measure.
            position (Position): The position of the measure.
            mapping (Dict[str, str]): A dict mapping the encoded value to a description.
            missing (Optional[str], optional): The repr of a missing value if provided. Defaults to None.. Defaults to None.
        """
        super().__init__(name, position, missing)
        self._mapping = mapping 
    
    def schema(self) -> Dict[str, Any]:
        """ Returns the schema as a dictionary. A description maps the repr value to text.

        Returns:
            Dict[str, Any]: Resulting schema mapped meaure : name, value : val, description : text
        """
        if self._missing is not None and self._value in self._missing:
            val = None
        else:
            val = self._value
        return {
            'measure': self._name,
            'value': val,
            'description': self._mapping[self._value]
        }


class Section(object): 
    __slots__ = ('_name', '_measures')
    
    def __init__(self, 
        name: str, 
        measures: Union[Callable[...,List[Measure]], List[Measure]] ) -> None:
        """Provides for a list of measures as modeled by the isd documentation. 
        Creates an intermediate level schema and allows applications to iterate over Measures, filling 
        the values from the record-string.

        Args:
            name (str): The section name.
            measures (Union[Callable[...,List[Measure]], List[Measure]]): Either a list of measure instances 
                or a callable that returns one.
        """
        self._name = name
        if callable(measures):
            measures = measures()    
        self._measures = measures 
    
    @property 
    def name(self) -> str: 
        return self._name 
    
    def measures(self) -> Generator[Measure, None, None]:
        """Yields measure instances,

        Yields:
            Generator[Measure]: Yields measure instances.
        """
        for m in self._measures:
            yield m 
            
    def schema(self) -> Dict[str, Any]:
        """Returns a schema that in turn produces schemas for each measure.

        Returns:
            Dict[str, Union[str, List[Dict[str, Any]]]]: A section schema of 
                name: name, measures: List[Measures]
        """
        return {
            'name': self._name, 
            'measures': [m.schema() for m in self._measures]
        }    
    


def control_measures() -> List[Measure]:
    """A convenience factory method that returns all of the ISD measures for the control section.

    Returns:
        List[Measure]: A List of measures from the isd control section.
    """
    return [
        Measure('usaf', Position(5,10)), 
        Measure('wban', Position(11,15)), 
        Measure('date', Position(16,23)), 
        Measure('time', Position(24,27)),
        CategoricalMeasure('data_source_flag', Position(28,28),missing='9', mapping=mappings.DATA_SOURCE_FLAG),
        NumericMeasure('latitude',Position(29,34), missing='+999999', unit='angular_degrees', scaling_factor=1000), 
        NumericMeasure('longitude',Position(35,41), missing='+999999', unit='angular_degrees', scaling_factor=1000), 
        CategoricalMeasure('code', Position(42,46), missing='99999', mapping=mappings.GEOPHYSICAL_REPORT_CODES), 
        NumericMeasure('elevation_dimension', Position(47,51), missing='+9999', scaling_factor=1, unit='meters'),
        Measure('call_letter_identifier', Position(52,56), missing='99999'), 
        CategoricalMeasure('quality_control_process_name', Position(57,60), mapping=mappings.QUALITY_CONTROL_PROCESS)
    ]



def mandatory_measures() -> List[Measure]:
    """A convenience factory method that returns all of the ISD measures for the mandatory section.

    Returns:
        List[Measure]: A List of measures from the isd mandatory section
    """
    return [
        NumericMeasure('wind_observation_direction_angle', Position(61,63), missing='999', scaling_factor=1, unit='angular_degrees'), 
        CategoricalMeasure('wind_observation_direction_quality_code', Position(64,64), mapping=mappings.NUMERICS),
        CategoricalMeasure('wind_observation_type_code', Position(65,65), missing='9', mapping=mappings.WIND_OBS_TYPE_CODE),
        NumericMeasure('wind_observation_speed_rate', Position(66,69), unit='meters_per_second', scaling_factor=10, missing='9999'), 
        CategoricalMeasure('wind_observation_speed_quality_code',Position(70,70), mapping=mappings.NUMERICS),
        NumericMeasure('sky_condition_observation_ceiling_height_dimension', Position(71,75), unit='meters', scaling_factor=1, missing='99999'),
        CategoricalMeasure('sky_condition_observation_ceiling_quality_code', Position(76,76), mapping=mappings.NUMERICS),
        CategoricalMeasure('sky_condition_observation_ceiling_determination_code', Position(77,77), missing='9', mapping=mappings.CEILING_DETERMINATION_CODE),
        CategoricalMeasure('sky_condition_observation_cavok_code', Position(78,78), missing='9', mapping=mappings.CAVOK_CODE), 
        NumericMeasure('visibility_observation_distance_dimension',Position(79,84), unit='meters', missing='999999'),
        CategoricalMeasure('visibility_observation_distance_quality_code', Position(85,85), mapping=mappings.NUMERICS),
        CategoricalMeasure('visibility_observation_variability_code',Position(86,86), missing='9', mapping=mappings.VARIABLITY_CODE),
        CategoricalMeasure('visibility_observation_quality_variability_code', Position(87,87), mapping=mappings.NUMERICS), 
        NumericMeasure('air_temperature_observation_air_temperature', Position(88,92), scaling_factor=10,unit='degrees_celsius', missing='+9999'),
        CategoricalMeasure('air_temperature_observation_air_temperature_quality_code', Position(93,93), mapping=mappings.NUMERICS),
        NumericMeasure('air_temperature_observation_dew_point_temperature', Position(94,98), unit='degrees_celsius', scaling_factor=10,missing='+9999'),
        CategoricalMeasure('air_temperature_observation_dew_point_quality_code', Position(99,99), mapping=mappings.NUMERICS),
        NumericMeasure('atmospheric_pressure_observation_sea_level_pressure', Position(100,104), unit='hectopascals', missing='99999', scaling_factor=10),
        CategoricalMeasure('atmospheric_pressure_observation_sea_level_pressure_quality_code', Position(105,105), mapping=mappings.NUMERICS)
    ]