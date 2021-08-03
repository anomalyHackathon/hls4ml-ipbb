import pytest
import os
import hls4ml_ipbb
from utils import get_project_path
from hls4ml_ipbb import Project, VHDLWrapper
from hls4ml_ipbb.backend import VivadoBackend


class MetaProject:
    def __init__(self, name, **kwargs):
        self.path = get_project_path(name)
        self.__dict__.update(kwargs)


PROJECTS = [
    MetaProject(name='0', hls_project_name=None, solutions=['solution1']),
    MetaProject(name='1', hls_project_name=None, solutions=['solution1']),
    MetaProject(name='2', hls_project_name='__test',
                solutions=['final__solution'])
]


def compare(actual_path, expected_path):
    assert os.path.exists(actual_path)
    with open(actual_path, 'r') as actual:
        with open(expected_path, 'r') as expected:
            assert [row for row in expected] == [row for row in actual]


@pytest.fixture(scope='module')
def backend():
    return VivadoBackend()


@pytest.mark.parametrize('meta_project,solution', [(p, s)
                                                   for p in PROJECTS
                                                   for s in p.solutions])
def test_vhdl_wrapper_produces_correct_ipbb_component(backend, meta_project,
                                                      solution, tmp_path):
    project = Project(meta_project.path, backend=backend,
                      hls_project_name=meta_project.hls_project_name)
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
    ip_path_expected = os.path.join(meta_project.path, 'expected',
                                    'hls4ml_ip.vhd')
    compare(str(ip_path), ip_path_expected)

    # Check the contents of hls4ml_wrapper.vhd
    wrapper_path = tmp_path / 'hls4ml_wrapper' / 'firmware' / 'hdl' / 'hls4ml_wrapper.vhd'
    wrapper_path_expected = os.path.join(meta_project.path,
                                         'expected', 'hls4ml_wrapper.vhd')
    compare(str(wrapper_path), wrapper_path_expected)
