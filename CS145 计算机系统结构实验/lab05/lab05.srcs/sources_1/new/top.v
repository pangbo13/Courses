`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/05/26 08:04:59
// Design Name: 
// Module Name: top
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


module top(
    input clk,
    input reset
    );
    wire REG_DST;
    wire REG_WRITE;
    wire EXT_OP;
    wire ALU_SRC;
    wire[2:0] ALU_OP;
    wire[3:0] ALU_CTR;
    wire BRANCH;
    wire JUMP;
    wire JAL_SIGN;
    wire MEM_WRITE;
    wire MEM_READ;
    wire MEM_TO_REG;
    wire ALU_ZERO;
    wire SHAMT_SIGN;
    wire JR_SIGN;
    wire[4:0] WRITE_REG_ID;
    wire[4:0] WRITE_REG_ID_AFTER_JAL_MUX;

    wire[31:0] INST;
    wire[31:0] REG_WRITE_DATA_AFTER_JAL_MUX;
    wire[31:0] REG_WRITE_DATA;
    wire[31:0] REG_READ_DATA1;
    wire[31:0] REG_READ_DATA2;
    wire[31:0] EXT_IMM;
    wire[31:0] ALU_INPUT1;
    wire[31:0] ALU_INPUT2;
    wire[31:0] ALU_OUTPUT;
    wire[31:0] MEM_OUTPUT_DATA;
    wire[31:0] MEM_INPUT_DATA;
    wire[31:0] PC_IN;
    wire[31:0] PC_OUT;
    wire[31:0] PC_AFTER_BRANCH_MUX;
    wire[31:0] PC_AFTER_JR_MUX;
    wire[31:0] JUMP_ADDR;

    assign MEM_INPUT_DATA = REG_READ_DATA2;

    Ctr main_ctr(
        .opCode(INST[31:26]),
        .regDst(REG_DST),
        .aluSrc(ALU_SRC),
        .memToReg(MEM_TO_REG),
        .regWrite(REG_WRITE),
        .memRead(MEM_READ),
        .memWrite(MEM_WRITE),
        .branch(BRANCH),
        .aluOp(ALU_OP),
        .jump(JUMP),
        .extSign(EXT_OP),
        .jalSign(JAL_SIGN)
    );

    RegMux reg_dst_mux(
        .input0(INST[20:16]),
        .input1(INST[15:11]),
        .select(REG_DST),
        .out(WRITE_REG_ID)
    );

    Mux alu_src_mux(
        .input0(REG_READ_DATA2),
        .input1(EXT_IMM),
        .select(ALU_SRC),
        .out(ALU_INPUT2)
    );

    Mux mem_to_reg_mux(
        .input0(ALU_OUTPUT),
        .input1(MEM_OUTPUT_DATA),
        .select(MEM_TO_REG),
        .out(REG_WRITE_DATA)
    );

    Mux reg_shame_to_ALU(
        .input0(REG_READ_DATA1),
        .input1({27'b0,INST[10:6]}),
        .select(SHAMT_SIGN),
        .out(ALU_INPUT1)
    );

    Registers reg_file(
        .readReg1(INST[25:21]),
        .readReg2(INST[20:16]),
        .writeReg(WRITE_REG_ID_AFTER_JAL_MUX),
        .writeData(REG_WRITE_DATA_AFTER_JAL_MUX),
        .regWrite(REG_WRITE & !JR_SIGN),
        .clk(clk),
        .reset(reset),
        .readData1(REG_READ_DATA1),
        .readData2(REG_READ_DATA2)
    );

    ALUCtr alu_ctr(
        .aluOp(ALU_OP),
        .funct(INST[5:0]),
        .shamtSign(SHAMT_SIGN),
        .aluCtrOut(ALU_CTR),
        .jrSign(JR_SIGN)
    );

    ALU alu(
        .input1(ALU_INPUT1),
        .input2(ALU_INPUT2),
        .aluCtr(ALU_CTR),
        .aluRes(ALU_OUTPUT),
        .zero(ALU_ZERO)
    );

    dataMemory memory(
        .clk(clk),
        .address(ALU_OUTPUT),
        .writeData(MEM_INPUT_DATA),
        .memWrite(MEM_WRITE),
        .memRead(MEM_READ),
        .readData(MEM_OUTPUT_DATA)
    );

    signext sign_ext(
        .inst(INST[15:0]),
        .signExt(EXT_OP),
        .data(EXT_IMM)
    );

    InstMem inst_mem(
        .address(PC_OUT),
        .inst(INST)
    );

    PC pc(
        .pcIn(PC_IN),
        .clk(clk),
        .reset(reset),
        .pcOut(PC_OUT)
    );


    Mux branch_mux(
        .select(BRANCH & ALU_ZERO),
        .input1(PC_OUT+4+(EXT_IMM<<2)),
        .input0(PC_OUT+4),
        .out(PC_AFTER_BRANCH_MUX)
    );

    Mux jr_mux(
        .select(JR_SIGN),
        .input0(PC_AFTER_BRANCH_MUX),
        .input1(REG_READ_DATA1),
        .out(PC_AFTER_JR_MUX)
    );

    Mux jump_mux(
        .select(JUMP),
        .input0(PC_AFTER_JR_MUX),
        .input1(JUMP_ADDR),
        .out(PC_IN)
    );

    Mux jal_data_mux(
        .select(JAL_SIGN),
        .input0(REG_WRITE_DATA),
        .input1(PC_OUT+4),
        .out(REG_WRITE_DATA_AFTER_JAL_MUX)
    );

    Mux jal_reg_id_mux(
        .select(JAL_SIGN),
        .input0(WRITE_REG_ID),
        .input1(5'b11111),
        .out(WRITE_REG_ID_AFTER_JAL_MUX)
    );

    assign JUMP_ADDR = ((PC_OUT+4)&32'hf0000000)+(INST[25:0]<<2);
    assign JUMP_ADDR_debug = INST[25:0]<<2;
endmodule
