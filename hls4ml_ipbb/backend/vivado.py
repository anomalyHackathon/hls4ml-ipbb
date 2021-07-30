import re
import os
import defusedxml.ElementTree as ET
from . import Backend
from .. import Port, IOType, ValueType
from ..exception import NoHLSProjectError, InvalidHLSProjectError


class VivadoBackend(Backend):
    """A Backend subclass representing the Vivado HLS backend."""

    def process_solutions(self, path: str) -> (str, list):
        project_path = None
        for root, directories, files in os.walk(path):
            for f in files:
                if f == 'vivado_hls.app':
                    project_path = root
                    break

        if project_path is None:
            raise NoHLSProjectError

        solutions_to_return = []

        try:
            hls_config_tree = ET.parse(os.path.join(project_path,
                                                    'vivado_hls.app'))
            root = hls_config_tree.getroot()
            solutions = root.find('{com.autoesl.autopilot.project}solutions')

            for solution in solutions:
                name = solution.get('name')
                if name is not None:
                    solutions_to_return.append(name)
        except Exception as ex:
            raise InvalidHLSProjectError(exception=ex)

        return project_path, solutions_to_return

    def get_hdl_dir_path(self, proj_path: str, solution: str) -> str:
        return os.path.join(proj_path, solution, 'impl', 'ip', 'hdl')

    def get_ip_hdl_file_path(self, proj_path: str, solution: str) -> str:
        return os.path.join(self.get_hdl_dir_path(proj_path, solution),
                            'vhdl', 'myproject.vhd')

    def parse_ports(self, hdl_str: str) -> list:
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

        return ports

    def parse_num_inputs(self, ports: list, hdl_str: str) -> int:
        const_size_in_name = None
        for port in ports:
            if port.name.startswith('const_size_in'):
                const_size_in_name = port.name
                break

        if const_size_in_name is None:
            return None

        regex = re.compile(const_size_in_name + r'\s+<=\s+(\S+)\s*;',
                           flags=re.IGNORECASE)
        res = regex.search(hdl_str)

        if res is None:
            return None

        const_name = res.group(1)
        regex = re.compile(
            r'constant\s+' + const_name +
            r'\s*:\s+std_logic_vector.+:=\s*"([01]+)"\s*;', flags=re.IGNORECASE)
        res = regex.search(hdl_str)

        if res is None:
            return None

        return int(res.group(1), 2)
