import pytest
from hls4ml_ipbb import Port, IOType, VHDLStdLogic, VHDLStdLogicVector
from hls4ml_ipbb import PortPurpose, ValueType


@pytest.mark.parametrize('name', ['test1', 'test2', 'test3'])
def test_port_name_returns_correct_name(name):
    port = Port(name=name, io_type=IOType.INPUT, value_type=VHDLStdLogic())
    assert port.name == name


@pytest.mark.parametrize('io_type', list(IOType))
def test_port_io_type_returns_correct_io_type(io_type):
    port = Port(name='test', io_type=io_type, value_type=VHDLStdLogic())
    assert port.io_type == io_type


@pytest.mark.parametrize('value_type', [VHDLStdLogic(), VHDLStdLogicVector(10)])
def test_port_value_type_returns_correct_value_type(value_type):
    port = Port(name='test', io_type=IOType.INPUT, value_type=value_type)
    assert port.value_type == value_type


@pytest.mark.parametrize('name,expected', [('test_input_1', PortPurpose.NET_IN),
                                           ('abc_abc_in_121', PortPurpose.OTHER),
                                           ('12_out_z', PortPurpose.NET_OUT),
                                           ('fc1_input_V', PortPurpose.NET_IN),
                                           ('fmgjiomc94', PortPurpose.OTHER),
                                           ('fc1_input_V_ap_vld',
                                            PortPurpose.NET_IN_AP_VLD),
                                           ('abc_out_28', PortPurpose.NET_OUT),
                                           ('layer13_out_3_V',
                                            PortPurpose.NET_OUT),
                                           ('layer13_out_0_V_ap_vld',
                                            PortPurpose.NET_OUT_AP_VLD),
                                           ('const_1', PortPurpose.CONST),
                                           ('const_size_in_1',
                                            PortPurpose.CONST),
                                           ('const_size_out_1',
                                            PortPurpose.CONST),
                                           ('ap_vld', PortPurpose.OTHER)])
def test_port_purpose_returns_correct_purpose(name, expected):
    port = Port(name=name, io_type=IOType.INPUT, value_type=VHDLStdLogic())
    assert port.purpose == expected


def test_valuetype_convert_returns_vhdl_std_logic():
    assert isinstance(ValueType.convert('std_logic'), VHDLStdLogic)
    assert isinstance(ValueType.convert('STD_logic'), VHDLStdLogic)
    assert isinstance(ValueType.convert('STD_LOGIC'), VHDLStdLogic)


@pytest.mark.parametrize('name,expected_size',
                         [('std_logic_vector(10 downto 0)', 11),
                          ('std_logic_vector(2292 downto 0)', 2293),
                          ('STD_LOGIC_VECTOR  (1  DOWNto  0)', 2),
                          ('STD_LOGIC_VECTOR (7 DOWNTO 0)', 8),
                          ('std_logic_vector (0 to 88)', 89),
                          ('STD_Logic_Vector(0 to 100)', 101),
                          ('STD_LOGIC_VECTOR\t(0 to 204)', 205),
                          ('std_logic_vector(0 to 9)', 10)])
def test_valuetype_convert_returns_vhdl_std_logic_vector(name, expected_size):
    instance = ValueType.convert(name)
    assert isinstance(instance, VHDLStdLogicVector)
    assert len(instance) == expected_size


@pytest.mark.parametrize('name', ['ajoijmo', 'std_logic2', 'std_logic;',
                                  'std_logic_vector(2 to 1)',
                                  'STD_LOGIC_VECTOR (89 downto 2)'])
def test_valuetype_convert_returns_none_for_invalid_str(name):
    assert ValueType.convert(name) is None
