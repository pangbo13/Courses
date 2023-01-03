//`include "define.vh" 问题 2v

module parallel2serial (
	input wire clk,  // main clock
	input wire rst,  // synchronous reset
	input wire [DATA_BITS-1:0] data,  // parallel input data
	input wire start,  // start command
	output wire busy,  // busy flag
    output wire finish,  // finish acknowledgement
    output wire s_clk,  // serial clock
    output wire s_clr,  // serial clear
    output wire s_dat  // serial output data ；从reg到wire
	);

	parameter
		P_CLK_FREQ = 200,  // main clock frequency in MHz
		S_CLK_FREQ = 20,  // serial clock frequency in MHz
		DATA_BITS = 16,  // data length
		CODE_ENDIAN = 1;  // 0 for little-endian and 1 for big-endian
	localparam
		COUNT_HALFCYCLE = 1 + (P_CLK_FREQ-1) / S_CLK_FREQ / 2;



endmodule
