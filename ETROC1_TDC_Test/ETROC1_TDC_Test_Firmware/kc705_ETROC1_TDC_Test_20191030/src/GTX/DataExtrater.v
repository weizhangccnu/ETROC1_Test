////////////////////////////////////////////////////////////////////////////////////////////////////
//
//  Filename: DataExtrater
//
//  Descripiton: Extract Data from data in DeSerGTX module
//
//  Author: Binwei Deng
//
//  Organization: Southern Methodist University 
//  
//  Date: 08/20/2018
//
//  Version: Beta 1.0
//
//  detail: for lpGBT align (dynamic) on KC705
//  DataExtrater module operation cotrolled by SynController
//  Southern Methodist University
//
//  data32 make of two datain which is 16 bit, in order to solve cross data.
//  PATTERN obtained from data32
//
//  When deal with shift one bit which includes early and later arrivison  within data stream, 
//  downlink PATTERN=0xf00f
///////////////////////////////////////////////////////////////////////////////////////////////////
module DataExtrater(
						  input  wire	 clk,			// 160MHz clock for ETROC��
						  input 	wire  [31:00] datain,		// input unframed data, namely, GTX received data
						  output reg   [31:00] dataout=32'b0,     // data to descrambler
						  input  wire   d_enb,       // alig data flag , dataout output enable
//						  output wire   d_fr,        // frame signal to descramber
						 // output reg   [07:00] crc=8'b0,		 	// 8 bit CRC to CRC checher
						 // output wire    crc_fr,      // frame signal to CRC checker
						  output reg   [01:00] PATTERN=2'b0,			// PATTERN BCID to controller and BCID counter
//						  output reg    bcid_fr=1'b0,     // frame signal to controller and BCID counter
						//  output reg    early_bit=1'b0,   // one bit before PATTERN, for re-synchronizeation
						//  output reg    later_bit=1'b0,   // one bit afeter PATTERN, for re-synchronizeation
					//	  input  wire   shift_fr_early, // pulse signal from controller, to shift current frame one bit early
						  input  wire   shift_fr_later,  // pulse signal from controller, to shift current frame one bit later
								
						 // for test
						  (* keep = "TRUE" *)output reg [63:00] data64=64'b0
					//	  output reg   [15:00] dataout1=16'b0,     // data to descrambler
					//	  output reg   [15:00] dataout2=16'b0,     // data to descrambler
					//	  output reg   [15:00] dataout3=16'b0,     // data to descrambler
					//	  output reg   [15:00] dataout4=16'b0     // data to descrambler
						 );

						  


// generate data32
//(* keep = "TRUE" *)reg [31:00] data32=32'b0;	
reg [00:00] crc_fr_d=1'b0;

// Special treatment control-variant for borderline cases
//reg [00:00] ENTRF0=1'b0;
//reg [00:00] ENTR0F=1'b0;
////reg [57:00] rsr = 58'b0101010101010101010101010101010101010101010101010101010101;		  
//reg [32:00] data64;
always @( posedge clk )						 

begin
// data32[31:00]<={datain[15:0],data32[31:16]};// combine to 32 bit 
// data64[32:00]<={data32[31:0],data64[16:16]};// combine to 33 bit
   data64[63:00]<={ datain[31:0],data64[63:32]};
end


//------------------------------------------------------------------------
reg [02:00] clk_counter=0;
reg [04:00] shift_counter=0;
reg [02:00] field_counter=0;
always @( posedge clk )

begin
   // for operating later bit
	if (shift_fr_later)
		begin
			if (shift_counter==31)
				begin
					shift_counter<=0;
	//				clk_counter<=clk_counter;// later one clock for shift_fr_later
				end
			else	
				begin
					shift_counter<=shift_counter+5'b00001;
			//		clk_counter<=clk_counter+3'b001;// for movement within frame 
				end
		end
	else 	shift_counter<=shift_counter;//clk_counter<=clk_counter+3'b001;// for movement within frame 
	
//	// for controlling early bit
//	if (shift_fr_early)
//		begin
//			if (shift_counter==5'b00000) 
//				begin
//					shift_counter<=31;
//					clk_counter<=clk_counter+2'b10;
//				end
//			else  
//				begin
//					shift_counter<=shift_counter-1'b1;
//				end
//
//		end

	// get 8 bit data as PATTERN and PATTERN early bit and later bit to send SynController module to judge.
	// 05/21/2013 modify for LSB->MSB = crc-->PATTERN
                        
	
 //dataout1<=data64[16:01];
 //dataout2<=data64[17:02];
 //dataout3<=data64[18:03];
// dataout4<=data64[19:04];

	// move one word and calculate counter within the frame	
	// when arrive one frame, bcid_fr=1 inform synController module 
//	if (clk_counter== 7)
//		begin
//			clk_counter<=1'b0;
//			bcid_fr<=1'b1;
//		end
//	else bcid_fr<=1'b0;
end
// output frame data and header boundary
//assign d_fr= ~bcid_fr;
//assign crc_fr= bcid_fr;

always @*
	case (shift_counter)
	5'b00000:begin PATTERN<=data64[1:0];   dataout<=data64[31:00];   end
	5'b00001:begin PATTERN<=data64[2:1];   dataout<=data64[32:01];   end
	5'b00010:begin PATTERN<=data64[3:2];   dataout<=data64[33:02];   end
	5'b00011:begin PATTERN<=data64[4:3];   dataout<=data64[34:03];   end
	5'b00100:begin PATTERN<=data64[5:4];   dataout<=data64[35:04];   end
	5'b00101:begin PATTERN<=data64[6:5];   dataout<=data64[36:05];   end
	5'b00110:begin PATTERN<=data64[7:6];   dataout<=data64[37:06];   end
	5'b00111:begin PATTERN<=data64[8:7];   dataout<=data64[38:07];  end
	5'b01000:begin PATTERN<=data64[9:8];   dataout<=data64[39:08];  end
	5'b01001:begin PATTERN<=data64[10:9];  dataout<=data64[40:09];  end
	5'b01010:begin PATTERN<=data64[11:10]; dataout<=data64[41:10]; end
	5'b01011:begin PATTERN<=data64[12:11]; dataout<=data64[42:11]; end
	5'b01100:begin PATTERN<=data64[13:12]; dataout<=data64[43:12]; end
	5'b01101:begin PATTERN<=data64[14:13]; dataout<=data64[44:13]; end
	5'b01110:begin PATTERN<=data64[15:14]; dataout<=data64[45:14]; end
	5'b01111:begin PATTERN<=data64[16:15]; dataout<=data64[46:15]; end
	5'b10000:begin PATTERN<=data64[17:16]; dataout<=data64[47:16];   end
	5'b10001:begin PATTERN<=data64[18:17]; dataout<=data64[48:17];   end
	5'b10010:begin PATTERN<=data64[19:18]; dataout<=data64[49:18];   end
	5'b10011:begin PATTERN<=data64[20:19]; dataout<=data64[50:19];   end
	5'b10100:begin PATTERN<=data64[21:20]; dataout<=data64[51:20];   end
	5'b10101:begin PATTERN<=data64[22:21]; dataout<=data64[52:21];   end
	5'b10110:begin PATTERN<=data64[23:22]; dataout<=data64[53:22];   end
	5'b10111:begin PATTERN<=data64[24:23]; dataout<=data64[54:23];  end
	5'b11000:begin PATTERN<=data64[25:24]; dataout<=data64[55:24];  end
	5'b11001:begin PATTERN<=data64[26:25]; dataout<=data64[56:25];  end
	5'b11010:begin PATTERN<=data64[27:26]; dataout<=data64[57:26]; end
	5'b11011:begin PATTERN<=data64[28:27]; dataout<=data64[58:27]; end
	5'b11100:begin PATTERN<=data64[29:28]; dataout<=data64[59:28]; end
	5'b11101:begin PATTERN<=data64[30:29]; dataout<=data64[60:29]; end
	5'b11110:begin PATTERN<=data64[31:30]; dataout<=data64[61:30]; end
	5'b11111:begin PATTERN<=data64[32:31]; dataout<=data64[62:31]; end	


	endcase      

endmodule
					