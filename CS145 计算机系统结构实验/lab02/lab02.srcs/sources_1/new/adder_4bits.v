`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/05/12 10:28:27
// Design Name: 
// Module Name: adder_4bits
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


module adder_4bits(
    input [3:0] a,
    input [3:0] b,
    input ci,
    output [3:0] s,
    output co
    );
    wire [20:0] ct;
    adder_1bit  a1(.a(a[0]),.b(b[0]),.ci(ci),.s(s[0]),.co(ct[0])),
                a2(.a(a[1]),.b(b[1]),.ci(ct[0]),.s(s[1]),.co(ct[1])),
                a3(.a(a[2]),.b(b[2]),.ci(ct[1]),.s(s[2]),.co(ct[2])),
                a4(.a(a[3]),.b(b[3]),.ci(ct[2]),.s(s[3]),.co(co));
endmodule
