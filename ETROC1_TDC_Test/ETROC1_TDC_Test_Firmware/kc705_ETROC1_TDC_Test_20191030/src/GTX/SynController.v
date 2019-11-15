/////////////////////////////////////////////////////////////////////////////////////////////////////
//
//  Filename: SynController
//  Descripiton: to sync FSM  Based KC705, board clock 156.25MHz
//
//  Author: Binwei Deng
//
//  Date: 05/03/2018
//
//  Organization: Southern Methodist University
//
//  Version: V1.0.1.2  mass test be run, Reliable Version

//  
//  detail: for lpGBT align
//   sync have three states that are CHECK, SYNC.
////////////////////////////////////////////////////////////////////////////////////////////////////  

module SynController(
							input  wire  clk, // 320MHz, namely, rx_clkout
							input  wire [01:00] PATTERN,// Header with current frame
//							input  wire  bcid_fr,// frame trailer arrivision flag
							output reg   d_enb=1'b0, // align data flag , dataout output enable
							(* KEEP =  "TRUE" *)output reg  [01:00] synch_status=CHECK, // sync status signal
					//		output reg   shift_fr_early, // change frame border one bit early
							output wire   shift_fr_later // change frame border one bit later
										//for test
					
							
						
						
							
							);
							
parameter CHECK = 2'b00,
			 SYNC=2'b10;
	//		 RESYNC=2'b11;
				
//reg [07:00] prbs=8'b0;
reg [05:00] Pcounter=3'b0;  // counter for prbs buffer 
reg [11:00] frame_counter=0;   // frame counter 

assign shift_fr_later= (PATTERN[1:0]== 2'b01)?0:1;
always @(posedge clk)
begin
		
		case (synch_status)
		CHECK:
		begin
			d_enb<=0;
			//syn_state<=0;
			//pre_syn<=1;
		//	if (bcid_fr)
				begin
				if (PATTERN[1:0]== 2'b01)
						begin
						       if (Pcounter== 20)
										begin
											//pre_syn<=1'b0;
											//syn_state<=1'b1;
											//precount<=1'b0;
											Pcounter<=1'b0;
											synch_status<=SYNC;
										end
									else 
										begin
											Pcounter<=Pcounter+1'b1;
											synch_status<=CHECK;
										end
					//	shift_fr_later<=1'b0;
/////////////////////////////////////////////////////////////////						
//							frame_counter<=frame_counter+1'b1;
//							if (frame_counter== 4095 )//
//								begin
//									shift_fr_later<=1'b1;
//									frame_counter<=1'b0;
//								end
//							else shift_fr_later<=1'b0;
//							
						end
					else //if (PATTERN[1:0]== 2'b01)
						begin
					//		shift_fr_later<=1'b1;
					//		frame_counter<=1'b0;
							 Pcounter<=1'b0;// ensure to contiuos counter
							synch_status<=CHECK;
						end
					end
//			 else 
//				begin
//					shift_fr_later<=1'b0;
//					synch_status<=CHECK;
//				end
		end

		SYNC:
			begin
				//if ( bcid_fr )
							begin
								
								if (PATTERN[1:0]==2'b01 )
									begin
										d_enb<=1'b1;
										synch_status<=SYNC;
								//		shift_fr_later<=1'b0;
									end
								else
									begin
										d_enb<=1'b0;
										synch_status<=CHECK;
								//		shift_fr_later<=1'b1;
									end
								
							
							end
//						else
//							begin
							
//								synch_status<=SYNC;
//							end
			end
		endcase
end
endmodule
