//////////////////////////////////////////////////////////////////////////////////
// Org:        	FNAL&SMU
// Author:      Quan Sun
// 
// Create Date:    Fri Feb 15 11:08 CST 2019
// Design Name:    ETROC1 
// Module Name:    SCR30b
// Project Name: 
// Description: a parallel scrambler for 30-bit data, G=X^58+X^39+1
//
// Dependencies: 
//
// Revision: v3, added input latch
//
//
//////////////////////////////////////////////////////////////////////////////////
`timescale 1ps/1fs
module SCR30b(
	CLK,
	RSTn,
	DataIn,
	REV,
	EN,
	DataOut
);

input CLK;
input RSTn;
input [29:0] DataIn;
input REV;	//reverse input data in bit-wise, active-high
//input REVCLK;		//reverse word clock, active-high. input data can be latched correctly at least in one clock phase
input EN;	//enable Scrambler, active-high
output [29:0] DataOut;

reg [57:0] S_reg;
wire [57:0] S_wire;
reg rst_int;
wire [57:0] A;
wire [29:0] DataOutSCR;
reg [29:0] reg_input;
wire CLK_SCR_int;

assign A = REV?~reg_input:reg_input;
assign DataOut = EN?DataOutSCR:A;

assign DataOutSCR[0] = S_reg[57]^S_reg[38]^A[0];
assign DataOutSCR[1] = S_reg[56]^S_reg[37]^A[1];
assign DataOutSCR[2] = S_reg[55]^S_reg[36]^A[2];
assign DataOutSCR[3] = S_reg[54]^S_reg[35]^A[3];
assign DataOutSCR[4] = S_reg[53]^S_reg[34]^A[4];
assign DataOutSCR[5] = S_reg[52]^S_reg[33]^A[5];
assign DataOutSCR[6] = S_reg[51]^S_reg[32]^A[6];
assign DataOutSCR[7] = S_reg[50]^S_reg[31]^A[7];
assign DataOutSCR[8] = S_reg[49]^S_reg[30]^A[8];
assign DataOutSCR[9] = S_reg[48]^S_reg[29]^A[9];
assign DataOutSCR[10] = S_reg[47]^S_reg[28]^A[10];
assign DataOutSCR[11] = S_reg[46]^S_reg[27]^A[11];
assign DataOutSCR[12] = S_reg[45]^S_reg[26]^A[12];
assign DataOutSCR[13] = S_reg[44]^S_reg[25]^A[13];
assign DataOutSCR[14] = S_reg[43]^S_reg[24]^A[14];
assign DataOutSCR[15] = S_reg[42]^S_reg[23]^A[15];
assign DataOutSCR[16] = S_reg[41]^S_reg[22]^A[16];
assign DataOutSCR[17] = S_reg[40]^S_reg[21]^A[17];
assign DataOutSCR[18] = S_reg[39]^S_reg[20]^A[18];
assign DataOutSCR[19] = S_reg[38]^S_reg[19]^A[19];
assign DataOutSCR[20] = S_reg[37]^S_reg[18]^A[20];
assign DataOutSCR[21] = S_reg[36]^S_reg[17]^A[21];
assign DataOutSCR[22] = S_reg[35]^S_reg[16]^A[22];
assign DataOutSCR[23] = S_reg[34]^S_reg[15]^A[23];
assign DataOutSCR[24] = S_reg[33]^S_reg[14]^A[24];
assign DataOutSCR[25] = S_reg[32]^S_reg[13]^A[25];
assign DataOutSCR[26] = S_reg[31]^S_reg[12]^A[26];
assign DataOutSCR[27] = S_reg[30]^S_reg[11]^A[27];
assign DataOutSCR[28] = S_reg[29]^S_reg[10]^A[28];
assign DataOutSCR[29] = S_reg[28]^S_reg[9]^A[29];

assign S_wire[0] =  S_reg[28]^S_reg[9]^A[29];
assign S_wire[1] =  S_reg[29]^S_reg[10]^A[28];
assign S_wire[2] =  S_reg[30]^S_reg[11]^A[27];
assign S_wire[3] =  S_reg[31]^S_reg[12]^A[26];
assign S_wire[4] =  S_reg[32]^S_reg[13]^A[25];
assign S_wire[5] =  S_reg[33]^S_reg[14]^A[24];
assign S_wire[6] =  S_reg[34]^S_reg[15]^A[23];
assign S_wire[7] =  S_reg[35]^S_reg[16]^A[22];
assign S_wire[8] =  S_reg[36]^S_reg[17]^A[21];
assign S_wire[9] =  S_reg[37]^S_reg[18]^A[20];
assign S_wire[10] =  S_reg[38]^S_reg[19]^A[19];
assign S_wire[11] =  S_reg[39]^S_reg[20]^A[18];
assign S_wire[12] =  S_reg[40]^S_reg[21]^A[17];
assign S_wire[13] =  S_reg[41]^S_reg[22]^A[16];
assign S_wire[14] =  S_reg[42]^S_reg[23]^A[15];
assign S_wire[15] =  S_reg[43]^S_reg[24]^A[14];
assign S_wire[16] =  S_reg[44]^S_reg[25]^A[13];
assign S_wire[17] =  S_reg[45]^S_reg[26]^A[12];
assign S_wire[18] =  S_reg[46]^S_reg[27]^A[11];
assign S_wire[19] =  S_reg[47]^S_reg[28]^A[10];
assign S_wire[20] =  S_reg[48]^S_reg[29]^A[9];
assign S_wire[21] =  S_reg[49]^S_reg[30]^A[8];
assign S_wire[22] =  S_reg[50]^S_reg[31]^A[7];
assign S_wire[23] =  S_reg[51]^S_reg[32]^A[6];
assign S_wire[24] =  S_reg[52]^S_reg[33]^A[5];
assign S_wire[25] =  S_reg[53]^S_reg[34]^A[4];
assign S_wire[26] =  S_reg[54]^S_reg[35]^A[3];
assign S_wire[27] =  S_reg[55]^S_reg[36]^A[2];
assign S_wire[28] =  S_reg[56]^S_reg[37]^A[1];
assign S_wire[29] =  S_reg[57]^S_reg[38]^A[0];
assign S_wire[30] =  S_reg[0];
assign S_wire[31] =  S_reg[1];
assign S_wire[32] =  S_reg[2];
assign S_wire[33] =  S_reg[3];
assign S_wire[34] =  S_reg[4];
assign S_wire[35] =  S_reg[5];
assign S_wire[36] =  S_reg[6];
assign S_wire[37] =  S_reg[7];
assign S_wire[38] =  S_reg[8];
assign S_wire[39] =  S_reg[9];
assign S_wire[40] =  S_reg[10];
assign S_wire[41] =  S_reg[11];
assign S_wire[42] =  S_reg[12];
assign S_wire[43] =  S_reg[13];
assign S_wire[44] =  S_reg[14];
assign S_wire[45] =  S_reg[15];
assign S_wire[46] =  S_reg[16];
assign S_wire[47] =  S_reg[17];
assign S_wire[48] =  S_reg[18];
assign S_wire[49] =  S_reg[19];
assign S_wire[50] =  S_reg[20];
assign S_wire[51] =  S_reg[21];
assign S_wire[52] =  S_reg[22];
assign S_wire[53] =  S_reg[23];
assign S_wire[54] =  S_reg[24];
assign S_wire[55] =  S_reg[25];
assign S_wire[56] =  S_reg[26];
assign S_wire[57] =  S_reg[27];

/*
always@(negedge RSTn or posedge CLK) begin
if(!RSTn)
	rst_int <= 0;
else
	rst_int <= 1;
end
*/

always@(negedge RSTn or posedge CLK) begin
if(!RSTn)		
	reg_input[29:0] <= 30'b010101010101010101010101010101;
else begin
	reg_input[29:0] <= DataIn[29:0];
end

end


always@(negedge RSTn or posedge CLK) begin
if(!RSTn)		
	S_reg[57:0] <= 58'b0101010101010101010101010101010101010101010101010101010101;
else begin
	S_reg[57:0] <= S_wire[57:0];
end

end


endmodule
