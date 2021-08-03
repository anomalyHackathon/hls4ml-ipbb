import os
import pytest
import hls4ml_ipbb.exception as exc
from utils import get_project_path
from hls4ml_ipbb import Project, IP, Port, IOType
from hls4ml_ipbb import VHDLStdLogic, VHDLStdLogicVector
from hls4ml_ipbb.backend import VivadoBackend


class MetaProject:
    def __init__(self, name, **kwargs):
        self.path = get_project_path(name)
        self.__dict__.update(kwargs)


class MetaSolution:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


PROJECTS = [
    MetaProject(name='0', hls_path='myproject_prj', hls_project_name=None,
                solutions=[
                    MetaSolution(name='solution1',
                                 num_inputs=16,
                                 num_outputs=5,
                                 input_width=16,
                                 output_width=16,
                                 ports=[
                                     Port(name='ap_clk',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_rst',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_start',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_done',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_idle',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_ready',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='fc1_input_V_ap_vld',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='fc1_input_V',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogicVector(256)),
                                     Port(name='layer13_out_0_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(16)),
                                     Port(name='layer13_out_0_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer13_out_1_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(16)),
                                     Port(name='layer13_out_1_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer13_out_2_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(16)),
                                     Port(name='layer13_out_2_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer13_out_3_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(16)),
                                     Port(name='layer13_out_3_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer13_out_4_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(16)),
                                     Port(name='layer13_out_4_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='const_size_in_1',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(16)),
                                     Port(name='const_size_in_1_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='const_size_out_1',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(16)),
                                     Port(name='const_size_out_1_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic())
                                 ])
                ]),
    MetaProject(name='1', hls_path='hlsproject', hls_project_name=None,
                solutions=[
                    MetaSolution(name='solution1',
                                 num_inputs=16,
                                 num_outputs=5,
                                 input_width=7,
                                 output_width=41,
                                 ports=[
                                     Port(name='ap_clk',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_rst',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_start',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_done',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_idle',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_ready',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='fc1_input_V_ap_vld',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='fc1_input_V',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogicVector(112)),
                                     Port(name='layer13_out_0_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(41)),
                                     Port(name='layer13_out_0_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer13_out_1_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(41)),
                                     Port(name='layer13_out_1_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer13_out_2_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(41)),
                                     Port(name='layer13_out_2_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer13_out_3_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(41)),
                                     Port(name='layer13_out_3_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer13_out_4_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(41)),
                                     Port(name='layer13_out_4_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='const_size_in_1',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(16)),
                                     Port(name='const_size_in_1_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='const_size_out_1',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(16)),
                                     Port(name='const_size_out_1_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic())
                                 ])
                    ]),
    MetaProject(name='2', hls_path='__test', hls_project_name='__test',
                solutions=[
                    MetaSolution(name='final__solution',
                                 num_inputs=40,
                                 num_outputs=23,
                                 input_width=22,
                                 output_width=34,
                                 ports=[
                                     Port(name='ap_clk',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_rst',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_start',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_done',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_idle',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='ap_ready',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer1_input_V_ap_vld',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer1_input_V',
                                          io_type=IOType.INPUT,
                                          value_type=VHDLStdLogicVector(880)),
                                     Port(name='layer10_out_0_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_0_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_1_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_1_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_2_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_2_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_3_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_3_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_4_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_4_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_5_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_5_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_6_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_6_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_7_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_7_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_8_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_8_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_9_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_9_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_10_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_10_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_11_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_11_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_12_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_12_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_13_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_13_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_14_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_14_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_15_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_15_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_16_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_16_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_17_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_17_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_18_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_18_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_19_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_19_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_20_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_20_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_21_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_21_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='layer10_out_22_V',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(34)),
                                     Port(name='layer10_out_22_V_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='const_size_in_1',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(16)),
                                     Port(name='const_size_in_1_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic()),
                                     Port(name='const_size_out_1',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogicVector(16)),
                                     Port(name='const_size_out_1_ap_vld',
                                          io_type=IOType.OUTPUT,
                                          value_type=VHDLStdLogic())
                                     ])
                    ])
]


@pytest.fixture(scope='module')
def backend():
    return VivadoBackend()


def test_project_no_hls_project(backend):
    with pytest.raises(exc.NoHLSProjectError):
        Project(get_project_path('no_hls'), backend=backend)


def test_project_invalid_hls_project(backend):
    with pytest.raises(exc.InvalidHLSProjectError):
        Project(get_project_path('invalid_hls'), backend=backend)


def test_project_many_hls_projects(backend):
    with pytest.raises(exc.ManyHLSProjectsError):
        Project(get_project_path('2'), backend=backend)


def test_project_no_specified_hls_project(backend):
    with pytest.raises(exc.NoSpecifiedHLSProjectError):
        Project(get_project_path('0'), backend=backend,
                hls_project_name='reifmdfjr')


@pytest.mark.parametrize('meta_project', PROJECTS)
def test_project_backend_returns_correct_backend(backend, meta_project):
    project = Project(meta_project.path, backend=backend,
                      hls_project_name=meta_project.hls_project_name)
    assert project.backend == backend
    

@pytest.mark.parametrize('meta_project', PROJECTS)
def test_project_solutions_returns_correct_solutions(backend, meta_project):
    project = Project(meta_project.path, backend=backend,
                      hls_project_name=meta_project.hls_project_name)
    assert project.solutions == list(map(lambda x: x.name,
                                         meta_project.solutions))


@pytest.mark.parametrize('meta_project', PROJECTS)
def test_project_path_returns_correct_path(backend, meta_project):
    path = meta_project.path
    project = Project(path, backend=backend,
                      hls_project_name=meta_project.hls_project_name)
    assert project.path == os.path.join(path, meta_project.hls_path)


@pytest.mark.parametrize('meta_project,solution', [(p, s) for p in PROJECTS
                                                   for s in p.solutions])
def test_project_get_ip_returns_ip(backend, meta_project, solution):
    project = Project(meta_project.path, backend=backend,
                      hls_project_name=meta_project.hls_project_name)
    assert isinstance(project.get_ip(solution.name), IP)


@pytest.mark.parametrize('meta_project', PROJECTS)
def test_project_get_ip_returns_none_for_invalid_solution(backend, meta_project):
    project = Project(meta_project.path, backend=backend,
                      hls_project_name=meta_project.hls_project_name)
    assert project.get_ip('giorejmgioerujgmoeri') is None


@pytest.mark.parametrize('project_name', ['no_ip_0', 'no_ip_1'])
def test_ip_no_hdl_error(backend, project_name):
    project = Project(get_project_path(project_name), backend=backend)
    with pytest.raises(exc.NoHDLError):
        project.get_ip('solution1')


@pytest.mark.parametrize('meta_project,solution', [(p, s) for p in PROJECTS
                                                   for s in p.solutions])
def test_ip_hdl_path_returns_correct_hdl_path(backend, meta_project, solution):
    project = Project(meta_project.path, backend=backend,
                      hls_project_name=meta_project.hls_project_name)
    ip = project.get_ip(solution.name)
    assert ip.hdl_path == os.path.join(project.path,
                                       solution.name,
                                       'impl',
                                       'ip',
                                       'hdl')


@pytest.mark.parametrize('meta_project,solution', [(p, s) for p in PROJECTS
                                                   for s in p.solutions])
def test_ip_get_num_inputs_returns_correct_num_inputs(backend, meta_project,
                                                      solution):
    project = Project(meta_project.path, backend=backend,
                      hls_project_name=meta_project.hls_project_name)
    ip = project.get_ip(solution.name)
    assert ip.get_num_inputs() == solution.num_inputs


@pytest.mark.parametrize('meta_project,solution', [(p, s) for p in PROJECTS
                                                   for s in p.solutions])
def test_ip_get_num_outputs_returns_correct_num_outputs(backend, meta_project,
                                                        solution):
    project = Project(meta_project.path, backend=backend,
                      hls_project_name=meta_project.hls_project_name)
    ip = project.get_ip(solution.name)
    assert ip.get_num_outputs() == solution.num_outputs


@pytest.mark.parametrize('meta_project,solution', [(p, s) for p in PROJECTS
                                                   for s in p.solutions])
def test_ip_get_input_width_returns_correct_input_width(backend, meta_project,
                                                        solution):
    project = Project(meta_project.path, backend=backend,
                      hls_project_name=meta_project.hls_project_name)
    ip = project.get_ip(solution.name)
    assert ip.get_input_width() == solution.input_width


@pytest.mark.parametrize('meta_project,solution', [(p, s) for p in PROJECTS
                                                   for s in p.solutions])
def test_ip_get_output_width_returns_correct_output_width(backend, meta_project,
                                                          solution):
    project = Project(meta_project.path, backend=backend,
                      hls_project_name=meta_project.hls_project_name)
    ip = project.get_ip(solution.name)
    assert ip.get_output_width() == solution.output_width


@pytest.mark.parametrize('meta_project,solution', [(p, s) for p in PROJECTS
                                                   for s in p.solutions])
def test_ip_get_ports_returns_correct_ports(backend, meta_project, solution):
    project = Project(meta_project.path, backend=backend,
                      hls_project_name=meta_project.hls_project_name)
    ip = project.get_ip(solution.name)
    assert ip.get_ports() == solution.ports
