import pytest
import os
import hls4ml_ipbb
from utils import get_project_path
from hls4ml_ipbb import Project, VHDLWrapper
from hls4ml_ipbb.backend import VivadoBackend


PROJECTS = [str(i) for i in range(1)]
PROJECT_SOLUTIONS = [['solution1']]


def compare(actual_path, expected_path):
    assert os.path.exists(actual_path)
    with open(actual_path, 'r') as actual:
        with open(expected_path, 'r') as expected:
            assert [row for row in expected] == [row for row in actual]


@pytest.fixture(scope='module')
def backend():
    return VivadoBackend()


@pytest.mark.parametrize('project_name,solution',
                         [(p, s) for i, p in enumerate(PROJECTS)
                          for s in PROJECT_SOLUTIONS[i]])
def test_vhdl_wrapper_produces_correct_ipbb_component(backend, project_name,
                                                      solution, tmp_path):
    project = Project(get_project_path(project_name), backend=backend)
    ip = project.get_ip(solution)
    wrapper = VHDLWrapper(ip)
    wrapper.save(str(tmp_path))

    # Check the dir tree
    dir_tree = {
        str(tmp_path / 'hls4ml_wrapper'): 0,
        str(tmp_path / 'hls4ml_wrapper' / 'addr_table'): 0,
        str(tmp_path / 'hls4ml_wrapper' / 'firmware'): 0,
        str(tmp_path / 'hls4ml_wrapper' / 'firmware' / 'cfg'): 0,
        str(tmp_path / 'hls4ml_wrapper' / 'firmware' / 'hdl'): 0,
        str(tmp_path / 'hls4ml_wrapper' / 'firmware' / 'ucf'): 0,
    }
    
    for root, dirs, _ in os.walk(str(tmp_path)):
        for directory in dirs:
            path = os.path.join(root, directory)
            assert path in dir_tree
            dir_tree[path] += 1

    for key, val in dir_tree.items():
        assert val == 1

    # Check the contents of fixed files
    paths = [
        os.path.join('hls4ml_wrapper', 'addr_table', 'hls4ml_wrapper.xml'),
        os.path.join('hls4ml_wrapper', 'firmware', 'cfg', 'hls4ml_wrapper.dep'),
        os.path.join('hls4ml_wrapper', 'firmware', 'cfg',
                     'hls4ml_wrapper_msg_suppressions.tcl'),
        os.path.join('hls4ml_wrapper', 'firmware', 'ucf', 'hls4ml_wrapper.tcl')
    ]

    for path in paths:
        actual_path = str(tmp_path / path)
        expected_path = os.path.join(os.path.dirname(hls4ml_ipbb.__file__),
                                     path)
        compare(actual_path, expected_path)

    # Check the contents of hls4ml_ip.vhd
    ip_path = tmp_path / 'hls4ml_wrapper' / 'firmware' / 'hdl' / 'hls4ml_ip.vhd'
    ip_path_expected = os.path.join(get_project_path(project_name), 'expected',
                                    'hls4ml_ip.vhd')
    compare(str(ip_path), ip_path_expected)

    # Check the contents of hls4ml_wrapper.vhd
    wrapper_path = tmp_path / 'hls4ml_wrapper' / 'firmware' / 'hdl' / 'hls4ml_wrapper.vhd'
    wrapper_path_expected = os.path.join(get_project_path(project_name),
                                         'expected', 'hls4ml_wrapper.vhd')
    compare(str(wrapper_path), wrapper_path_expected)
    
