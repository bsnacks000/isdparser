"""Module for creating the parent schema for a single isd record.
"""
    
import datetime
from typing import Any, Dict, List, Tuple, Union

from .measures import Measure, Section, control_measures, mandatory_measures


class ISDRecord(object):
    __slots__ = ('_datestamp', '_identifier', '_sections')
    
    def __init__(self, 
        datestamp: datetime.datetime, 
        identifier: str, 
        sections: List[Section]) -> None:
        """A container for an isd record. This is a top level container suitable for storage with a 
        top level key and appropriate sections. Technically to create a record with this API all that is needed
        is a single control section with date, time usaf and wban.

        Args:
            datestamp (datetime.datetime): A datetime combined from `date` and `time` control section data.
            identifier (str): An identifier of `usaf`-`wban` extracted from control section data.
            sections (List[Section]): A list of section objects. 
        Raises:
            ValueError: If an empty list is passed for sections.
        """
        self._datestamp = datestamp 
        self._identifier = identifier 
        if len(sections) == 0:
            raise ValueError("Must provide at least a single section.")
        self._sections = sections 
        
        
    def schema(self) -> Dict[str, Union[datetime.datetime, str, Dict[str, Any]]]:
        """Return the record schema

        Returns:
            Dict[str, Union[datetime.datetime, str, Dict[str, Any]]]: Dictionary of complete schema.
        """
        return {  # note this is specifically for mongo
            'datestamp': self._datestamp, 
            'identifier': self._identifier, 
            'sections': [s.schema() for s in self._sections]
        } 


class ISDRecordFactory(object):
    __slots__ = ('_control', '_mandatory')
    
    def __init__(self, 
                 control: Tuple[str, List[Measure]]=('control', control_measures()), 
                 mandatory: Tuple[str, List[Measure]]=('mandatory', mandatory_measures())):
        """Creates an ISDRecord from a single line from an isd file. 
        Object configuration uses Section and Measure object APIs internally. 

        Args:
            control (Tuple[str, List[Measure]], optional): A name and list of control measures. 
                Defaults to ('control', control_measures()).
            mandatory (Tuple[str, List[Measure]], optional): A name and list of section measures. 
                Defaults to ('mandatory', mandatory_measures()).
        """
        self._control = control
        self._mandatory = mandatory
        

    @staticmethod 
    def parse_line(line: str, start: int, end: int) -> str:
        """Return a slice of string.

        Args:
            line (str): The line to slice from
            start (int): start slice
            end (int): end slice

        Returns:
            str: The string slice.
        """
        return line[start:end]
    
    
    @staticmethod
    def make_datestamp(yyyymmdd: str, hhmm: str) -> datetime.datetime:
        """Make a datestamp from a set of two strings.

        Args:
            yyyymmdd (str): A string formatted 'YYYYmmdd'
            hhmm (str): A string formatted 'HHMM'

        Returns:
            datetime.datetime: A utc encoded datetime object.
        """
        year, month, day = int(yyyymmdd[:4]), int(yyyymmdd[4:6]), int(yyyymmdd[6:])
        hours, minutes = int(hhmm[:2]), int(hhmm[2:])
        return datetime.datetime(year, month, day, hours, minutes, tzinfo=datetime.timezone.utc)


    @staticmethod
    def make_station_identifier(usaf: str, wban: str) -> str:
        """Make the station identifier string

        Args:
            usaf (str): usaf string
            wban (str): wban string

        Returns:
            str: combined identifier `usaf`-`wban`
        """
        return usaf + '-' + wban
    
    
    def _extract(self, section, name):
        for m in section.measures():
            if name == m.name:
                return m._value 


    def _create_key(self, section, key=()):
        a,b = self._extract(section, key[0]), self._extract(section, key[1])
        assert all((a, b)), f'`{key[0]}` and `{key[1]}` must be included in the control section in order to create a ParentRecord'
        return a, b 


    def create(self, line: str) -> ISDRecord:
        """Create an ISDRecord with a line of isd data extracted from a file.

        Args:
            line (str): A single line of raw isd data.

        Returns:
            ISDRecord: The resulting ISDRecord object.
        """
        control, mandatory = Section(*self._control), Section(*self._mandatory)
        [m.set_value(self.parse_line(line, m.start, m.end)) 
                        for s in (control, mandatory) 
                            for m in s.measures()]
        
        date, time = self._create_key(control, ('date', 'time'))
        usaf, wban = self._create_key(control, ('usaf', 'wban'))

        datestamp = self.make_datestamp(date, time)
        identifier = self.make_station_identifier(usaf, wban)
        
        return ISDRecord(datestamp, identifier, [control, mandatory])