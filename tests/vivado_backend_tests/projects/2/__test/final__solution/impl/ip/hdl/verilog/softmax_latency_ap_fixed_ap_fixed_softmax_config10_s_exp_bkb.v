// ==============================================================
// Vivado(TM) HLS - High-Level Synthesis from C, C++ and SystemC v2020.1 (64-bit)
// Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
// ==============================================================
`timescale 1 ns / 1 ps
(* rom_style = "block" *) module softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom (
addr0, ce0, q0, addr1, ce1, q1, addr2, ce2, q2, addr3, ce3, q3, addr4, ce4, q4, addr5, ce5, q5, addr6, ce6, q6, addr7, ce7, q7, addr8, ce8, q8, addr9, ce9, q9, addr10, ce10, q10, addr11, ce11, q11, addr12, ce12, q12, addr13, ce13, q13, addr14, ce14, q14, addr15, ce15, q15, addr16, ce16, q16, addr17, ce17, q17, addr18, ce18, q18, addr19, ce19, q19, addr20, ce20, q20, addr21, ce21, q21, addr22, ce22, q22, clk);

parameter DWIDTH = 18;
parameter AWIDTH = 10;
parameter MEM_SIZE = 1024;

input[AWIDTH-1:0] addr0;
input ce0;
output reg[DWIDTH-1:0] q0;
input[AWIDTH-1:0] addr1;
input ce1;
output reg[DWIDTH-1:0] q1;
input[AWIDTH-1:0] addr2;
input ce2;
output reg[DWIDTH-1:0] q2;
input[AWIDTH-1:0] addr3;
input ce3;
output reg[DWIDTH-1:0] q3;
input[AWIDTH-1:0] addr4;
input ce4;
output reg[DWIDTH-1:0] q4;
input[AWIDTH-1:0] addr5;
input ce5;
output reg[DWIDTH-1:0] q5;
input[AWIDTH-1:0] addr6;
input ce6;
output reg[DWIDTH-1:0] q6;
input[AWIDTH-1:0] addr7;
input ce7;
output reg[DWIDTH-1:0] q7;
input[AWIDTH-1:0] addr8;
input ce8;
output reg[DWIDTH-1:0] q8;
input[AWIDTH-1:0] addr9;
input ce9;
output reg[DWIDTH-1:0] q9;
input[AWIDTH-1:0] addr10;
input ce10;
output reg[DWIDTH-1:0] q10;
input[AWIDTH-1:0] addr11;
input ce11;
output reg[DWIDTH-1:0] q11;
input[AWIDTH-1:0] addr12;
input ce12;
output reg[DWIDTH-1:0] q12;
input[AWIDTH-1:0] addr13;
input ce13;
output reg[DWIDTH-1:0] q13;
input[AWIDTH-1:0] addr14;
input ce14;
output reg[DWIDTH-1:0] q14;
input[AWIDTH-1:0] addr15;
input ce15;
output reg[DWIDTH-1:0] q15;
input[AWIDTH-1:0] addr16;
input ce16;
output reg[DWIDTH-1:0] q16;
input[AWIDTH-1:0] addr17;
input ce17;
output reg[DWIDTH-1:0] q17;
input[AWIDTH-1:0] addr18;
input ce18;
output reg[DWIDTH-1:0] q18;
input[AWIDTH-1:0] addr19;
input ce19;
output reg[DWIDTH-1:0] q19;
input[AWIDTH-1:0] addr20;
input ce20;
output reg[DWIDTH-1:0] q20;
input[AWIDTH-1:0] addr21;
input ce21;
output reg[DWIDTH-1:0] q21;
input[AWIDTH-1:0] addr22;
input ce22;
output reg[DWIDTH-1:0] q22;
input clk;

(* ram_style = "block" *)reg [DWIDTH-1:0] ram0[0:MEM_SIZE-1];
(* ram_style = "block" *)reg [DWIDTH-1:0] ram1[0:MEM_SIZE-1];
(* ram_style = "block" *)reg [DWIDTH-1:0] ram2[0:MEM_SIZE-1];
(* ram_style = "block" *)reg [DWIDTH-1:0] ram3[0:MEM_SIZE-1];
(* ram_style = "block" *)reg [DWIDTH-1:0] ram4[0:MEM_SIZE-1];
(* ram_style = "block" *)reg [DWIDTH-1:0] ram5[0:MEM_SIZE-1];
(* ram_style = "block" *)reg [DWIDTH-1:0] ram6[0:MEM_SIZE-1];
(* ram_style = "block" *)reg [DWIDTH-1:0] ram7[0:MEM_SIZE-1];
(* ram_style = "block" *)reg [DWIDTH-1:0] ram8[0:MEM_SIZE-1];
(* ram_style = "block" *)reg [DWIDTH-1:0] ram9[0:MEM_SIZE-1];
(* ram_style = "block" *)reg [DWIDTH-1:0] ram10[0:MEM_SIZE-1];
(* ram_style = "block" *)reg [DWIDTH-1:0] ram11[0:MEM_SIZE-1];

initial begin
    $readmemh("./softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom.dat", ram0);
    $readmemh("./softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom.dat", ram1);
    $readmemh("./softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom.dat", ram2);
    $readmemh("./softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom.dat", ram3);
    $readmemh("./softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom.dat", ram4);
    $readmemh("./softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom.dat", ram5);
    $readmemh("./softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom.dat", ram6);
    $readmemh("./softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom.dat", ram7);
    $readmemh("./softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom.dat", ram8);
    $readmemh("./softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom.dat", ram9);
    $readmemh("./softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom.dat", ram10);
    $readmemh("./softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom.dat", ram11);
end



always @(posedge clk)  
begin 
    if (ce0) 
    begin
        q0 <= ram0[addr0];
    end
end



always @(posedge clk)  
begin 
    if (ce1) 
    begin
        q1 <= ram0[addr1];
    end
end



always @(posedge clk)  
begin 
    if (ce2) 
    begin
        q2 <= ram1[addr2];
    end
end



always @(posedge clk)  
begin 
    if (ce3) 
    begin
        q3 <= ram1[addr3];
    end
end



always @(posedge clk)  
begin 
    if (ce4) 
    begin
        q4 <= ram2[addr4];
    end
end



always @(posedge clk)  
begin 
    if (ce5) 
    begin
        q5 <= ram2[addr5];
    end
end



always @(posedge clk)  
begin 
    if (ce6) 
    begin
        q6 <= ram3[addr6];
    end
end



always @(posedge clk)  
begin 
    if (ce7) 
    begin
        q7 <= ram3[addr7];
    end
end



always @(posedge clk)  
begin 
    if (ce8) 
    begin
        q8 <= ram4[addr8];
    end
end



always @(posedge clk)  
begin 
    if (ce9) 
    begin
        q9 <= ram4[addr9];
    end
end



always @(posedge clk)  
begin 
    if (ce10) 
    begin
        q10 <= ram5[addr10];
    end
end



always @(posedge clk)  
begin 
    if (ce11) 
    begin
        q11 <= ram5[addr11];
    end
end



always @(posedge clk)  
begin 
    if (ce12) 
    begin
        q12 <= ram6[addr12];
    end
end



always @(posedge clk)  
begin 
    if (ce13) 
    begin
        q13 <= ram6[addr13];
    end
end



always @(posedge clk)  
begin 
    if (ce14) 
    begin
        q14 <= ram7[addr14];
    end
end



always @(posedge clk)  
begin 
    if (ce15) 
    begin
        q15 <= ram7[addr15];
    end
end



always @(posedge clk)  
begin 
    if (ce16) 
    begin
        q16 <= ram8[addr16];
    end
end



always @(posedge clk)  
begin 
    if (ce17) 
    begin
        q17 <= ram8[addr17];
    end
end



always @(posedge clk)  
begin 
    if (ce18) 
    begin
        q18 <= ram9[addr18];
    end
end



always @(posedge clk)  
begin 
    if (ce19) 
    begin
        q19 <= ram9[addr19];
    end
end



always @(posedge clk)  
begin 
    if (ce20) 
    begin
        q20 <= ram10[addr20];
    end
end



always @(posedge clk)  
begin 
    if (ce21) 
    begin
        q21 <= ram10[addr21];
    end
end



always @(posedge clk)  
begin 
    if (ce22) 
    begin
        q22 <= ram11[addr22];
    end
end



endmodule

`timescale 1 ns / 1 ps
module softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb(
    reset,
    clk,
    address0,
    ce0,
    q0,
    address1,
    ce1,
    q1,
    address2,
    ce2,
    q2,
    address3,
    ce3,
    q3,
    address4,
    ce4,
    q4,
    address5,
    ce5,
    q5,
    address6,
    ce6,
    q6,
    address7,
    ce7,
    q7,
    address8,
    ce8,
    q8,
    address9,
    ce9,
    q9,
    address10,
    ce10,
    q10,
    address11,
    ce11,
    q11,
    address12,
    ce12,
    q12,
    address13,
    ce13,
    q13,
    address14,
    ce14,
    q14,
    address15,
    ce15,
    q15,
    address16,
    ce16,
    q16,
    address17,
    ce17,
    q17,
    address18,
    ce18,
    q18,
    address19,
    ce19,
    q19,
    address20,
    ce20,
    q20,
    address21,
    ce21,
    q21,
    address22,
    ce22,
    q22);

parameter DataWidth = 32'd18;
parameter AddressRange = 32'd1024;
parameter AddressWidth = 32'd10;
input reset;
input clk;
input[AddressWidth - 1:0] address0;
input ce0;
output[DataWidth - 1:0] q0;
input[AddressWidth - 1:0] address1;
input ce1;
output[DataWidth - 1:0] q1;
input[AddressWidth - 1:0] address2;
input ce2;
output[DataWidth - 1:0] q2;
input[AddressWidth - 1:0] address3;
input ce3;
output[DataWidth - 1:0] q3;
input[AddressWidth - 1:0] address4;
input ce4;
output[DataWidth - 1:0] q4;
input[AddressWidth - 1:0] address5;
input ce5;
output[DataWidth - 1:0] q5;
input[AddressWidth - 1:0] address6;
input ce6;
output[DataWidth - 1:0] q6;
input[AddressWidth - 1:0] address7;
input ce7;
output[DataWidth - 1:0] q7;
input[AddressWidth - 1:0] address8;
input ce8;
output[DataWidth - 1:0] q8;
input[AddressWidth - 1:0] address9;
input ce9;
output[DataWidth - 1:0] q9;
input[AddressWidth - 1:0] address10;
input ce10;
output[DataWidth - 1:0] q10;
input[AddressWidth - 1:0] address11;
input ce11;
output[DataWidth - 1:0] q11;
input[AddressWidth - 1:0] address12;
input ce12;
output[DataWidth - 1:0] q12;
input[AddressWidth - 1:0] address13;
input ce13;
output[DataWidth - 1:0] q13;
input[AddressWidth - 1:0] address14;
input ce14;
output[DataWidth - 1:0] q14;
input[AddressWidth - 1:0] address15;
input ce15;
output[DataWidth - 1:0] q15;
input[AddressWidth - 1:0] address16;
input ce16;
output[DataWidth - 1:0] q16;
input[AddressWidth - 1:0] address17;
input ce17;
output[DataWidth - 1:0] q17;
input[AddressWidth - 1:0] address18;
input ce18;
output[DataWidth - 1:0] q18;
input[AddressWidth - 1:0] address19;
input ce19;
output[DataWidth - 1:0] q19;
input[AddressWidth - 1:0] address20;
input ce20;
output[DataWidth - 1:0] q20;
input[AddressWidth - 1:0] address21;
input ce21;
output[DataWidth - 1:0] q21;
input[AddressWidth - 1:0] address22;
input ce22;
output[DataWidth - 1:0] q22;



softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom softmax_latency_ap_fixed_ap_fixed_softmax_config10_s_exp_bkb_rom_U(
    .clk( clk ),
    .addr0( address0 ),
    .ce0( ce0 ),
    .q0( q0 ),
    .addr1( address1 ),
    .ce1( ce1 ),
    .q1( q1 ),
    .addr2( address2 ),
    .ce2( ce2 ),
    .q2( q2 ),
    .addr3( address3 ),
    .ce3( ce3 ),
    .q3( q3 ),
    .addr4( address4 ),
    .ce4( ce4 ),
    .q4( q4 ),
    .addr5( address5 ),
    .ce5( ce5 ),
    .q5( q5 ),
    .addr6( address6 ),
    .ce6( ce6 ),
    .q6( q6 ),
    .addr7( address7 ),
    .ce7( ce7 ),
    .q7( q7 ),
    .addr8( address8 ),
    .ce8( ce8 ),
    .q8( q8 ),
    .addr9( address9 ),
    .ce9( ce9 ),
    .q9( q9 ),
    .addr10( address10 ),
    .ce10( ce10 ),
    .q10( q10 ),
    .addr11( address11 ),
    .ce11( ce11 ),
    .q11( q11 ),
    .addr12( address12 ),
    .ce12( ce12 ),
    .q12( q12 ),
    .addr13( address13 ),
    .ce13( ce13 ),
    .q13( q13 ),
    .addr14( address14 ),
    .ce14( ce14 ),
    .q14( q14 ),
    .addr15( address15 ),
    .ce15( ce15 ),
    .q15( q15 ),
    .addr16( address16 ),
    .ce16( ce16 ),
    .q16( q16 ),
    .addr17( address17 ),
    .ce17( ce17 ),
    .q17( q17 ),
    .addr18( address18 ),
    .ce18( ce18 ),
    .q18( q18 ),
    .addr19( address19 ),
    .ce19( ce19 ),
    .q19( q19 ),
    .addr20( address20 ),
    .ce20( ce20 ),
    .q20( q20 ),
    .addr21( address21 ),
    .ce21( ce21 ),
    .q21( q21 ),
    .addr22( address22 ),
    .ce22( ce22 ),
    .q22( q22 ));

endmodule

