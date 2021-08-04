-- hls4ml IP wrapper based on null_algo made by Dave Newbold
--
-- Maksymilian Graczyk, July 2021

library IEEE;
use IEEE.STD_LOGIC_1164.all;

use work.ipbus.all;
use work.emp_data_types.all;
use work.emp_project_decl.all;

use work.emp_device_decl.all;
use work.emp_ttc_decl.all;

entity emp_payload is
  port(
    clk         : in  std_logic;        -- ipbus signals
    rst         : in  std_logic;
    ipb_in      : in  ipb_wbus;
    ipb_out     : out ipb_rbus;
    clk_payload : in  std_logic_vector(2 downto 0);
    rst_payload : in  std_logic_vector(2 downto 0);
    clk_p       : in  std_logic;        -- data clock
    rst_loc     : in  std_logic_vector(N_REGION - 1 downto 0);
    clken_loc   : in  std_logic_vector(N_REGION - 1 downto 0);
    ctrs        : in  ttc_stuff_array;
    bc0         : out std_logic;
    d           : in  ldata(4 * N_REGION - 1 downto 0);  -- data in
    q           : out ldata(4 * N_REGION - 1 downto 0);  -- data out
    gpio        : out std_logic_vector(29 downto 0);  -- IO to mezzanine connector
    gpio_en     : out std_logic_vector(29 downto 0)  -- IO to mezzanine connector (three-state enables)
    );

end emp_payload;

architecture rtl of emp_payload is

  component myproject is
    port(
      ap_clk : in std_logic;
      ap_rst : in std_logic;
      ap_start : in std_logic;
      ap_done : out std_logic;
      ap_idle : out std_logic;
      ap_ready : out std_logic;
      layer1_input_V_ap_vld : in std_logic;
      layer1_input_V : in std_logic_vector(879 downto 0);
      layer10_out_0_V : out std_logic_vector(33 downto 0);
      layer10_out_0_V_ap_vld : out std_logic;
      layer10_out_1_V : out std_logic_vector(33 downto 0);
      layer10_out_1_V_ap_vld : out std_logic;
      layer10_out_2_V : out std_logic_vector(33 downto 0);
      layer10_out_2_V_ap_vld : out std_logic;
      layer10_out_3_V : out std_logic_vector(33 downto 0);
      layer10_out_3_V_ap_vld : out std_logic;
      layer10_out_4_V : out std_logic_vector(33 downto 0);
      layer10_out_4_V_ap_vld : out std_logic;
      layer10_out_5_V : out std_logic_vector(33 downto 0);
      layer10_out_5_V_ap_vld : out std_logic;
      layer10_out_6_V : out std_logic_vector(33 downto 0);
      layer10_out_6_V_ap_vld : out std_logic;
      layer10_out_7_V : out std_logic_vector(33 downto 0);
      layer10_out_7_V_ap_vld : out std_logic;
      layer10_out_8_V : out std_logic_vector(33 downto 0);
      layer10_out_8_V_ap_vld : out std_logic;
      layer10_out_9_V : out std_logic_vector(33 downto 0);
      layer10_out_9_V_ap_vld : out std_logic;
      layer10_out_10_V : out std_logic_vector(33 downto 0);
      layer10_out_10_V_ap_vld : out std_logic;
      layer10_out_11_V : out std_logic_vector(33 downto 0);
      layer10_out_11_V_ap_vld : out std_logic;
      layer10_out_12_V : out std_logic_vector(33 downto 0);
      layer10_out_12_V_ap_vld : out std_logic;
      layer10_out_13_V : out std_logic_vector(33 downto 0);
      layer10_out_13_V_ap_vld : out std_logic;
      layer10_out_14_V : out std_logic_vector(33 downto 0);
      layer10_out_14_V_ap_vld : out std_logic;
      layer10_out_15_V : out std_logic_vector(33 downto 0);
      layer10_out_15_V_ap_vld : out std_logic;
      layer10_out_16_V : out std_logic_vector(33 downto 0);
      layer10_out_16_V_ap_vld : out std_logic;
      layer10_out_17_V : out std_logic_vector(33 downto 0);
      layer10_out_17_V_ap_vld : out std_logic;
      layer10_out_18_V : out std_logic_vector(33 downto 0);
      layer10_out_18_V_ap_vld : out std_logic;
      layer10_out_19_V : out std_logic_vector(33 downto 0);
      layer10_out_19_V_ap_vld : out std_logic;
      layer10_out_20_V : out std_logic_vector(33 downto 0);
      layer10_out_20_V_ap_vld : out std_logic;
      layer10_out_21_V : out std_logic_vector(33 downto 0);
      layer10_out_21_V_ap_vld : out std_logic;
      layer10_out_22_V : out std_logic_vector(33 downto 0);
      layer10_out_22_V_ap_vld : out std_logic;
      const_size_in_1 : out std_logic_vector(15 downto 0);
      const_size_in_1_ap_vld : out std_logic;
      const_size_out_1 : out std_logic_vector(15 downto 0);
      const_size_out_1_ap_vld : out std_logic
      );  
  end component myproject;

  constant NUM_INPUTS : integer := 40;
  constant NUM_OUTPUTS : integer := 23;
  
  constant INPUT_WIDTH : integer := 22;
  constant OUTPUT_WIDTH : integer := 34;

  type output is array (NUM_OUTPUTS - 1 downto 0) of std_logic_vector(OUTPUT_WIDTH - 1 downto 0);

  signal in_vld : std_logic;
  signal in_V : std_logic_vector(NUM_INPUTS * INPUT_WIDTH - 1 downto 0);
  signal out_V : output;

  signal d_vld : std_logic_vector(NUM_INPUTS - 1 downto 0);
  signal out_vld : std_logic_vector(NUM_OUTPUTS - 1 downto 0);

begin

  ip: myproject port map (
    ap_clk => clk_p,
    ap_rst => '0',
    ap_start => '1',
    ap_done => open,
    ap_idle => open,
    ap_ready => open,
    layer1_input_V_ap_vld => d_vld(NUM_INPUTS - 1),
    layer1_input_V => in_V,
    layer10_out_0_V => out_V(0),
    layer10_out_0_V_ap_vld => out_vld(0),
    layer10_out_1_V => out_V(1),
    layer10_out_1_V_ap_vld => out_vld(1),
    layer10_out_2_V => out_V(2),
    layer10_out_2_V_ap_vld => out_vld(2),
    layer10_out_3_V => out_V(3),
    layer10_out_3_V_ap_vld => out_vld(3),
    layer10_out_4_V => out_V(4),
    layer10_out_4_V_ap_vld => out_vld(4),
    layer10_out_5_V => out_V(5),
    layer10_out_5_V_ap_vld => out_vld(5),
    layer10_out_6_V => out_V(6),
    layer10_out_6_V_ap_vld => out_vld(6),
    layer10_out_7_V => out_V(7),
    layer10_out_7_V_ap_vld => out_vld(7),
    layer10_out_8_V => out_V(8),
    layer10_out_8_V_ap_vld => out_vld(8),
    layer10_out_9_V => out_V(9),
    layer10_out_9_V_ap_vld => out_vld(9),
    layer10_out_10_V => out_V(10),
    layer10_out_10_V_ap_vld => out_vld(10),
    layer10_out_11_V => out_V(11),
    layer10_out_11_V_ap_vld => out_vld(11),
    layer10_out_12_V => out_V(12),
    layer10_out_12_V_ap_vld => out_vld(12),
    layer10_out_13_V => out_V(13),
    layer10_out_13_V_ap_vld => out_vld(13),
    layer10_out_14_V => out_V(14),
    layer10_out_14_V_ap_vld => out_vld(14),
    layer10_out_15_V => out_V(15),
    layer10_out_15_V_ap_vld => out_vld(15),
    layer10_out_16_V => out_V(16),
    layer10_out_16_V_ap_vld => out_vld(16),
    layer10_out_17_V => out_V(17),
    layer10_out_17_V_ap_vld => out_vld(17),
    layer10_out_18_V => out_V(18),
    layer10_out_18_V_ap_vld => out_vld(18),
    layer10_out_19_V => out_V(19),
    layer10_out_19_V_ap_vld => out_vld(19),
    layer10_out_20_V => out_V(20),
    layer10_out_20_V_ap_vld => out_vld(20),
    layer10_out_21_V => out_V(21),
    layer10_out_21_V_ap_vld => out_vld(21),
    layer10_out_22_V => out_V(22),
    layer10_out_22_V_ap_vld => out_vld(22),
    const_size_in_1 => open,
    const_size_in_1_ap_vld => open,
    const_size_out_1 => open,
    const_size_out_1_ap_vld => open
    );

  ipb_out <= IPB_RBUS_NULL;

  d_vld(0) <= d(0).valid;
  
  gen_d_vld: for i in 1 to NUM_INPUTS - 1 generate
  begin
    d_vld(i) <= d_vld(i - 1) and d(i).valid;
  end generate;

  gen_in_V: for i in 0 to NUM_INPUTS - 1 generate
  begin
    in_V((i + 1) * INPUT_WIDTH - 1 downto i * INPUT_WIDTH) <= d(i).data(INPUT_WIDTH - 1 downto 0);
  end generate;

  gen_q_const: for i in 4 * N_REGION - 1 downto 0 generate
  begin
    q(i).strobe <= '1';
    q(i).start <= '0';
  end generate;

  gen_q: for i in 0 to NUM_OUTPUTS - 1 generate
  begin
    q(i).valid <= out_vld(i);
    q(i).data(LWORD_WIDTH - 1 downto OUTPUT_WIDTH) <= (others => '0');
    q(i).data(OUTPUT_WIDTH - 1 downto 0) <= out_V(i);
  end generate;

  gen_zero: for i in 4 * N_REGION - 1 downto NUM_OUTPUTS generate
  begin
    q(i).data <= (others => '0');
    q(i).valid <= '0';
  end generate;
  
  bc0 <= '0';
  
  gpio <= (others => '0');
  gpio_en <= (others => '0');

end rtl;
