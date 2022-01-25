`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/05/19 10:20:37
// Design Name: 
// Module Name: dataMemory
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


module dataMemory(
    input clk,
    input [31:0] address,
    input [31:0] writeData,
    input memWrite,
    input memRead,
    output [127:0] readData
    );

    reg [31:0] memFile [0:1023];
    reg [127:0] ReadData;
    always @(memRead or address or memWrite) 
    begin
        if(memRead)
        begin
            if(address<1023)
                ReadData = {memFile[address],memFile[address+1],memFile[address+2],memFile[address+3]};
            else
                ReadData = 0;
        end
    end

    always @(negedge clk)
    begin
        if(memWrite)
            if(address<1023)
                memFile[address] = writeData;
    end

    assign readData = ReadData;
endmodule
