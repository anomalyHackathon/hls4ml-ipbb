from abc import ABC, abstractmethod


class Wrapper(ABC):
    def __init__(self, ip: IP):
        self._ip = ip

    @abstractmethod
    def save(self, dest: str):
        pass


class VHDLWrapper(Wrapper):
    _IP_VAR_DICT = {
        'NUM_INPUTS': IP.get_num_inputs,
        'NUM_OUTPUTS': IP.get_num_outputs,
        'INPUT_WIDTH': None,
        'OUTPUT_WIDTH': None
    }

    _VHDL_VAR_DICT = {
        'PORTS': VHDLWrapper._get_ports,
        'PORT_MAP': VHDLWrapper._get_port_map
    }
    
    def __init__(self, ip: IP):
        super().__init__(ip)
        self._wrapper_str = ''
        
    def save(self, dest: str):
        pass

    def _get_ports(self):
        pass

    def _get_port_map(self):
        pass
