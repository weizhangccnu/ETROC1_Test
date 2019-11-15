`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: CCNU
// Engineer: WeiZhang
// 
// Create Date: 03/16/2018 09:34:02 PM
// Design Name: kc705_mig
// Module Name: kc705_mig
// Project Name: kc705_mig
// Target Devices: KC705 EVB
// Tool Versions: 
// Description: 
// This project is used to learn ddr3 in KC705 EVB
// Dependencies: 
// 
// Revision: V1.0
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////
module kc705_mig(
input SYS_RST,              //system reset
input SYS_CLK_P,            //system clock 200MHz
input SYS_CLK_N,
input SGMIICLK_Q0_P,        //125MHz for GTP/GTH/GTX  for 1G Ethernet interface
input SGMIICLK_Q0_N,
//----------------------< LED        
output [7:0] LED8Bit,        //clock output
//----------------------< DIPSw4Bit
input  [3:0] DIPSw4Bit,
//----------------------> Gigbit eth interface (RGMII)
output PHY_RESET_N,
output [3:0] RGMII_TXD,
output RGMII_TX_CTL,
output RGMII_TXC,
input  [3:0] RGMII_RXD,
input  RGMII_RX_CTL,
input  RGMII_RXC,
inout  MDIO,
output MDC,
//----------------------< SDRAM PHY interface
inout wire [63:0] DDR3_DQ,
inout wire [7:0] DDR3_DQS_P,
inout wire [7:0] DDR3_DQS_N,
// Outputs
output wire [13:0] DDR3_ADDR,
output wire [2:0] DDR3_BA,
output wire DDR3_RAS_N,
output wire DDR3_CAS_N,
output wire DDR3_WE_N,
output wire DDR3_RESET_N,
output wire DDR3_CK_P,
output wire DDR3_CK_N,
output wire DDR3_CKE,
output wire DDR3_CS_N,
output wire [7:0] DDR3_DM,
output wire DDR3_ODT,

//---------------------< IIC interface
inout wire SDA,
output wire SCL, 

//---------------------< GTX
input Q2_CLK1_GTREFCLK_PAD_N_IN,
input Q2_CLK1_GTREFCLK_PAD_P_IN,
input RXN_IN,
input RXP_IN,
output TXN_OUT,
output TXP_OUT  
);
//---------------------------------------------------------< signal define
wire reset;
wire sys_clk;
wire clk_25MHz;
wire clk_50MHz;
wire clk_100MHz;
wire clk_200MHz;
//---------------------------------------------------------> signal define
//---------------------------------------------------------< global_clock_reset
global_clock_reset global_clock_reset_inst(
    .SYS_CLK_P(SYS_CLK_P),
    .SYS_CLK_N(SYS_CLK_N),
    .FORCE_RST(SYS_RST),
    // output
    .GLOBAL_RST(reset),
    .SYS_CLK(sys_clk),
    .CLK_OUT1(clk_25MHz),
    .CLK_OUT2(clk_50MHz),
    .CLK_OUT3(clk_100MHz),
    .CLK_OUT4("open"),
    .CLK_OUT5(clk_200MHz)
  );
//---------------------------------------------------------> global_clock_reset
//---------------------------------------------------------< generate sgmii_i clock
wire clk_sgmii_i;
wire clk_sgmii;
wire clk_125MHz;
IBUFDS_GTE2 #(
   .CLKCM_CFG("TRUE"),          // Refer to Transceiver User Guide
   .CLKRCV_TRST("TRUE"),        // Refer to Transceiver User Guide
   .CLKSWING_CFG(2'b11)         // Refer to Transceiver User Guide
)
IBUFDS_GTE2_inst (
   .O(clk_sgmii_i),             // 1-bit output: Refer to Transceiver User Guide
   .ODIV2("open"),              // 1-bit output: Refer to Transceiver User Guide
   .CEB(1'b0),                  // 1-bit input: Refer to Transceiver User Guide
   .I(SGMIICLK_Q0_P),           // 1-bit input: Refer to Transceiver User Guide
   .IB(SGMIICLK_Q0_N)           // 1-bit input: Refer to Transceiver User Guide
);

BUFG BUFG_inst (
   .O(clk_sgmii),               // 1-bit output: Clock output
   .I(clk_sgmii_i)              // 1-bit input: Clock input
);
assign clk_125MHz = clk_sgmii;
//---------------------------------------------------------> generate sgmii_i clock
//---------------------------------------------------------< dbg_ila
wire probe1;
assign probe1 = pulse_reg[6:3];
dbg_ila dbg_ila_inst(
	.clk(clk_25MHz),                // input wire clk
	.probe0(counter[3:0]),          // input wire [3:0] probe0
    .probe1(probe1)                 // input wire [3:0]  probe1
);
//---------------------------------------------------------> dbg_ila
//---------------------------------------------------------< vio core
wire [15:0] probe_in0;
wire [31:0] probe_in1;
wire [255:0] probe_in2;
wire [55:0] probe_in3;
wire [255:0] probe_in4;
wire [15:0] probe_out0;
assign probe_in0 = {12'h000,DIPSw4Bit[3:0]};
assign probe_in1 = {5'b00000,MODE,SL_ADDR[6:0],SL_WR,WR_ADDR[7:0],WR_DATA0[7:0]};
assign probe_in2 = config_reg[255:0];
assign probe_in3 = {wr_pointer, trigger_pointer};
assign probe_in4 = fifo_data_out;
vio_0 vio_0_inst (
  .clk(clk_25MHz),          // input wire clk
  .probe_in0(probe_in0),    // input wire [15 : 0] probe_in0
  .probe_in1(probe_in1),    // input wire [31 : 0] probe_in1
  .probe_in2(probe_in2),    // input wire [255 : 0] probe_in2
  .probe_in3(probe_in3),    // input wire [55 : 0] probe_in3
  .probe_in4(probe_in4),    // input wire [255 : 0] probe_in4
  .probe_out0(probe_out0)   // output wire [15 : 0] probe_out0
);
//---------------------------------------------------------> vio core
reg [24:0]counter;
wire select;
assign select = probe_out0[0];
always @(posedge clk_125MHz)
begin
    if(reset)
        counter <= 25'd0;
    else
    begin
        counter <= counter + 1'b1; 
        if(counter == 25'h1ffffff)
            counter <= 25'd0;
    end
end
assign LED8Bit[0] = counter[22];
assign LED8Bit[1] = counter[24];
assign LED8Bit[2] = select?counter[22]:counter[24];
assign LED8Bit[3] = select?counter[22]:counter[24];
assign LED8Bit[4] = select?counter[22]:counter[24];
//assign LED8Bit[5] = select?counter[22]:counter[24];
//assign LED8Bit[6] = select?counter[22]:counter[24];
//assign LED8Bit[7] = select?counter[22]:counter[24];
//---------------------------------------------------------< gig_eth 
wire [47:0]gig_eth_mac_addr;
wire [31:0]gig_eth_ipv4_addr;
wire [31:0]gig_eth_subnet_mask;
wire [31:0]gig_eth_gateway_ip_addr; 
wire [7:0]gig_eth_tx_tdata;
wire gig_eth_tx_tvalid;
wire gig_eth_tx_tready;
wire [7:0]gig_eth_rx_tdata;
wire gig_eth_rx_tvalid;
wire gig_eth_rx_tready;
wire gig_eth_tcp_use_fifo;
wire gig_eth_tx_fifo_wrclk;
wire [31:0]gig_eth_tx_fifo_q;
wire gig_eth_tx_fifo_wren;
wire gig_eth_tx_fifo_full;
wire gig_eth_rx_fifo_rdclk;
wire [31:0]gig_eth_rx_fifo_q;
wire gig_eth_rx_fifo_rden;
wire gig_eth_rx_fifo_empty;

assign gig_eth_mac_addr = {44'h000a3502a75,DIPSw4Bit[3:0]};
assign gig_eth_ipv4_addr = {28'hc0a8020,DIPSw4Bit[3:0]};
assign gig_eth_subnet_mask = 32'hffffff00;
assign gig_eth_gateway_ip_addr = 32'hc0a80201;
//assign gpio_high = 2'b11;
gig_eth gig_eth_inst
(
// asynchronous reset
   .GLBL_RST(reset),
// clocks
   .GTX_CLK(clk_125MHz),
   .REF_CLK(sys_clk), // 200MHz for IODELAY
// PHY interface
   .PHY_RESETN(PHY_RESET_N),
//         -- RGMII Interface
   .RGMII_TXD(RGMII_TXD),
   .RGMII_TX_CTL(RGMII_TX_CTL),
   .RGMII_TXC(RGMII_TXC),
   .RGMII_RXD(RGMII_RXD),
   .RGMII_RX_CTL(RGMII_RX_CTL),
   .RGMII_RXC(RGMII_RXC),
// MDIO Interface
   .MDIO(MDIO),
   .MDC(MDC),
// TCP
   .MAC_ADDR(gig_eth_mac_addr),
   .IPv4_ADDR(gig_eth_ipv4_addr),
   .IPv6_ADDR(128'h0),
   .SUBNET_MASK(gig_eth_subnet_mask),
   .GATEWAY_IP_ADDR(gig_eth_gateway_ip_addr),
   .TCP_CONNECTION_RESET(1'b0),
   .TX_TDATA(gig_eth_tx_tdata),
   .TX_TVALID(gig_eth_tx_tvalid),
   .TX_TREADY(gig_eth_tx_tready),
   .RX_TDATA(gig_eth_rx_tdata),
   .RX_TVALID(gig_eth_rx_tvalid),
   .RX_TREADY(gig_eth_rx_tready),
//fifo8to32 and fifo32to8
   .TCP_USE_FIFO(gig_eth_tcp_use_fifo),
   .TX_FIFO_WRCLK(gig_eth_tx_fifo_wrclk),
   .TX_FIFO_Q(gig_eth_tx_fifo_q),
   .TX_FIFO_WREN(gig_eth_tx_fifo_wren),
   .TX_FIFO_FULL(gig_eth_tx_fifo_full),
   .RX_FIFO_RDCLK(gig_eth_rx_fifo_rdclk),
   .RX_FIFO_Q(gig_eth_rx_fifo_q),
   .RX_FIFO_RDEN(gig_eth_rx_fifo_rden),
   .RX_FIFO_EMPTY(gig_eth_rx_fifo_empty)
);
assign gig_eth_tcp_use_fifo = 1'b1;
assign gig_eth_rx_fifo_rdclk = control_clk;
//---------------------------------------------------------> gig_eth
//---------------------------------------------------------< control_interface
wire control_clk;
wire [35:0]control_fifo_q;
wire control_fifo_empty;
wire control_fifo_rdreq;
wire control_fifo_rdclk;

wire [35:0]cmd_fifo_q;
wire cmd_fifo_empty;
wire cmd_fifo_rdreq;

wire [511:0]config_reg;
wire [15:0]pulse_reg;
wire [175:0]status_reg;

wire control_mem_we;
wire [31:0]control_mem_addr;
wire [31:0]control_mem_din;

wire idata_data_fifo_rdclk;
wire idata_data_fifo_empty;
wire idata_data_fifo_rden;
wire [31:0]idata_data_fifo_dout;
assign control_clk = clk_100MHz;

control_interface  control_interface_inst(
   .RESET(reset),
   .CLK(control_clk),
  // From FPGA to PC
   .FIFO_Q(control_fifo_q),
   .FIFO_EMPTY(control_fifo_empty),
   .FIFO_RDREQ(control_fifo_rdreq),
   .FIFO_RDCLK(control_fifo_rdclk),
  // From PC to FPGA, FWFT
   .CMD_FIFO_Q(cmd_fifo_q),
   .CMD_FIFO_EMPTY(cmd_fifo_empty),
   .CMD_FIFO_RDREQ(cmd_fifo_rdreq),
  // Digital I/O
   .CONFIG_REG(config_reg),
   .PULSE_REG(pulse_reg),
   .STATUS_REG(status_reg),
  // Memory interface
   .MEM_WE(control_mem_we),
   .MEM_ADDR(control_mem_addr),
   .MEM_DIN(control_mem_din),
   .MEM_DOUT(),
  // Data FIFO interface, FWFT
   .DATA_FIFO_Q(idata_data_fifo_dout),
   .DATA_FIFO_EMPTY(idata_data_fifo_empty),
   .DATA_FIFO_RDREQ(idata_data_fifo_rden),
   .DATA_FIFO_RDCLK(idata_data_fifo_rdclk)
);
assign cmd_fifo_q = gig_eth_rx_fifo_q;
assign cmd_fifo_empty = gig_eth_rx_fifo_empty;
assign gig_eth_rx_fifo_rden = cmd_fifo_rdreq;

assign gig_eth_tx_fifo_wrclk = clk_125MHz;
assign control_fifo_rdclk = gig_eth_tx_fifo_wrclk;
assign gig_eth_tx_fifo_q = control_fifo_q[31:0];
assign gig_eth_tx_fifo_wren = ~control_fifo_empty;
assign control_fifo_rdreq = ~gig_eth_tx_fifo_full;
//---------------------------------------------------------> control_interface
//---------------------------------------------------------< mig_7series_0
wire idata_data_fifo_reset;
wire idata_data_wr_busy;
wire idata_data_wr_wrapped;
wire idata_data_fifo_reset;
wire idata_idata_fifo_wrclk;
wire [255:0] idata_idata_fifo_q;
wire idata_idata_fifo_full;
wire idata_idata_fifo_wren;
wire [27:0] wr_pointer;
wire [27:0] trigger_pointer;

//wire idata_data_fifo_rdclk;
//wire [31:0] idata_data_fifo_dout;
//wire idata_data_fifo_empty;
//wire idata_data_fifo_rden;

wire [27:0] sdram_app_addr;
wire sdram_app_en;
wire sdram_app_rdy;
wire [511:0] sdram_app_wdf_data;
wire sdram_app_wdf_end;
wire sdram_app_wdf_wren;
wire sdram_app_wdf_rdy;
wire [511:0] sdram_app_rd_data;
wire sdram_app_rd_data_valid;
sdram_ddr3 sdram_ddr3_inst(
.CLK(sys_clk),                     // system clock, must be the same as intended in MIG
.REFCLK(sys_clk),                  // 200MHz for iodelay
.RESET(reset),
// SDRAM_DDR3
// Inouts
.DDR3_DQ(DDR3_DQ),
.DDR3_DQS_P(DDR3_DQS_P),
.DDR3_DQS_N(DDR3_DQS_N),
// Outputs
.DDR3_ADDR(DDR3_ADDR),
.DDR3_BA(DDR3_BA),
.DDR3_RAS_N(DDR3_RAS_N),
.DDR3_CAS_N(DDR3_CAS_N),
.DDR3_WE_N(DDR3_WE_N),
.DDR3_RESET_N(DDR3_RESET_N),
.DDR3_CK_P(DDR3_CK_P),
.DDR3_CK_N(DDR3_CK_N),
.DDR3_CKE(DDR3_CKE),
.DDR3_CS_N(DDR3_CS_N),
.DDR3_DM(DDR3_DM),
.DDR3_ODT(DDR3_ODT),
// Status Outputs
.INIT_CALIB_COMPLETE(LED8Bit[7]),
// Internal data r/w interface
.UI_CLK(clk_200MHz),
//
.CTRL_RESET(pulse_reg[6]),
.WR_START(pulse_reg[3]),
.WR_ADDR_BEGIN(config_reg[32*4+27:32*4]),
.WR_STOP(pulse_reg[4]),
.WR_WRAP_AROUND(config_reg[32*4+28]),
.POST_TRIGGER(config_reg[32*5+27:32*5]),
.WR_BUSY(LED8Bit[6]),
.WR_POINTER(wr_pointer),
.TRIGGER_POINTER(trigger_pointer),
.WR_WRAPPED(idata_data_wr_wrapped),
.RD_START(pulse_reg[5]),
.RD_ADDR_BEGIN(28'h0000000),
.RD_ADDR_END(config_reg[32*6+27:32*6]),
.RD_BUSY(LED8Bit[5]),
//
.DATA_FIFO_RESET(idata_data_fifo_reset),
.INDATA_FIFO_WRCLK(idata_idata_fifo_wrclk),
.INDATA_FIFO_Q(idata_idata_fifo_q),
.INDATA_FIFO_FULL(idata_idata_fifo_full),
.INDATA_FIFO_WREN(idata_idata_fifo_wren),
//
.OUTDATA_FIFO_RDCLK(idata_data_fifo_rdclk),
.OUTDATA_FIFO_Q(idata_data_fifo_dout),
.OUTDATA_FIFO_EMPTY(idata_data_fifo_empty),
.OUTDATA_FIFO_RDEN(idata_data_fifo_rden),
//-----------------------------------------------< dbg_interface
.DBG_APP_ADDR(sdram_app_addr),
.DBG_APP_EN(sdram_app_en),
.DBG_APP_RDY(sdram_app_rdy),
.DBG_APP_WDF_DATA(sdram_app_wdf_data),
.DBG_APP_WDF_END(sdram_app_wdf_end),
.DBG_APP_WDF_WREN(sdram_app_wdf_wren),
.DBG_APP_WDF_RDY(sdram_app_wdf_rdy),
.DBG_APP_RD_DATA(sdram_app_rd_data),
.DBG_APP_RD_DATA_VALID(sdram_app_rd_data_valid)
  );
assign idata_idata_fifo_wrclk = clk_25MHz;
assign idata_idata_fifo_q = fifo_data_out;
assign idata_idata_fifo_wren = ~fifo_empty;
assign fifo_rd_en = ~idata_idata_fifo_full;
assign idata_data_fifo_reset = pulse_reg[2];
//---------------------------------------------------------> mig_7series_0
//---------------------------------------------------------< create_input_data
wire fifo_rd_en;
wire [255:0] fifo_data_out;
wire fifo_empty;
create_input_data create_input_data_inst(
.clk(gt0_rxusrclk2_i),                          //input clock
.reset(pulse_reg[6]),                           //system reset
.data_in(DataAfterDESCR),
.fifo_wr_en(config_reg[0]),
.fifo_rd_clk(clk_25MHz),
.fifo_rd_en(fifo_rd_en),
.fifo_data_out(fifo_data_out),
.fifo_empty(fifo_empty)
);
//---------------------------------------------------------> create_input_data

//---------------------------------------------------------< IIC
wire START;
wire [1:0]MODE;
wire SL_WR;
wire [6:0]SL_ADDR;
wire [7:0]WR_ADDR;
wire [7:0]WR_DATA0;
wire [7:0]WR_DATA1;
wire [7:0]RD_DATA0;
wire [7:0]RD_DATA1;
wire SDA_OUT;
wire SDA_IN;
wire SDA_T;

assign START = pulse_reg[0];
assign MODE = config_reg[2*32+25:2*32+24];
assign SL_ADDR = config_reg[2*32+23:2*32+17];
assign SL_WR = config_reg[2*32+16];
assign WR_ADDR = config_reg[2*32+15:2*32+8];
assign WR_DATA0 = config_reg[2*32+7:2*32+0];
assign status_reg[15:0] = {RD_DATA1, RD_DATA0};
i2c_wr_bytes i2c_wr_bytes_inst(
.CLK(clk_100MHz),                       //system clock 50Mhz
.RESET(reset),                          //active high reset
.START(START),                          //the rising edge trigger a start, generate by config_reg
.MODE(MODE),                            //'0' is 1 bytes read or write, '1' is 2 bytes read or write,
                                        //'2' is 3 bytes write only , don't set to '3'
.SL_WR(SL_WR),                          //'0' is write, '1' is read
.SL_ADDR(SL_ADDR),                      //slave addr
.WR_ADDR(WR_ADDR),                      //chip internal addr for read and write
.WR_DATA0(WR_DATA0),                    //first byte data for write
.WR_DATA1(WR_DATA1),                    //second byte data for write
.RD_DATA0(RD_DATA0),                    //first byte readout
.RD_DATA1(RD_DATA1),                    //second byte readout
.BUSY("open"),                          //indicates transaction in progress
.SDA_in(SDA),                           //serial data input of i2c bus
.SDA_out(SDA_OUT),                      //serial data output of i2c bus
.SDA_T(SDA_T),                          //serial data direction of i2c bus
.SCL(SCL)                               //serial clock output of i2c bus
);
assign SDA = SDA_T ? 1'bz : SDA_OUT;
//---------------------------------------------------------> IIC

//---------------------------------------------------------< GTX
wire [31:0] gt0_rxdata_i;
reg [31:0] gt0_txdata_i;
wire gt0_txusrclk2_i;
wire gt0_rxusrclk2_i;

gtwizard_0_exdes gtwizard_0_exdes_i(
.Q2_CLK1_GTREFCLK_PAD_N_IN(Q2_CLK1_GTREFCLK_PAD_N_IN), 
.Q2_CLK1_GTREFCLK_PAD_P_IN(Q2_CLK1_GTREFCLK_PAD_P_IN),
.DRPCLK_IN(sys_clk),
.TRACK_DATA_OUT("open"),//(track_data_i),
.RXN_IN(RXN_IN),
.RXP_IN(RXP_IN),
.TXN_OUT(TXN_OUT),
.TXP_OUT(TXP_OUT),
.gt0_rxdata_i(gt0_rxdata_i),
.gt0_txdata_i(gt0_txdata_i),
.gt0_txusrclk2_i( gt0_txusrclk2_i),
.gt0_rxusrclk2_i( gt0_rxusrclk2_i)
);
//---------------------------------------------------------> GTX
//---------------------------------------------------------< Counter  
reg [29:0]cnt=30'b0;
reg [29:0] In_reg;
wire [29:0] DataScrambled;
always @(posedge gt0_txusrclk2_i)
begin
    cnt<= cnt+1'b1;
    In_reg[29:0] <= cnt[29:0];
    gt0_txdata_i[31:0] <= {DataScrambled,2'b01};
end
//---------------------------------------------------------> Counter
//---------------------------------------------------------< Scraber
SCR30b INS_SCR30b(
.CLK(gt0_txusrclk2_i),
.RSTn(!reset),
.DataIn(In_reg),
.REV(1'b0),//(REVData),
.EN(1'b1),//(ENScr),
.DataOut(DataScrambled)
);
//---------------------------------------------------------> Scraber

//----------------------------------------------------------------< DataExtrater
wire [31:0] dataout;
wire d_enb;
wire [1:0] PATTERN;
wire shift_fr_later;

DataExtrater dataext (
.clk(gt0_rxusrclk2_i), 
.datain(gt0_rxdata_i), 
.dataout(dataout), 
.d_enb(d_enb), 
.PATTERN(PATTERN), 
.shift_fr_later(shift_fr_later) 
);
//----------------------------------------------------------------> DataExtrater

//----------------------------------------------------------------< Sync
wire [1:0] synch_status;
SynController sync (
.clk(gt0_rxusrclk2_i), 
.PATTERN(PATTERN), 
.d_enb(d_enb), 
.synch_status(synch_status), 
.shift_fr_later(shift_fr_later)
);
//----------------------------------------------------------------> Sync

//----------------------------------------------------------------< Descrabler
wire [29:0] DataAfterDESCR;
DESCR30b DESCR30b_Ins(
	.CLK(gt0_rxusrclk2_i),
	.RSTn(!reset),
	.DataIn(dataout[31:2]),    //(DataBeforeDESCR),
	.REV(1'b0),                //(reverse_data),
	.DataOut(DataAfterDESCR)
);
//----------------------------------------------------------------> Descrabler

//----------------------------------------------------------------< ILA
wire [160:0] TRIG0;
ila_0 ila (
.clk(gt0_rxusrclk2_i),
.probe0(TRIG0)
);
assign TRIG0[31:0]=gt0_txdata_i[31:0];
assign TRIG0[63:32]=gt0_rxdata_i;
assign TRIG0[95:64]=dataout;
assign TRIG0[97:96]=synch_status;
assign TRIG0[99:98]=PATTERN;
assign TRIG0[129:100]=DataAfterDESCR;
assign TRIG0[159:130]=In_reg;
assign TRIG0[160]=reset;
//----------------------------------------------------------------> ILA
endmodule
