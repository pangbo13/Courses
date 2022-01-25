`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/05/19 10:27:35
// Design Name: 
// Module Name: dataMemory_tb
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


module dataMemory_tb(

    );
    
    reg Clk;
    reg [31 : 0] Address;
    reg [31 : 0] WriteData;
    reg MemWrite;
    reg MemRead;
    wire [31 : 0] ReadData;
    
    dataMemory u0(
        .clk(Clk),
        .address(Address),
        .writeData(WriteData),
        .memWrite(MemWrite),
        .memRead(MemRead),
        .readData(ReadData)
    );
    
    always #100 Clk = ~Clk;
    
    initial begin
        Clk = 0;
        Address = 0;
        WriteData = 0;
        MemWrite = 0;
        MemRead = 0;
        
        #185;

        //185
        MemRead = 0;
        MemWrite = 1;
        Address = 32'b00000000000000000000000000000111;
        WriteData = 32'b11100000000000000000000000000000;
        #100;

        //285
        MemRead = 0;
        MemWrite = 1;
        WriteData = 32'hffffffff;
        Address = 32'b00000000000000000000000000000110;
        #185;

        //470
        MemRead = 1;
        MemWrite = 0;
        #80;

        //550
        MemRead = 1;
        MemWrite = 1;
        Address = 8;
        WriteData = 32'haaaaaaaa;
        #80;

        //630
        MemWrite = 0;
        MemRead = 1;
    end
endmodule
