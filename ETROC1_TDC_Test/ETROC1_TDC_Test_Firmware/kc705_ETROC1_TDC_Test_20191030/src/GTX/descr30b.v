//////////////////////////////////////////////////////////////////////////////////
// Org:		FNAL&SMU
// Author:	Quan Sun
// 
// Create Date:    Fri Feb 15 11:08 CST 2019
// Design Name:    ETROC1 
// Module Name:    SCR30b
// Project Name: 
// Description: a parallel scrambler for 30-bit data, G=X^58+X^39+1
//
// Dependencies: 
//
// Revision: 
//
//
//////////////////////////////////////////////////////////////////////////////////
`timescale 1ps/1fs

module DESCR30b(
	CLK,
	RSTn,
	DataIn,
	REV,
	DataOut
);

input CLK;
input RSTn;
input [29:0] DataIn;
input REV;	//reverse output data in bit-wise
output [29:0] DataOut;

reg [57:0] S_reg;
wire [57:0] S_wire;
reg rst_int;
wire [57:0] B;

assign DataOut = REV?~B:B;


assign B[0] = S_reg[57]^S_reg[38]^DataIn[0];
assign B[1] = S_reg[56]^S_reg[37]^DataIn[1];
assign B[2] = S_reg[55]^S_reg[36]^DataIn[2];
assign B[3] = S_reg[54]^S_reg[35]^DataIn[3];
assign B[4] = S_reg[53]^S_reg[34]^DataIn[4];
assign B[5] = S_reg[52]^S_reg[33]^DataIn[5];
assign B[6] = S_reg[51]^S_reg[32]^DataIn[6];
assign B[7] = S_reg[50]^S_reg[31]^DataIn[7];
assign B[8] = S_reg[49]^S_reg[30]^DataIn[8];
assign B[9] = S_reg[48]^S_reg[29]^DataIn[9];
assign B[10] = S_reg[47]^S_reg[28]^DataIn[10];
assign B[11] = S_reg[46]^S_reg[27]^DataIn[11];
assign B[12] = S_reg[45]^S_reg[26]^DataIn[12];
assign B[13] = S_reg[44]^S_reg[25]^DataIn[13];
assign B[14] = S_reg[43]^S_reg[24]^DataIn[14];
assign B[15] = S_reg[42]^S_reg[23]^DataIn[15];
assign B[16] = S_reg[41]^S_reg[22]^DataIn[16];
assign B[17] = S_reg[40]^S_reg[21]^DataIn[17];
assign B[18] = S_reg[39]^S_reg[20]^DataIn[18];
assign B[19] = S_reg[38]^S_reg[19]^DataIn[19];
assign B[20] = S_reg[37]^S_reg[18]^DataIn[20];
assign B[21] = S_reg[36]^S_reg[17]^DataIn[21];
assign B[22] = S_reg[35]^S_reg[16]^DataIn[22];
assign B[23] = S_reg[34]^S_reg[15]^DataIn[23];
assign B[24] = S_reg[33]^S_reg[14]^DataIn[24];
assign B[25] = S_reg[32]^S_reg[13]^DataIn[25];
assign B[26] = S_reg[31]^S_reg[12]^DataIn[26];
assign B[27] = S_reg[30]^S_reg[11]^DataIn[27];
assign B[28] = S_reg[29]^S_reg[10]^DataIn[28];
assign B[29] = S_reg[28]^S_reg[9]^DataIn[29];

assign S_wire[0] =  DataIn[29];
assign S_wire[1] =  DataIn[28];
assign S_wire[2] =  DataIn[27];
assign S_wire[3] =  DataIn[26];
assign S_wire[4] =  DataIn[25];
assign S_wire[5] =  DataIn[24];
assign S_wire[6] =  DataIn[23];
assign S_wire[7] =  DataIn[22];
assign S_wire[8] =  DataIn[21];
assign S_wire[9] =  DataIn[20];
assign S_wire[10] =  DataIn[19];
assign S_wire[11] =  DataIn[18];
assign S_wire[12] =  DataIn[17];
assign S_wire[13] =  DataIn[16];
assign S_wire[14] =  DataIn[15];
assign S_wire[15] =  DataIn[14];
assign S_wire[16] =  DataIn[13];
assign S_wire[17] =  DataIn[12];
assign S_wire[18] =  DataIn[11];
assign S_wire[19] =  DataIn[10];
assign S_wire[20] =  DataIn[9];
assign S_wire[21] =  DataIn[8];
assign S_wire[22] =  DataIn[7];
assign S_wire[23] =  DataIn[6];
assign S_wire[24] =  DataIn[5];
assign S_wire[25] =  DataIn[4];
assign S_wire[26] =  DataIn[3];
assign S_wire[27] =  DataIn[2];
assign S_wire[28] =  DataIn[1];
assign S_wire[29] =  DataIn[0];
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

always@(negedge RSTn or posedge CLK) begin
if(!RSTn)
	rst_int <= 0;
else
	rst_int <= 1;
end

always@(negedge rst_int or posedge CLK) begin
if(!rst_int)		
	S_reg[57:0] <= 58'b0101010101010101010101011101010101010101010101010101010101;
else begin
S_reg[57:0] <= S_wire[57:0];
end

end


endmodule
