`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/05/12 10:39:17
// Design Name: 
// Module Name: Top
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module Top(
    input clk_p,
    input clk_n,
    input [3:0] a,
    input [3:0] b,
    input reset,
    
    output led_clk,
    output led_do,
    output led_en,
    
    output wire seg_clk,
    output wire seg_en,
    output wire seg_do
    );
    wire CLK_i;
    wire Clk_25M;
    
    IBUFGDS IBUFGDS_inst(
        .O(CLK_i),
        .I(clk_p),
        .IB(clk_n)
    );
    
    wire [3:0] s;
    wire co;
    wire [4:0] sum;
    assign sum = {co,s};
    
    adder_4bits U1(
        .a(a),
        .b(b),
        .ci(1'b0),
        .s(s),
        .co(co)
    );
    reg [1:0] clkdiv;
    always @ (posedge CLK_i)
        clkdiv<=clkdiv+1;
    assign Clk_25M=clkdiv[1];
    
    display DISPLAY(
        .clk(Clk_25M),
        .rst(1'b0),
        .en(8'b00000011),
        .data({27'b0,sum}),
        .dot(8'b00000000),
        .led(~{11'b0,sum}),
        .led_clk(led_clk),
        .led_en(led_en),
        .led_do(led_do),
        .seg_clk(seg_clk),
        .seg_en(seg_en),
        .seg_do(seg_do)
    );
endmodule
