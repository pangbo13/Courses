
module display (
	input wire clk,  // main clock
	input wire rst,  // synchronous reset
	input wire [7:0] en,  // enable for each tube
	input wire [31:0] data,  // data to display
	input wire [7:0] dot,  // enable for each dot
	input wire [15:0] led,  // LED display
	// LED interfaces
	output wire led_clk,
	output wire led_en,
	output wire led_clr_n,
	output wire led_do,
	// 7-segment tube interfaces
	output wire seg_clk,
	output wire seg_en,
	output wire seg_clr_n,
	output wire seg_do
);

endmodule
