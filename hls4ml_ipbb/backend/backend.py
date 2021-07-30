from abc import ABC, abstractmethod


class Backend(ABC):
    """
    An abstract class representing an hls4ml_ipbb backend.

    An hls4ml_ipbb backend corresponds to the one used in an hls4ml project.
    For example, if your hls4ml project has a Vivado HLS project inside,
    you want to use a Backend subclass created for Vivado HLS.
    """

    @abstractmethod
    def process_solutions(self, path: str) -> (str, list):
        """
        Searches for an HLS project inside a provided hls4ml project directory
        and extracts available solutions from the first found HLS project.

        Args:
        --------
        path: str
           The path to an hls4ml project directory.

        Returns:
        --------
        A tuple (path, solutions), where 'path' is the path to the HLS project
        found and 'solutions' is the list of names of solutions available in
        that project.
        """
        pass

    @abstractmethod
    def get_hdl_dir_path(self, proj_path: str, solution: str) -> str:
        """
        Gets the root directory of HDL files in a specified solution of a
        provided HLS project.

        Args:
        --------
        proj_path: str
           The path to an HLS project directory (it is not the same as an
           hls4ml project directory).

        solution: str
           The name of a solution inside the HLS project.

        Returns:
        --------
        The path to the root directory of HDL files.
        """
           
        pass

    @abstractmethod
    def get_ip_hdl_file_path(self, proj_path: str, solution: str) -> str:
        """
        Gets the path to the main HDL file (i.e. the one with an hls4ml IP code)
        in a specified solution of a provided HLS project.

        Args:
        --------
        proj_path: str
           The path to an HLS project directory (it is not the same as an
           hls4ml project directory).

        solution: str
           The name of a solution inside the HLS project.

        Returns:
        --------
        The path to the main HDL file.
        """
        pass

    @abstractmethod
    def parse_ports(self, hdl_str: str) -> list:
        """
        Parses a provided hls4ml IP code string to get the list of ports of
        an hls4ml IP.

        Args:
        --------
        hdl_str: str
           An HDL code string to be parsed. It must contain an hls4ml IP code.

        Returns:
        --------
        The list of ports represented by Port objects.
        """
        pass

    @abstractmethod
    def parse_num_inputs(self, ports: list, hdl_str: str) -> int:
        """
        Uses a provided list of hls4ml IP ports along with an hls4ml IP code
        string to get the number of network inputs.

        Args:
        --------
        ports: list of Port
           The list of hls4ml IP ports in form of Port objects.
        hdl_str: str
           An HDL code string. It must contain an hls4ml IP code.

        Returns:
        --------
        The number of network inputs.
        """
        pass
