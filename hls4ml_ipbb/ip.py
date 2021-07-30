import os
import defusedxml.ElementTree as ET
import re
import traceback
from . import Port, ValueType, IOType, PortPurpose, ToolException


class NoHDLError(ToolException):
    def __init__(self):
        super().__init__('The solution does not have an exported IP')


class NoHLSProjectError(ToolException):
    def __init__(self):
        super().__init__('The specified hls4ml project does not have any '
                         'Vivado HLS project directory inside')


class InvalidHLSProjectError(ToolException):
    def __init__(self, exception):
        traceback.print_exception(type(exception), exception,
                                  exception.__traceback__)
        message = 'The Vivado HLS project inside the specified hls4ml project ' \
            f'could not be processed because of {type(exception).__name__} ' \
            'printed above'
        super().__init__(message)

        self._exception = exception

    @property
    def original_exception(self):
        return self._exception


class Project:
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError('The specified hls4ml project does not '
                                    'exist')

        self._process_solutions(path)
      
    def _process_solutions(self, path: str):
        project_path = None
        for root, directories, files in os.walk(path):
            for f in files:
                if f == 'vivado_hls.app':
                    project_path = root
                    break

        if project_path is None:
            raise NoHLSProjectError

        self._path = project_path
        self._solutions = []

        try:
            hls_config_tree = ET.parse(os.path.join(project_path,
                                                    'vivado_hls.app'))
            root = hls_config_tree.getroot()
            solutions = root.find('{com.autoesl.autopilot.project}solutions')

            for solution in solutions:
                name = solution.get('name')
                if name is not None:
                    self._solutions.append(name)
        except Exception as ex:
            raise InvalidHLSProjectError(exception=ex)

        self._solution = None

    @property
    def solutions(self):
        return self._solutions

    @property
    def path(self):
        return self._path
        
    def get_ip(self, solution: str):
        if solution in self.solutions:
            return IP(self, solution)
        else:
            raise RuntimeError(f"'{solution}' is not one of {self.solutions}.")


class IP:
    def __init__(self, proj: Project, solution: str):
        self._hdl_path = os.path.join(proj.path, solution, 'impl', 'ip', 'hdl')

        if not os.path.exists(self._hdl_path):
            raise NoHDLError

        myproject_vhd_path = os.path.join(self._hdl_path, 'vhdl',
                                          'myproject.vhd')

        if not os.path.exists(myproject_vhd_path):
            raise NoHDLError

        hdl_str = ''
        with open(myproject_vhd_path, 'r') as f:
            for line in f:
                hdl_str += line

        self._parse_ports(hdl_str)
        self._parse_num_inputs(hdl_str)

        self._num_outputs = len(list(filter(
            lambda x: x.purpose == PortPurpose.NET_OUT, self._ports)))

    def _parse_ports(self, hdl_str: str):
        regex = re.compile(
            r'entity\s+myproject\s+is\s+port\s*\((.*)\)\s*;\s*end\s*;',
            flags=re.DOTALL|re.IGNORECASE)
        res = regex.search(hdl_str)

        port_lines = map(str.strip, res.group(1).split('\n'))
        ports = []

        line_regex = re.compile(r'(\S+)\s*:\s+(in|out)\s+([^;]+);?',
                                flags=re.IGNORECASE)
        for line in port_lines:
            line_res = line_regex.search(line)

            if line_res is None:
                continue
            
            ports.append(Port(line_res.group(1),
                              IOType.INPUT
                              if line_res.group(2).lower() == 'in'
                              else IOType.OUTPUT,
                              ValueType.convert(line_res.group(3))))

        self._ports = ports

    def _parse_num_inputs(self, hdl_str: str):
        const_size_in_name = None
        for port in self._ports:
            if port.name.startswith('const_size_in'):
                const_size_in_name = port.name
                break

        if const_size_in_name is None:
            self._num_inputs = None
            return

        regex = re.compile(const_size_in_name + r'\s+<=\s+(\S+)\s*;',
                           flags=re.IGNORECASE)
        res = regex.search(hdl_str)

        if res is None:
            self._num_inputs = None
            return

        const_name = res.group(1)
        regex = re.compile(
            r'constant\s+' + const_name +
            r'\s*:\s+std_logic_vector.+:=\s*"([01]+)"\s*;', flags=re.IGNORECASE)
        res = regex.search(hdl_str)

        if res is None:
            self._num_inputs = None
            return

        self._num_inputs = int(res.group(1), 2)

    @property
    def hdl_path(self):
        return self._hdl_path

    def get_ports(self):
        return self._ports

    def get_num_inputs(self):
        return self._num_inputs

    def get_num_outputs(self):
        return self._num_outputs

    def get_input_width(self):
        in_port = next(filter(lambda x: x.purpose == PortPurpose.NET_IN,
                              self.get_ports()))
        return len(in_port.value_type) // self.get_num_inputs()

    def get_output_width(self):
        out_port = next(filter(lambda x: x.purpose == PortPurpose.NET_OUT,
                               self.get_ports()))
        return len(out_port.value_type)
