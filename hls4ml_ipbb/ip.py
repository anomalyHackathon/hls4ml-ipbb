import os
import defusedxml.ElementTree as ET


class NoHDLError(Exception):
    pass


class NoHLSProjectError(Exception):
    pass


class InvalidHLSProjectError(Exception):
    def __init__(self, exception):
        self._exception = exception

    @property
    def original_exception(self):
        return self._exception


class IP:
    def __init__(self, proj_src):
        if not os.path.exists(proj_src):
            raise FileNotFoundError

        self._process_solutions(proj_src)
      
    def _process_solutions(self, proj_src):
        project_path = None
        for root, directories, files in os.walk(proj_src):
            for f in files:
                if f == 'vivado_hls.app':
                    project_path = root
                    break

        if project_path is None:
            raise NoHLSProjectError

        self._solutions = []

        try:
            hls_config_tree = ET.parse(os.path.join(project_path, 'vivado_hls.app'))
            root = hls_config_tree.getroot()
            solutions = root.find('solutions')

            for solution in solutions:
                name = solution.get('name')
                if name is not None:
                    self._solutions.append(name)
        except Exception as ex:
            raise InvalidHLSProjectError(ex)

        self._solution = None

    def _check_solution(self):
        if self.get_solution() is None:
            raise RuntimeError('You must select a solution first by calling set_solution()')

    def set_solution(self, solution):
        if solution in self.get_solutions():
            self._solution = solution
        else:
            raise RuntimeError('solution must be an element of get_solutions()')

    def get_solution(self):
        return self._solution

    def get_solutions(self):
        return self._solutions
    
    def get_ports(self):
        self._check_solution()
        return ports

    def get_num_inputs(self):
        self._check_solution()
        return self._num_inputs

    def get_num_outputs(self):
        self._check_solution()
        return self._num_outputs
