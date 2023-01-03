`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/05/19 09:25:54
// Design Name: 
// Module Name: ALU
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


module ALU(
    input [31:0] input1,
    input [31:0] input2,
    input [3:0] aluCtr,
    output [31:0] aluRes,
    output zero
    );

    reg Zero;
    reg [31:0] ALURes;

    always @ (input1 or input2 or aluCtr)
    begin
        case(aluCtr)
        4'b0000:    //AND
            ALURes = input1 & input2;
        4'b0001:    //OR
            ALURes = input1 | input2;
        4'b0010:    //ADD
            ALURes = input1 + input2;
        4'b0110:    //SUB
            ALURes = input1 - input2;
        4'b0111:    //SLT
            ALURes = ($signed(input1) < $signed(input2));
        4'b1100:    //nor
            ALURes = ~(input1 | input2);
        endcase
        if(ALURes==0)
            Zero = 1;
        else
            Zero = 0;
    end

    assign zero = Zero;
    assign aluRes = ALURes;
endmodule
