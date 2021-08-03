import os
import re
import traceback
from . import Port, ValueType, IOType, PortPurpose
from .backend import Backend
from .exception import NoHDLError


class Project:
    """
    A class representing an hls4ml project (i.e. the one with a YAML config file
    inside).

    Args:
    --------
    path : str
       The path to an hls4ml project directory.

    backend : Backend
       The backend used in the hls4ml project, in form of
       an hls4ml_ipbb.backend.Backend object (e.g. a VivadoBackend object).

    hls_project_name : str, optional
       The name of an HLS project directory inside the hls4ml project. It is
       usually not needed to provide this argument as hls4ml projects normally
       contain only one HLS project. However, if it's not the case, the
       value of hls_project_name must be provided.

    Raises:
    --------
    FileNotFoundError
       When the provided path points to a non-existent directory.

    NoHLSProjectError
       When there is no valid HLS project in the hls4ml project.

    InvalidHLSProjectError
       When an error occurs during processing an HLS project in the hls4ml
       project.

    ManyHLSProjectsError
       When the hls4ml project contains more than one HLS project and
       hls_project_name is not provided (or is None).
    """
    def __init__(self, path: str, backend: Backend,
                 hls_project_name: str = None):
        if not os.path.exists(path):
            raise FileNotFoundError('The specified hls4ml project does not '
                                    'exist')

        self._backend = backend
        self._path, self._solutions = \
            self._backend.process_solutions(path, hls_project_name)

    @property
    def backend(self):
        """The backend used in the project."""
        return self._backend
        
    @property
    def solutions(self):
        """The list of names of solutions in the project."""
        return self._solutions

    @property
    def path(self):
        """The path to the HLS project inside the hls4ml project."""
        return self._path
        
    def get_ip(self, solution: str):
        """
        Creates an hls4ml_ipbb.IP object corresponding to the IP in a specified
        solution in the hls4ml project.

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
       be done by running an appropriate feature in your HLS software).

    Raises:
    --------
    NoHDLError
       When no exported IP can be found in the solution. 
    """
    def __init__(self, proj: Project, solution: str):
        self._hdl_path = proj.backend.get_hdl_dir_path(proj.path, solution)

        if not os.path.exists(self._hdl_path):
            raise NoHDLError

        myproject_vhd_path = proj.backend.get_ip_hdl_file_path(proj.path,
                                                               solution)

        if not os.path.exists(myproject_vhd_path):
            raise NoHDLError

        hdl_str = ''
        with open(myproject_vhd_path, 'r') as f:
            for line in f:
                hdl_str += line

        self._ports = proj.backend.parse_ports(hdl_str)
        self._num_inputs = proj.backend.parse_num_inputs(self._ports, hdl_str)

        if self._num_inputs is None:
            print('warning: the number of network inputs could not be inferred, '
                  'so both get_num_inputs() and get_input_width() will return '
                  'None')

        self._num_outputs = len(list(filter(
            lambda x: x.purpose == PortPurpose.NET_OUT, self._ports)))

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
