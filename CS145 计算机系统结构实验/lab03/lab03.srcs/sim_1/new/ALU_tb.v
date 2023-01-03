`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/05/19 09:35:22
// Design Name: 
// Module Name: ALU_tb
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


module ALU_tb(

    );
    
    wire Zero;
    wire [31:0] ALURes;
    reg [31:0] Input1;
    reg [31:0] Input2;
    reg [3:0] ALUCtr;

    ALU u0(
        .aluRes(ALURes),
        .input1(Input1),
        .input2(Input2),
        .aluCtr(ALUCtr),
        .zero(Zero)
    );

    initial begin
        ALUCtr = 0;
        Input1 = 0;
        Input2 = 0;
        #100;

        ALUCtr = 0'b0000;
        Input1 = 15;
        Input2 = 10;
        #100;

        ALUCtr = 0'b0001;
        Input1 = 15;
        Input2 = 10;
        #100;

        ALUCtr = 0'b0010;
        Input1 = 15;
        Input2 = 10;
        #100;

        ALUCtr = 0'b0110;
        Input1 = 15;
        Input2 = 10;
        #100;

        ALUCtr = 0'b0110;
        Input1 = 10;
        Input2 = 15;
        #100;

        ALUCtr = 0'b0111;
        Input1 = 15;
        Input2 = 10;
        #100;

        ALUCtr = 0'b0111;
        Input1 = 10;
        Input2 = 15;
        #100;

        ALUCtr = 0'b1100;
        Input1 = 1;
        Input2 = 1;
        #100;

        ALUCtr = 0'b1100;
        Input1 = 16;
        Input2 = 1;
        #100;
    end
    
endmodule
