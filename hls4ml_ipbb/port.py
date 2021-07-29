from abc import ABC, abstractmethod
from enum import Enum


class IOType(Enum):
    INPUT = 0
    OUTPUT = 1


class PortPurpose(Enum):
    NET_IN = 0
    NET_OUT = 1
    NET_IN_AP_VLD = 2
    NET_OUT_AP_VLD = 3
    CONST = 4
    OTHER = 5


class ValueType(ABC):
    @abstractmethod
    def __str__(self):
        pass


class VHDLStdLogic(ValueType):
    def __str__(self):
        return 'std_logic'

    def __len__(self):
        return 1


class VHDLStdLogicVector(ValueType):
    def __init__(self, size):
        self._size = size

    def __str__(self):
        return f'std_logic_vector({self._size - 1} downto 0)'

    def __len__(self):
        return self._size


class Port:
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
                self._purpose = PortPurpose.NET_IN_AP_VLD if name.endswith('ap_vld') else PortPurpose.NET_IN
            elif is_out:
                self._purpose = PortPurpose.NET_OUT_AP_VLD if name.endswith('ap_vld') else PortPurpose.NET_OUT
            else:
                self._purpose = PortPurpose.OTHER

    @property
    def name(self):
        return self._name

    @property
    def io_type(self):
        return self._io_type

    @property
    def value_type(self):
        return self._value_type

    @property
    def purpose(self):
        return self._purpose

    
