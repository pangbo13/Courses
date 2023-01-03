`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/06/06 12:52:13
// Design Name: 
// Module Name: Cache
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


module Cache(
    input clk,
    input [31:0] address,
    input [31:0] writeData,
    input memWrite,
    input memRead,
    output [31:0] readData
    );
    reg[31:0] cacheFile[0:63];
    reg validBit[0:15];
    reg[25:0] tag[0:15];

    reg[31:0] ReadData;

    wire[127:0] dataFromMemFile;

    wire[3:0] cacheAddr = address[5:2];
    wire[31:0] MemFileAddress = {address[31:2],2'b00};
    integer i;
    dataMemory mem(
        .clk(clk),
        .address(MemFileAddress),
        .writeData(writeData),
        .memWrite(memWrite),
        .memRead(memRead),
        .readData(dataFromMemFile)
    );

    initial 
    begin
        for(i=0;i<64;i=i+1)
            validBit[i] = 1'b0;
            tag[i] = 16'b0;
    end

    always @(memRead or address or memWrite) 
    begin
        if(memRead)
        begin
            if(validBit[cacheAddr] & tag[cacheAddr] == address[31:6])
                ReadData = cacheFile[address[5:0]];
            else begin
                tag[cacheAddr] = address[31:6];
                validBit[cacheAddr] = 1'b1;
                #5
                cacheFile[{cacheAddr,2'b11}] = dataFromMemFile[31:0];
                cacheFile[{cacheAddr,2'b10}] = dataFromMemFile[63:32];
                cacheFile[{cacheAddr,2'b01}] = dataFromMemFile[95:64];
                cacheFile[{cacheAddr,2'b00}] = dataFromMemFile[127:96];
                ReadData = cacheFile[address[5:0]];
            end
        end
    end

    always @(negedge clk)
    begin
        if(memWrite)
            validBit[cacheAddr] = 1'b0;
    end

    assign readData = ReadData;
endmodule
