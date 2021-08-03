import traceback


class ToolException(Exception):
    """An exception base class for all hls4ml_ipbb-specific exceptions."""
    pass


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


class ManyHLSProjectsError(ToolException):
    def __init__(self):
        super().__init__('The hls4ml project has more than one HLS project '
                         'inside. Please use the hls_project_name argument '
                         '(if hls4ml_ipbb is used as a Python module) or the '
                         '--hls-name flag (if ipbb_convert is used).')


class NoSpecifiedHLSProjectError(ToolException):
    def __init__(self):
        super().__init__('The hls4ml project does not have the specified HLS '
                         'project directory inside.')


class NoVHDLError(ToolException):
    def __init__(self):
        super().__init__('The solution does not have an exported VHDL IP '
                         '(but it may have an IP exported in a different HDL)')


class UnknownPortEncounteredError(ToolException):
    def __init__(self, port_name):
        super().__init__(f"The solution has an unknown port '{port_name}'")
        self._port_name = port_name

    @property
    def port_name(self):
        return self._port_name
