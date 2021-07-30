import re
from abc import ABC, abstractmethod
from enum import Enum


class IOType(Enum):
    """An enum representing the IO type of a port."""
    INPUT = 0
    OUTPUT = 1


class PortPurpose(Enum):
    """An enum representing the purpose of a port."""
    NET_IN = 0
    NET_OUT = 1
    NET_IN_AP_VLD = 2
    NET_OUT_AP_VLD = 3
    CONST = 4
    OTHER = 5


class ValueType(ABC):
    """An abstract class representing a port value type in HDL."""

    @abstractmethod
    def __str__(self):
        """A string representation of the object that can be inserted directly into an HDL code."""
        pass

    def convert(type_str: str):
        """
        Converts a type string (e.g. std_logic in VHDL) to a ValueType
        subclass object.

        Args:
        --------
        type_str : str
           A type string to be converted.
        
        Returns:
        --------
        A ValueType subclass object corresponding to the type string. If
        the method does not know what to do with the provided string, it
        returns None.
        """
        type_str = type_str.lower()
        if type_str == 'std_logic':
            return VHDLStdLogic()
        elif type_str.find('std_logic_vector') != -1:
            regex = re.compile(
                r'std_logic_vector\s*\(\s*(\d+)\s+downto\s+0\s*\)')
            res = regex.search(type_str)

            if res is None:
                regex = re.compile(r'std_logic_vector\s*\(\s*0\s+to\s+(\d+)s*\)')
                res = regex.search(type_str)

                if res is None:
                    return None

            return VHDLStdLogicVector(int(res.group(1)) + 1)
        else:
            return None


class VHDLStdLogic(ValueType):
    """A ValueType subclass representing VHDL's STD_LOGIC."""
    def __str__(self):
        return 'std_logic'

    def __len__(self):
        """The bit width of STD_LOGIC."""
        return 1


class VHDLStdLogicVector(ValueType):
    """
    A ValueType subclass representing VHDL's STD_LOGIC_VECTOR.

    Args:
    --------
    size : int
       The bit width of the type.
    """
    def __init__(self, size):
        self._size = size

    def __str__(self):
        return f'std_logic_vector({self._size - 1} downto 0)'

    def __len__(self):
        return self._size


class Port:
    """
    A class representing a port in an IP.

    Args:
    --------
    name : str
       The name of the port as it appears in an HDL code.
    io_type : IOType
       The IO type of the port.
    value_type : ValueType
       The value type of the port.
    """
    def __init__(self, name: str, io_type: IOType, value_type: ValueType):
        self._name = name
        self._io_type = io_type
        self._value_type = value_type

        if name.startswith('const'):
            self._purpose = PortPurpose.CONST
        else:
            is_in = name.find('_input_') != -1
            is_out = name.find('_out_') != -1

            if is_in:
                self._purpose = \
                    PortPurpose.NET_IN_AP_VLD \
                    if name.endswith('ap_vld') \
                       else PortPurpose.NET_IN
            elif is_out:
                self._purpose = \
                    PortPurpose.NET_OUT_AP_VLD \
                    if name.endswith('ap_vld') \
                       else PortPurpose.NET_OUT
            else:
                self._purpose = PortPurpose.OTHER

    @property
    def name(self):
        """The name of the port."""
        return self._name

    @property
    def io_type(self):
        """The IO type of the port."""
        return self._io_type

    @property
    def value_type(self):
        """The value type of the port."""
        return self._value_type

    @property
    def purpose(self):
        """The purpose of the port."""
        return self._purpose

    
