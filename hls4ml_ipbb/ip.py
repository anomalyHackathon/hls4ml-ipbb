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
    """
    A class representing an hls4ml project (i.e. the one with a YAML config file
    inside).

    Args:
    --------
    path : str
       The path to an hls4ml project directory.

    Raises:
    --------
    FileNotFoundError
       When the provided path points to a non-existent directory.

    NoHLSProjectError
       When there is no Vivado HLS project in the hls4ml project.

    InvalidHLSProjectError
       When an error occurs during processing a Vivado HLS project in the hls4ml
       project.
    """
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError('The specified hls4ml project does not '
                                    'exist')

        self._process_solutions(path)
      
    def _process_solutions(self, path: str):
        """A private method processing Vivado HLS solutions in the project."""
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
        """The list of names of Vivado HLS solutions in the project."""
        return self._solutions

    @property
    def path(self):
        """The path to the Vivado HLS project inside the hls4ml project."""
        return self._path
        
    def get_ip(self, solution: str):
        """
        Creates an hls4ml_ipbb.IP object corresponding to the IP in a specified
        Vivado HLS solution in the hls4ml project.

        Args:
        --------
        solution : str
           The name of a solution for which the IP object should be returned.
           It must be an element of the 'solutions' list.

        Returns:
        --------
        An hls4ml_ipbb.IP object corresponding to the IP in the solution.
        If the provided solution name does not exist, None is returned.
        """
        if solution in self.solutions:
            return IP(self, solution)
        else:
            return None


class IP:
    """
    A class representing an hls4ml IP.

    Args:
    --------
    proj : Project
       An hls4ml project, in form of a Project object.
    
    solution : str
       The name of a solution where the hls4ml IP can be found. The solution
       must exist in the hls4ml project and must have the exported IP (this can
       be done by running an appropriate Vivado HLS feature).

    Raises:
    --------
    NoHDLError
       When no exported IP can be found in the solution. 
    """
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

        if self._num_inputs is None:
            print('warning: the number of network inputs could not be inferred, '
                  'so both get_num_inputs() and get_input_width() will return '
                  'None')

        self._num_outputs = len(list(filter(
            lambda x: x.purpose == PortPurpose.NET_OUT, self._ports)))

    def _parse_ports(self, hdl_str: str):
        """A private method parsing IP ports from the provided VHDL code string."""
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
        """A private method parsing the number of network inputs from the provided VHDL code string."""
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
        """The path where the HDL code of the IP can be found."""
        return self._hdl_path

    def get_ports(self):
        """Gets the IP ports, represented by Port objects."""
        return self._ports

    def get_num_inputs(self):
        """
        Gets the number of network inputs (it is not the same as input ports).
        
        Returns:
        --------
        The number of network inputs. It is None when the number could not be
        inferred from the HDL code.
        """
        return self._num_inputs

    def get_num_outputs(self):
        """Gets the number of network outputs (it is not the same as output ports)."""
        return self._num_outputs

    def get_input_width(self):
        """
        Gets the bit width of a network input in the IP.

        Returns:
        --------
        The bit width of a network input. It is None when the number could not be
        inferred from the HDL code.
        """
        if self.get_num_inputs() is None:
            return None

        in_port = next(filter(lambda x: x.purpose == PortPurpose.NET_IN,
                              self.get_ports()))
        return len(in_port.value_type) // self.get_num_inputs()

    def get_output_width(self):
        """Gets the bit width of a network output in the IP."""
        out_port = next(filter(lambda x: x.purpose == PortPurpose.NET_OUT,
                               self.get_ports()))
        return len(out_port.value_type)
