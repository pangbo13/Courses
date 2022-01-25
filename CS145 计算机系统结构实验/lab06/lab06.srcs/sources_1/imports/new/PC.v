`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/05/26 08:15:46
// Design Name: 
// Module Name: PC
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


module PC(
    input [31:0] pcIn,
    input clk,
    input reset,
    output [31:0] pcOut
    );
    
    reg [31:0] PC;
    
    initial PC = 0;
    
    always @ (posedge clk or reset)
    begin
        if(reset)
            PC = 0;
        else
            PC = pcIn;
    end
    assign pcOut = PC;
endmodule
