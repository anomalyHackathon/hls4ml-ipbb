-- null_algo
--
-- Do-nothing top level algo for testing
--
-- Dave Newbold, July 2013

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

  component hls4ml_ip is
    port(
      ap_clk : IN STD_LOGIC;
      ap_rst : IN STD_LOGIC;
      ap_start : IN STD_LOGIC;
      ap_done : OUT STD_LOGIC;
      ap_idle : OUT STD_LOGIC;
      ap_ready : OUT STD_LOGIC;
      fc1_input_V_ap_vld : IN STD_LOGIC;
      fc1_input_V : IN STD_LOGIC_VECTOR (255 downto 0);
      layer13_out_0_V : OUT STD_LOGIC_VECTOR (15 downto 0);
      layer13_out_0_V_ap_vld : OUT STD_LOGIC;
      layer13_out_1_V : OUT STD_LOGIC_VECTOR (15 downto 0);
      layer13_out_1_V_ap_vld : OUT STD_LOGIC;
      layer13_out_2_V : OUT STD_LOGIC_VECTOR (15 downto 0);
      layer13_out_2_V_ap_vld : OUT STD_LOGIC;
      layer13_out_3_V : OUT STD_LOGIC_VECTOR (15 downto 0);
      layer13_out_3_V_ap_vld : OUT STD_LOGIC;
      layer13_out_4_V : OUT STD_LOGIC_VECTOR (15 downto 0);
      layer13_out_4_V_ap_vld : OUT STD_LOGIC;
      const_size_in_1 : OUT STD_LOGIC_VECTOR (15 downto 0);
      const_size_in_1_ap_vld : OUT STD_LOGIC;
      const_size_out_1 : OUT STD_LOGIC_VECTOR (15 downto 0);
      const_size_out_1_ap_vld : OUT STD_LOGIC
      );  
  end component hls4ml_ip;

  constant NUM_INPUTS : integer := 16;
  constant NUM_OUTPUTS : integer := 5;
  
  constant INPUT_WIDTH : integer := 16;
  constant OUTPUT_WIDTH : integer := 16;

  type output is array (NUM_OUTPUTS - 1 downto 0) of std_logic_vector(OUTPUT_WIDTH - 1 downto 0);

  signal in_vld : std_logic;
  signal in_V : std_logic_vector(255 downto 0);
  signal out_V : output;

  signal d_vld : std_logic_vector(NUM_INPUTS - 1 downto 0);
  signal out_vld : std_logic_vector(NUM_OUTPUTS - 1 downto 0);

begin

  ip: hls4ml_ip port map (
    ap_clk => clk_p,
    ap_rst => '0',
    ap_start => '1',
    ap_done => open,
    ap_idle => open,
    ap_ready => open,
    fc1_input_V_ap_vld => d_vld(NUM_INPUTS - 1),
    fc1_input_V => in_V,
    layer13_out_0_V => out_V(0),
    layer13_out_0_V_ap_vld => out_vld(0),
    layer13_out_1_V => out_V(1),
    layer13_out_1_V_ap_vld => out_vld(1),
    layer13_out_2_V => out_V(2),
    layer13_out_2_V_ap_vld => out_vld(2),
    layer13_out_3_V => out_V(3),
    layer13_out_3_V_ap_vld => out_vld(3),
    layer13_out_4_V => out_V(4),
    layer13_out_4_V_ap_vld => out_vld(4),
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
    in_V((i + 1) * 16 - 1 downto i * 16) <= d(i).data(INPUT_WIDTH - 1 downto 0);
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
