import os
import shutil
import re
from abc import ABC, abstractmethod
from . import IP, IOType, PortPurpose


class NoVHDLError(Exception):
    pass


class UnknownPortEncounteredError(Exception):
    def __init__(self, port_name):
        self._port_name = port_name

    @property
    def port_name(self):
        return self._port_name


class Wrapper(ABC):
    def __init__(self, ip: IP):
        self._ip = ip

    @abstractmethod
    def save(self, dest: str):
        pass


class VHDLWrapper(Wrapper):
    _PORT_INDENTATION = 6
    _PORT_MAP_INDENTATION = 4
    
    def __init__(self, ip: IP):
        super().__init__(ip)

        self._IP_VAR_DICT = {
            'NUM_INPUTS': IP.get_num_inputs,
            'NUM_OUTPUTS': IP.get_num_outputs,
            'INPUT_WIDTH': IP.get_input_width,
            'OUTPUT_WIDTH': IP.get_output_width
        }

        self._VHDL_VAR_DICT = {
            'PORTS': self._get_ports,
            'PORT_MAP': self._get_port_map
        }
        
    def save(self, dest: str):
        vhdl_path = os.path.join(self._ip.hdl_path, 'vhdl')

        if not os.path.exists(vhdl_path):
            raise NoVHDLError

        os.makedirs(dest, exist_ok=True)

        wrapper_orig_path = os.path.join(os.path.dirname(__file__),
                                         'hls4ml_wrapper')
        wrapper_new_path = os.path.join(dest, 'hls4ml_wrapper')

        shutil.copytree(wrapper_orig_path, wrapper_new_path,
                        ignore=shutil.ignore_patterns('.*', '#*', '*~'),
                        dirs_exist_ok=True)

        wrapper_hdl_path = os.path.join(wrapper_new_path, 'firmware', 'hdl')

        # Gather all IP VHDL files and save everything in a single .vhd file
        entire_hdl_str = ''
        
        for entry in os.listdir(vhdl_path):
            extension = os.path.splitext(entry)[-1].lower()

            if extension != '.vhd':
                continue

            with open(os.path.join(vhdl_path, entry), 'r') as f:
                for line in f:
                    entire_hdl_str += line

        if entire_hdl_str == '':
            raise NoVHDLError

        with open(os.path.join(wrapper_hdl_path, 'hls4ml_ip.vhd'), 'w') as f:
            f.write(entire_hdl_str)

        # Save the wrapper file
        wrapper_str = ''
        with open(os.path.join(wrapper_hdl_path,
                               'hls4ml_wrapper.vhd'), 'r') as f:
            for line in f:
                wrapper_str += line

        for key, func in self._IP_VAR_DICT.items():
            wrapper_str = wrapper_str.replace('{{' + key + '}}',
                                              str(func(self._ip)))

        for key, func in self._VHDL_VAR_DICT.items():
            wrapper_str = wrapper_str.replace('{{' + key + '}}', str(func()))

        with open(os.path.join(wrapper_hdl_path,
                               'hls4ml_wrapper.vhd'), 'w') as f:
            f.write(wrapper_str)

    def _get_ports(self):
        string = ''
        ports = self._ip.get_ports()
        
        for i, port in enumerate(ports):
            string += VHDLWrapper._PORT_INDENTATION * ' '
            string += port.name
            string += ' : '
            string += 'in' if port.io_type == IOType.INPUT else 'out'
            string += ' '
            string += str(port.value_type)

            if i < len(ports) - 1:
                string += ';\n'

        return string

    def _get_port_map(self):
        def get_out_number(name):
            regex = re.compile(r'out_(\d+)', flags=re.IGNORECASE)
            res = regex.search(name)

            if res is None:
                raise UnknownPortEncounteredError(port_name=name)

            return res.group(1)
        
        port_dict = {
            'ap_clk': 'clk_p',
            'ap_rst': "'0'",
            'ap_start': "'1'",
            'ap_done': 'open',
            'ap_idle': 'open',
            'ap_ready': 'open'
        }
        
        string = ''
        ports = self._ip.get_ports()

        for i, port in enumerate(ports):
            string += VHDLWrapper._PORT_MAP_INDENTATION * ' '
            string += port.name
            string += ' => '
            
            if port.name in port_dict:
                string += port_dict[port.name]
            elif port.purpose == PortPurpose.NET_IN:
                string += 'in_V'
            elif port.purpose == PortPurpose.NET_IN_AP_VLD:
                string += 'd_vld(NUM_INPUTS - 1)'
            elif port.purpose == PortPurpose.NET_OUT:
                num = get_out_number(port.name)
                string += f'out_V({num})'
            elif port.purpose == PortPurpose.NET_OUT_AP_VLD:
                num = get_out_number(port.name)
                string += f'out_vld({num})'
            elif port.purpose == PortPurpose.CONST:
                string += 'open'
            else:
                raise UnknownPortEncounteredError(port_name=port.name)

            if i < len(ports) - 1:
                string += ',\n'

        return string
