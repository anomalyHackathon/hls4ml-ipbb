// ==============================================================
// Vivado(TM) HLS - High-Level Synthesis from C, C++ and SystemC v2020.1 (64-bit)
// Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
// ==============================================================

`timescale 1 ns / 1 ps

module myproject_mul_16s_12s_26_2_0_MulnS_29(clk, ce, a, b, p);
input clk;
input ce;
input signed [16 - 1 : 0] a;
input signed [12 - 1 : 0] b;
output[26 - 1 : 0] p;
reg signed [26 - 1 : 0] p;
wire signed [26 - 1 : 0] tmp_product;

assign tmp_product = $signed(a) * $signed(b);
always @ (posedge clk) begin
    if (ce) begin
        p <= tmp_product;
    end
end
endmodule
`timescale 1 ns / 1 ps
module myproject_mul_16s_12s_26_2_0(
    clk,
    reset,
    ce,
    din0,
    din1,
    dout);

parameter ID = 32'd1;
parameter NUM_STAGE = 32'd1;
parameter din0_WIDTH = 32'd1;
parameter din1_WIDTH = 32'd1;
parameter dout_WIDTH = 32'd1;
input clk;
input reset;
input ce;
input[din0_WIDTH - 1:0] din0;
input[din1_WIDTH - 1:0] din1;
output[dout_WIDTH - 1:0] dout;



myproject_mul_16s_12s_26_2_0_MulnS_29 myproject_mul_16s_12s_26_2_0_MulnS_29_U(
    .clk( clk ),
    .ce( ce ),
    .a( din0 ),
    .b( din1 ),
    .p( dout ));

endmodule

