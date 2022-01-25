`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/05/19 08:08:22
// Design Name: 
// Module Name: Ctr
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


module Ctr(
    input [5:0] opCode,
    output regDst,
    output aluSrc,
    output memToReg,
    output regWrite,
    output memRead,
    output memWrite,
    output branch,
    output [2:0] aluOp,
    output jump,
    output extSign,
    output jalSign
    );

    reg RegDst;
    reg ALUSrc;
    reg MemToReg;
    reg RegWrite;
    reg MemRead;
    reg MemWrite;
    reg Branch;
    reg [2:0] ALUOp;
    reg Jump;
    reg ExtSign;
    reg JalSign;

    always @(opCode)
    begin
        case(opCode)
        6'b000000: //R type
        begin
            RegDst = 1;
            ALUSrc = 0;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            Branch = 0;
            ExtSign = 0;
            JalSign = 0;
            ALUOp = 3'b101;
            Jump = 0;
        end
        6'b100011: //lw
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 1;
            RegWrite = 1;
            MemRead = 1;
            MemWrite = 0;
            Branch = 0;
            ExtSign = 1;
            JalSign = 0;
            ALUOp = 3'b000;
            Jump = 0;
        end
        6'b101011: //sw
        begin
            RegDst = 0; //x
            ALUSrc = 1;
            MemToReg = 0;   //x
            RegWrite = 0;
            MemRead = 0;
            MemWrite = 1;
            Branch = 0;
            ExtSign = 1;
            JalSign = 0;
            ALUOp = 3'b000;
            Jump = 0;
        end
        6'b000100: //beq
        begin
            RegDst = 0; //x
            ALUSrc = 0;
            MemToReg = 0;   //x
            RegWrite = 0;
            MemRead = 0;
            MemWrite = 0;
            Branch = 1;
            ExtSign = 1;
            JalSign = 0;
            ALUOp = 3'b001;
            Jump = 0;
        end
        6'b000010: //jump
        begin
            RegDst = 0;
            ALUSrc = 0;
            MemToReg = 0;
            RegWrite = 0;
            MemRead = 0;
            MemWrite = 0;
            Branch = 0;
            ExtSign = 0;
            JalSign = 0;
            ALUOp = 3'b101;
            Jump = 1;
        end
        6'b000011: //jal
        begin
            RegDst = 0;
            ALUSrc = 0;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            Branch = 0;
            ExtSign = 0;
            JalSign = 1;
            ALUOp = 3'b101;
            Jump = 1;
        end
        6'b001000:      //addi
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            Branch = 0;
            ExtSign = 1;
            JalSign = 0;
            ALUOp = 3'b000; //add
            Jump = 0;
        end
        6'b001001:      //addiu
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            Branch = 0;
            ExtSign = 0;
            JalSign = 0;
            ALUOp = 3'b000; //addiu
            Jump = 0;
        end
        6'b001100:      //andi
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            Branch = 0;
            ExtSign = 0;
            JalSign = 0;
            ALUOp = 3'b011;
            Jump = 0;
        end
        6'b001101:      //ori
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            Branch = 0;
            ExtSign = 0;
            JalSign = 0;
            ALUOp = 3'b100;
            Jump = 0;
        end
        6'b001101:      //xori
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            Branch = 0;
            ExtSign = 0;
            JalSign = 0;
            ALUOp = 3'b111;
            Jump = 0;
        end
        6'b001010:      //slti
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            Branch = 0;
            ExtSign = 1;
            JalSign = 0;
            ALUOp = 3'b010;
            Jump = 0;
        end
        6'b001011:      //sltiu
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            Branch = 0;
            ExtSign = 0;
            JalSign = 0;
            ALUOp = 3'b110;
            Jump = 0;
        end
        default:
        begin
            RegDst = 0;
            ALUSrc = 0;
            MemToReg = 0;
            RegWrite = 0;
            MemRead = 0;
            MemWrite = 0;
            Branch = 0;
            ALUOp = 2'b000;
            Jump = 0;
        end
        endcase
    end

    assign regDst = RegDst;
    assign aluSrc = ALUSrc;
    assign memToReg = MemToReg;
    assign regWrite = RegWrite;
    assign memRead = MemRead;
    assign memWrite = MemWrite;
    assign branch = Branch;
    assign aluOp = ALUOp;
    assign jump = Jump;
    assign extSign = ExtSign;
    assign jalSign = JalSign;
endmodule
