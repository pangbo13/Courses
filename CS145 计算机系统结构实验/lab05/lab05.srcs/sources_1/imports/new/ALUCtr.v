`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/05/19 08:55:06
// Design Name: 
// Module Name: ALUCtr
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


module ALUCtr(
    input [2:0] aluOp,
    input [5:0] funct,
    output [3:0] aluCtrOut,
    output shamtSign,
    output jrSign
    );

    reg [3:0] ALUCtrOut;
    reg ShamtSign;
    reg JrSign;
    //AND:0000
    //OR:0001
    //ADD:0010
    //Left-shift:0011
    //Right-shift:0100
    //No-change:0101
    //SUB:0110
    //SLT:0111
    //NOR:1100
    always @ (aluOp or funct)
    begin
        ShamtSign = 0;
        JrSign = 0;
        casex({aluOp,funct})
            9'b000xxxxxx:  // lw,sw,add,addiu
                ALUCtrOut = 4'b0010;    //add
            9'b001xxxxxx:  // beq
                ALUCtrOut = 4'b0110;    //sub
            9'b010xxxxxx:   //stli
                ALUCtrOut = 4'b0111;
            9'b110xxxxxx:   //stliu
                ALUCtrOut = 4'b1000;
            9'b011xxxxxx:  // andi
                ALUCtrOut = 4'b0000;
            9'b100xxxxxx:  // ori
                ALUCtrOut = 4'b0001;
            9'b111xxxxxx:  // xori
                ALUCtrOut = 4'b1011;
            
            //R type
            9'b101001000:  // jr
            begin
                ALUCtrOut = 4'b0101;
                JrSign = 1;
            end
            9'b101000000:  // sll
            begin
                ALUCtrOut = 4'b0011;
                ShamtSign = 1;
            end
            9'b101000010:  // srl
            begin
                ALUCtrOut = 4'b0100;
                ShamtSign = 1;
            end
            9'b101000011:  // sra
            begin
                ALUCtrOut = 4'b1110;
                ShamtSign = 1;
            end
            9'b101000100:  // sllv
                ALUCtrOut = 4'b0011;
            9'b101000110:  // srlv
                ALUCtrOut = 4'b0100;
            9'b101000111:  // srav
                ALUCtrOut = 4'b1110;

            9'b101100000:  // add
                ALUCtrOut = 4'b0010;
            9'b101100001:  // addu
                ALUCtrOut = 4'b0010;
            9'b101100010:  // sub
                ALUCtrOut = 4'b0110;
            9'b101100011:  // subu
                ALUCtrOut = 4'b0110;
            9'b101100100:  // and
                ALUCtrOut = 4'b0000;
            9'b101100101:  // or
                ALUCtrOut = 4'b0001;
            9'b101100110:  // xor
                ALUCtrOut = 4'b1011;
            9'b101100111:  // nor
                ALUCtrOut = 4'b1100;
            9'b101101010:  // slt
                ALUCtrOut = 4'b0111;
            9'b101101011:  // sltu
                ALUCtrOut = 4'b1000;
        endcase
    end
    
    assign aluCtrOut = ALUCtrOut;
    assign shamtSign = ShamtSign;
    assign jrSign = JrSign;

endmodule
