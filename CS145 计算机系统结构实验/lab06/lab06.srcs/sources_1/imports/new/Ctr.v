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
    input [5:0] funct,
    output regDst,
    output aluSrc,
    output memToReg,
    output regWrite,
    output memRead,
    output memWrite,
    output [2:0] aluOp,
    output extSign,
    output luiSign,
    output jumpSign,
    output jrSign,
    output jalSign,
    output beqSign,
    output bneSign
    );

    reg RegDst;
    reg ALUSrc;
    reg MemToReg;
    reg RegWrite;
    reg MemRead;
    reg MemWrite;
    reg LuiSign;
    reg BeqSign;
    reg BneSign;
    reg [2:0] ALUOp;
    reg JumpSign;
    reg JrSign;
    reg ExtSign;
    reg JalSign;

    always @(opCode or funct)
    begin
        case(opCode)
        6'b000000: //R type
        begin
            RegDst = 1;
            ALUSrc = 0;
            MemToReg = 0;
            MemRead = 0;
            MemWrite = 0;
            BeqSign = 0;
            BneSign = 0;
            ExtSign = 0;
            LuiSign = 0;
            JalSign = 0;
            ALUOp = 3'b101;
            JumpSign = 0;
            if (funct == 6'b001000) begin
                RegWrite = 0;
                JrSign = 1;
            end else begin
                RegWrite = 1;
                JrSign = 0;
            end
        end
        6'b100011: //lw
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 1;
            RegWrite = 1;
            MemRead = 1;
            MemWrite = 0;
            BeqSign = 0;
            BneSign = 0;
            ExtSign = 1;
            LuiSign = 0;
            JalSign = 0;
            ALUOp = 3'b000;
            JumpSign = 0;
            JrSign = 0;
        end
        6'b101011: //sw
        begin
            RegDst = 0; //x
            ALUSrc = 1;
            MemToReg = 0;   //x
            RegWrite = 0;
            MemRead = 0;
            MemWrite = 1;
            BeqSign = 0;
            BneSign = 0;
            ExtSign = 1;
            LuiSign = 0;
            JalSign = 0;
            ALUOp = 3'b000;
            JumpSign = 0;
            JrSign = 0;
        end
        6'b000100: //beq
        begin
            RegDst = 0; //x
            ALUSrc = 0;
            MemToReg = 0;   //x
            RegWrite = 0;
            MemRead = 0;
            MemWrite = 0;
            BeqSign = 1;
            BneSign = 0;
            ExtSign = 1;
            LuiSign = 0;
            JalSign = 0;
            ALUOp = 3'b001;
            JumpSign = 0;
            JrSign = 0;
        end
        6'b000101: //bne
        begin
            RegDst = 0; //x
            ALUSrc = 0;
            MemToReg = 0;   //x
            RegWrite = 0;
            MemRead = 0;
            MemWrite = 0;
            BeqSign = 0;
            BneSign = 1;
            ExtSign = 1;
            LuiSign = 0;
            JalSign = 0;
            ALUOp = 3'b001;
            JumpSign = 0;
            JrSign = 0;
        end
        6'b000010: //jump
        begin
            RegDst = 0;
            ALUSrc = 0;
            MemToReg = 0;
            RegWrite = 0;
            MemRead = 0;
            MemWrite = 0;
            BeqSign = 0;
            BneSign = 0;
            ExtSign = 0;
            LuiSign = 0;
            JalSign = 0;
            ALUOp = 3'b000;
            JumpSign = 1;
            JrSign = 0;
        end
        6'b000011: //jal
        begin
            RegDst = 0;
            ALUSrc = 0;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            BeqSign = 0;
            BneSign = 0;
            ExtSign = 0;
            LuiSign = 0;
            JalSign = 1;
            ALUOp = 3'b000;
            JumpSign = 1;
            JrSign = 0;
        end
        6'b001000:      //addi
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            BeqSign = 0;
            BneSign = 0;
            ExtSign = 1;
            LuiSign = 0;
            JalSign = 0;
            ALUOp = 3'b000; //add
            JumpSign = 0;
            JrSign = 0;
        end
        6'b001001:      //addiu
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            BeqSign = 0;
            BneSign = 0;
            ExtSign = 0;
            LuiSign = 0;
            JalSign = 0;
            ALUOp = 3'b000; //addiu
            JumpSign = 0;
            JrSign = 0;
        end
        6'b001100:      //andi
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            BeqSign = 0;
            BneSign = 0;
            ExtSign = 0;
            LuiSign = 0;
            JalSign = 0;
            ALUOp = 3'b011;
            JumpSign = 0;
            JrSign = 0;
        end
        6'b001101:      //ori
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            BeqSign = 0;
            BneSign = 0;
            ExtSign = 0;
            LuiSign = 0;
            JalSign = 0;
            ALUOp = 3'b100;
            JumpSign = 0;
            JrSign = 0;
        end
        6'b001110:      //xori
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            BeqSign = 0;
            BneSign = 0;
            ExtSign = 0;
            LuiSign = 0;
            JalSign = 0;
            ALUOp = 3'b111;
            JumpSign = 0;
            JrSign = 0;
        end
        6'b001111:      //lui
        begin
            RegDst = 0;
            ALUSrc = 0;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            BeqSign = 0;
            BneSign = 0;
            ExtSign = 0;
            LuiSign = 1;
            JalSign = 0;
            ALUOp = 3'b000;
            JumpSign = 0;
            JrSign = 0;
        end
        6'b001010:      //slti
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            BeqSign = 0;
            BneSign = 0;
            ExtSign = 1;
            LuiSign = 0;
            JalSign = 0;
            ALUOp = 3'b010;
            JumpSign = 0;
            JrSign = 0;
        end
        6'b001011:      //sltiu
        begin
            RegDst = 0;
            ALUSrc = 1;
            MemToReg = 0;
            RegWrite = 1;
            MemRead = 0;
            MemWrite = 0;
            BeqSign = 0;
            BneSign = 0;
            ExtSign = 0;
            LuiSign = 0;
            JalSign = 0;
            ALUOp = 3'b110;
            JumpSign = 0;
            JrSign = 0;
        end
        default:
        begin
            RegDst = 0;
            ALUSrc = 0;
            MemToReg = 0;
            RegWrite = 0;
            MemRead = 0;
            MemWrite = 0;
            ALUOp = 2'b00;
            JumpSign = 0;
            JrSign = 0;
        end
        endcase
    end

    assign regDst = RegDst;
    assign aluSrc = ALUSrc;
    assign memToReg = MemToReg;
    assign regWrite = RegWrite;
    assign memRead = MemRead;
    assign memWrite = MemWrite;
    // assign branch = Branch;
    assign aluOp = ALUOp;
    assign jumpSign = JumpSign;
    assign jrSign = JrSign;
    assign extSign = ExtSign;
    assign luiSign = LuiSign;
    assign jalSign = JalSign;

    assign beqSign = BeqSign;
    assign bneSign = BneSign;
    
endmodule
