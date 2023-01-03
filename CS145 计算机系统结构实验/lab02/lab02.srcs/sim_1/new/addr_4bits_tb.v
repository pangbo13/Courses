`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/05/12 10:32:51
// Design Name: 
// Module Name: addr_4bits_tb
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


module addr_4bits_tb(

    );
    reg [3:0] a;
    reg [3:0] b;
    reg ci;
    
    wire [3:0] s;
    wire co;
    
    adder_4bits u0(
        .a(a),
        .b(b),
        .ci(ci),
        .s(s),
        .co(co)
    );
    
    initial begin
        a = 0;
        b = 0;
        ci = 0;
        
        #100;
        a = 4'b0001;
        b = 4'b0010;
        #100;
        a = 4'b0010;
        b = 4'b0100;
        #100;
        a = 4'b1111;
        b = 4'b0001;
        #100;
        ci = 1'b1;
     end
endmodule
