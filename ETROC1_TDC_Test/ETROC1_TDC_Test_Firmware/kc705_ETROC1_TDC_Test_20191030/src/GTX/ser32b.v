//////////////////////////////////////////////////////////////////////////////////
// Org:        	FNAL&SMU
// Author:      Quan Sun
// 
// Create Date:    Fri Feb 15 14:26 CST 2019
// Design Name:    ETROC1 
// Module Name:    SER32b
// Project Name: 
// Description: 32:1 serializer
//
// Dependencies: 
//
// Revision:
//
//
//////////////////////////////////////////////////////////////////////////////////
`timescale 1ps/1fs
module SER32b(
	CLKBit,
	RSTn,
	DataIn,
	CLKWord,
	DataOut
);

input CLKBit;
input RSTn;
input [31:0] DataIn;
//input [1:0] Header;	//2-bit header
output CLKWord;
output DataOut;

reg [31:0] In_reg;
reg [4:0] counter;
//reg rst_int;
wire DOBuf;
wire [4:0] Load;

assign DataOut = DOBuf;
assign DOBuf = In_reg[31];
assign Load = counter;
assign CLKWord = counter[4];

always@(negedge RSTn or posedge CLKBit) begin
if(!RSTn)		
	counter[4:0] <= 5'b11111;
else begin
	counter[4:0] <= counter[4:0] - 5'b00001;
end
end


always@(negedge RSTn or posedge CLKBit) begin
if(!RSTn)		
	In_reg <= 0;
else begin
	if(Load == 5'b00001)
		In_reg <= DataIn;
	else
		In_reg <= In_reg << 1;
end
end


endmodule
