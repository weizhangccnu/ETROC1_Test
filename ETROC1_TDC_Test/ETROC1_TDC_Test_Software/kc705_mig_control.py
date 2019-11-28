#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import copy
import time
import struct
import socket
from command_interpret import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
'''
@author: Wei Zhang
@date: 2018-03-20
This script is used for testing ETROC1 TDC chip. The mianly function of this script is I2C write and read, Ethernet communication, instrument control and so on.
'''
hostname = '192.168.2.3'					#FPGA IP address
port = 1024									#port number
#--------------------------------------------------------------------------#
## plot parameters
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
#--------------------------------------------------------------------------#
## DDR3 write data to external device
# @param[in] wr_wrap: wrap address
# @param[in] wr_begin_addr: write data begin address
# @param[in] post_trigger_addr: post trigger address
def write_data_into_ddr3(wr_wrap, wr_begin_addr, post_trigger_addr):
    # writing begin address and wrap_around
    val = (wr_wrap << 28) + wr_begin_addr
    cmd_interpret.write_config_reg(8, 0xffff & val)
    cmd_interpret.write_config_reg(9, 0xffff & (val >> 16))
    # post trigger address
    cmd_interpret.write_config_reg(10, 0xffff & post_trigger_addr)
    cmd_interpret.write_config_reg(11, 0xffff & (post_trigger_addr >> 16))
#--------------------------------------------------------------------------#
## DDR3 read data from fifo to ethernet
# @param[in] rd_stop_addr: read data start address
def read_data_from_ddr3(rd_stop_addr):
    cmd_interpret.write_config_reg(12, 0xffff & rd_stop_addr)
    cmd_interpret.write_config_reg(13, 0xffff & (rd_stop_addr >> 16))
    cmd_interpret.write_pulse_reg(0x0020)           # reading start
#--------------------------------------------------------------------------#
## test ddr3
def test_ddr3():
    cmd_interpret.write_config_reg(0, 0x0000)       # written disable
    cmd_interpret.write_pulse_reg(0x0040)           # reset ddr3 control logic
    cmd_interpret.write_pulse_reg(0x0004)           # reset ddr3 data fifo
    print("sent pulse!")

    cmd_interpret.write_config_reg(0, 0x0001)       # written enable

    write_data_into_ddr3(1, 0x0000000, 0x0100000)   # set write begin address and post trigger address and wrap around
    cmd_interpret.write_pulse_reg(0x0008)           # writing start
    cmd_interpret.write_pulse_reg(0x0010)           # writing stop

    time.sleep(1)
    cmd_interpret.write_config_reg(0, 0x0000)       # write enable
    time.sleep(2)
    read_data_from_ddr3(0x0100000)                  # set read begin address

    data_out = []
    ## memoryview usage
    for i in range(30):
        data_out += cmd_interpret.read_data_fifo(60000)           # reading start
    return data_out
#--------------------------------------------------------------------------#
## IIC write slave device
# @param mode[1:0] : '0'is 1 bytes read or wirte, '1' is 2 bytes read or write, '2' is 3 bytes read or write
# @param slave[7:0] : slave device address
# @param wr: 1-bit '0' is write, '1' is read
# @param reg_addr[7:0] : register address
# @param data[7:0] : 8-bit write data
def iic_write(mode, slave_addr, wr, reg_addr, data):
    val = mode << 24 | slave_addr << 17 | wr << 16 | reg_addr << 8 | data
    cmd_interpret.write_config_reg(4, 0xffff & val)
    cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
    time.sleep(0.01)
    cmd_interpret.write_pulse_reg(0x0001)           # reset ddr3 data fifo
    time.sleep(0.01)
    # print(hex(val))
#--------------------------------------------------------------------------#
## IIC read slave device
# @param mode[1:0] : '0'is 1 bytes read or wirte, '1' is 2 bytes read or write, '2' is 3 bytes read or write
# @param slave[7:0]: slave device address
# @param wr: 1-bit '0' is write, '1' is read
# @param reg_addr[7:0] : register address
def iic_read(mode, slave_addr, wr, reg_addr):
    val = mode << 24 | slave_addr << 17 |  0 << 16 | reg_addr << 8 | 0x00	  # write device addr and reg addr
    cmd_interpret.write_config_reg(4, 0xffff & val)
    cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
    time.sleep(0.01)
    cmd_interpret.write_pulse_reg(0x0001)				                      # Sent a pulse to IIC module

    val = mode << 24 | slave_addr << 17 | wr << 16 | reg_addr << 8 | 0x00	  # write device addr and read one byte
    cmd_interpret.write_config_reg(4, 0xffff & val)
    cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
    time.sleep(0.01)
    cmd_interpret.write_pulse_reg(0x0001)				                      # Sent a pulse to IIC module
    time.sleep(0.01)									                      # delay 10ns then to read data
    return cmd_interpret.read_status_reg(0) & 0xff
#--------------------------------------------------------------------------#
## ddr3 fetching data plot
# @param[in] data: a data list
def data_plot(data):
    plt.plot(data, color='r',marker='X', linewidth=0.2, markersize=0.02, label='DDR3 fetched data')
    plt.title("DDR3 Fetched data plot", family="Times New Roman", fontsize=12)
    plt.xlabel("Point", family="Times New Roman", fontsize=10)
    plt.ylabel("Number", family="Times New Roman", fontsize=10)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("DDR3_Fetched_data.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()
#--------------------------------------------------------------------------#
## Manage ETROC1 TDC chip's internal registers map
# Allow combining and disassembling individual registers
class ETROC1_TDCReg(object):
    ## @var _defaultRegMap default register values
    _defaultRegMap = {
        'Dataout_disCMLDriver_BIAS'     :   0,
        'Clk40Mout_disCMLDriver_BIAS'   :   0,
        'TDC_offset'                    :   0x0,
        'TDC_enable'                    :   1,
        'TDC_level'                     :   0x1,
        'TDC_testMode'                  :   0,
        'TDC_selRawCode'                :   0,
        'TDC_resetn'                    :   1,
        'TDC_polaritySel'               :   1,
        'TDC_autoReset'                 :   0,
        'Clk40Mout_AmplSel'             :   0x1,
        'TDC_enableMon'                 :   0,
        'TDC_timeStampMode'             :   1,
        'Dataout_AmplSel'               :   0x1,
        'DMRO_testmode'                 :   0,
        'DMRO_enable'                   :   1,
        'DMRO_reverse'                  :   0,
        'DMRO_resetn'                   :   1,
        'DMRO_revclk'                   :   0,
        'Dataout_Sel'                   :   1,
        'Clk320M_Psel'                  :   1,
        'Clk40M_Psel'                   :   1,
        'Clk320M_Sel'                   :   1,
        'Clk40M_Sel'                    :   1,
        'Pulse_Sel'                     :   0x03,
        'Clk40M_equalizer'              :   0x0,
        'Clk40M_invertData'             :   0,
        'Clk40M_enableTermination'      :   1,
        'Clk40M_setCommonMode'          :   1,
        'Clk40M_enableRx'               :   1,
        'Clk320M_equalizer'             :   0x0,
        'Clk320M_invertData'            :   0,
        'Clk320M_enableTermination'     :   1,
        'Clk320M_setCommonMode'         :   1,
        'Clk320M_enableRx'              :   1,
        'Clk1G28_equalizer'             :   0x0,
        'Clk1G28_invertData'            :   0,
        'Clk1G28_enableTermination'     :   1,
        'Clk1G28_setCommonMode'         :   1,
        'Clk1G28_enableRx'              :   1,
        'Pulse_equalizer'               :   0x0,
        'Pulse_invertData'              :   0,
        'Pulse_enableTermination'       :   1,
        'Pulse_setCommonMode'           :   1,
        'Pulse_enableRx'                :   1,
        'TDCRawData_Sel'                :   1,
        'GRO_TOT_CK'                    :   1,
        'GRO_TOTRST_N'                  :   1,
        'GRO_TOA_Latch'                 :   1,
        'GRO_TOA_CK'                    :   1,
        'GRO_TOARST_N'                  :   1,
        'GRO_Start'                     :   0,
        'GROout_disCMLDriverBIAS'       :   0,
        'GROout_AmplSel'                :   0x1
        }
    ## @var register map local to the class
    _regMap = {}

    def __init__(self):
        self._regMap = copy.deepcopy(self._defaultRegMap)

    def set_Dataout_disCMLDriver_BIAS(self, val):                               # val = 0, CML driver bias enable, val = 1 CML driver bias disable
        self._regMap['Dataout_disCMLDriver_BIAS'] = 0x1 & val

    def set_Clk40Mout_disCMLDriver_BIAS(self, val):                             # val = 0, CML driver bias enable, val = 1 CML driver bias disable
        self._regMap['Clk40Mout_disCMLDriver_BIAS'] = 0x1 & val

    def set_TDC_offset(self, val):                                              # measurement window offset 0-127
        self._regMap['TDC_offset'] = 0x7f & val

    def set_TDC_enable(self, val):                                              # ONOFF = 0, disable TDC controller, ONOFF = 1 enable TDC controller
        self._regMap['TDC_enable'] = 0x1 & val

    def set_TDC_level(self, val):                                               # TDC encode bubble tolerance intensity, 1, 2, 3
        self._regMap['TDC_level'] = 0x7 & val

    def set_TDC_testMode(self, val):                                            # TDC testMode 1: TDC works on testMode, 0: TDC works on normal mode
        self._regMap['TDC_testMode'] = 0x1 & val

    def set_TDC_selRawCode(self, val):                                          # always keep "0"
        self._regMap['TDC_selRawCode']  = 0x1 & val

    def set_TDC_resetn(self, val):                                              # TDC controller reset, low active
        self._regMap['TDC_resetn'] = 0x1 & val

    def set_TDC_polaritySel(self, val):                                         # TDC controller pulse output polarity, default value "1"
        self._regMap['TDC_polaritySel'] = 0x1 & val

    def set_TDC_autoReset(self, val):                                           # TDC controller work on auto reset mode, default "0", high active
        self._regMap['TDC_autoReset'] = 0x1 & val

    def set_Clk40Mout_AmplSel(self, val):                                       # 40 MHz clock CML output amplitude select, 3-bit default 3'b001
        self._regMap['Clk40Mout_AmplSel'] = 0x7 & val

    def set_TDC_enableMon(self, val):                                           # TDC raw data Monitor output, default value: 0
        self._regMap['TDC_enableMon'] = 0x1 & val

    def set_TDC_timeStampMode(self, val):                                       # Calibration output timeStamp Mode
        self._regMap['TDC_timeStampMode'] = 0x1 & val

    def set_Dataout_Sel(self, val):                                             # Dataout for DMRO serial data or 320M pulse
        self._regMap['Dataout_Sel'] = 0x1 & val

    def set_Clk320M_Psel(self, val):                                            # select Clk320 pulse, 1: clock strobe generator   0: external pad input
        self._regMap['Clk320M_Psel'] = 0x1 & val

    def set_Clk40M_Psel(self, val):                                             # select Clk40 pulse, 1: clock strobe generator   0: external pad input
        self._regMap['Clk40M_Psel'] = 0x1 & val

    def set_Clk320M_Sel(self, val):                                             # select Clk320 clock, 1: clock divider   0: external pad input
        self._regMap['Clk320M_Sel'] = 0x1 & val

    def set_Clk40M_Sel(self, val):                                              # select Clk40 pulse, 1: clock divider   0: external pad input
        self._regMap['Clk40M_Sel'] = 0x1 & val

    def set_Pulse_Sel(self, val):                                               # strobe pulse select, default value 0x03
        self._regMap['Pulse_Sel'] = 0xff & val

    def set_Clk40M_equalizer(self, val):                                        # set clk40M input eRx equalizer intensity, default value 0x00
        self._regMap['Clk40M_equalizer'] = 0x3 & val

    def set_Clk40M_invertData(self, val):                                       # set clk40 input eRx data invert
        self._regMap['Clk40M_invertData'] = 0x1 & val

    def set_Clk40M_enableTermination(self, val):                                # set clk40M input eRx internal Termination
        self._regMap['Clk40M_enableTermination'] = 0x1 & val

    def set_Clk40M_setCommonMode(self, val):                                    # set clk40M input eRx internal Common voltage
        self._regMap['Clk40M_setCommonMode'] = 0x1 & val

    def set_Clk40M_enableRx(self, val):                                         # set clk40M input eRx enable or disable, 1: enable     0: disable
        self._regMap['Clk40M_enableRx'] = 0x1 & val

    def set_Clk320M_equalizer(self, val):                                       # set clk320M input eRx equalizer intensity, default value 0x00
        self._regMap['Clk320M_equalizer'] = 0x3 & val

    def set_Clk320M_invertData(self, val):                                      # set clk320 input eRx data invert
        self._regMap['Clk320M_invertData'] = 0x1 & val

    def set_Clk320M_enableTermination(self, val):                               # set clk320M input eRx internal Termination
        self._regMap['Clk320M_enableTermination'] = 0x1 & val

    def set_Clk320M_setCommonMode(self, val):                                   # set clk320M input eRx internal Common voltage
        self._regMap['Clk320M_setCommonMode'] = 0x1 & val

    def set_Clk320M_enableRx(self, val):                                        # set clk320M input eRx enable or disable, 1: enable     0: disable
        self._regMap['Clk320M_enableRx'] = 0x1 & val

    def set_Clk1G28_equalizer(self, val):                                       # set clk1G28 input eRx equalizer intensity, default value 0x00
        self._regMap['Clk1G28_equalizer'] = 0x3 & val

    def set_Clk1G28_invertData(self, val):                                      # set clk1G28 input eRx data invert
        self._regMap['Clk1G28_invertData'] = 0x1 & val

    def set_Clk1G28_enableTermination(self, val):                               # set clk1G28 input eRx internal Termination
        self._regMap['Clk1G28_enableTermination'] = 0x1 & val

    def set_Clk1G28_setCommonMode(self, val):                                   # set clk1G28 input eRx internal Common voltage
        self._regMap['Clk1G28_setCommonMode'] = 0x1 & val

    def set_Clk1G28_enableRx(self, val):                                        # set clk1G28 input eRx enable or disable, 1: enable     0: disable
        self._regMap['Clk1G28_enableRx'] = 0x1 & val

    def set_Pulse_equalizer(self, val):                                         # set Pulse input eRx equalizer intensity, default value 0x00
        self._regMap['Pulse_equalizer'] = 0x3 & val

    def set_Pulse_invertData(self, val):                                        # set Pulse input eRx data invert
        self._regMap['Pulse_invertData'] = 0x1 & val

    def set_Pulse_enableTermination(self, val):                                 # set Pulse input eRx internal Termination
        self._regMap['Pulse_enableTermination'] = 0x1 & val

    def set_Pulse_setCommonMode(self, val):                                     # set Pulse input eRx internal Common voltage
        self._regMap['Pulse_setCommonMode'] = 0x1 & val

    def set_Pulse_enableRx(self, val):                                          # set Pulse input eRx enable or disable, 1: enable     0: disable
        self._regMap['Pulse_enableRx'] = 0x1 & val

    def set_TDCRawData_Sel(self, val):                                          # TDC raw data output MUX switcher
        self._regMap['TDCRawData_Sel'] = 0x1 & val

    def set_GRO_TOT_CK(self, val):                                              # set GRO TOT clock
        self._regMap['GRO_TOT_CK'] = 0x1 & val

    def set_GRO_TOTRST_N(self, val):                                            # set GRO TOT Reset, default 1, low active
        self._regMap['GRO_TOTRST_N'] = 0x1 & val

    def set_GRO_TOA_Latch(self, val):                                           # set GRO TOA_Latch clock
        self._regMap['GRO_TOA_Latch'] = 0x1 & val

    def set_GRO_TOA_CK(self, val):                                              # set GRO TOA clock
        self._regMap['GRO_TOA_CK'] = 0x1 & val

    def set_GRO_TOARST_N(self, val):                                            # set GRO TOA Reset, default 1, low active
        self._regMap['GRO_TOARST_N'] = 0x1 & val

    def set_GRO_Start(self, val):                                               # set GRO Start signal, default 0, high active
        self._regMap['GRO_Start'] = 0x1 & val

    def set_GROout_disCMLDriverBISA(self, val):                                 # set GRO CML Driver bias disable, default 0
        self._regMap['GROout_disCMLDriverBIAS'] = 0x1 & val

    def set_GROout_AmplSel(self, val):                                          # set GRO CML driver output signal amplitude
        self._regMap['GROout_AmplSel'] = 0x7 & val

    ## get I2C register value
    def get_config_vector(self):
        reg_value = []
        reg_value += [self._regMap['Clk40Mout_disCMLDriver_BIAS'] << 1 | self._regMap['Dataout_disCMLDriver_BIAS']]             # register 0x00
        reg_value += [self._regMap['TDC_enable'] << 7 | self._regMap['TDC_offset']]                                             # register 0x01
        reg_value += [self._regMap['TDC_autoReset'] << 7 | self._regMap['TDC_polaritySel'] << 6 | self._regMap['TDC_resetn'] << 5 | self._regMap['TDC_selRawCode'] << 4 | self._regMap['TDC_testMode'] << 3 | self._regMap['TDC_level']]        # register 0x02
        reg_value += [self._regMap['TDC_timeStampMode'] << 4 | self._regMap['TDC_enableMon'] << 3 | self._regMap['Clk40Mout_AmplSel']]          # register 0x03
        reg_value += [self._regMap['DMRO_revclk'] << 7 | self._regMap['DMRO_resetn'] << 6 | self._regMap['DMRO_reverse'] << 5 | self._regMap['DMRO_enable'] << 4 | self._regMap['DMRO_testmode'] << 3 | self._regMap['Dataout_AmplSel']]        # register 0x04
        reg_value += [self._regMap['Clk40M_Sel'] << 4 | self._regMap['Clk320M_Sel'] << 3 | self._regMap['Clk40M_Psel'] << 2 | self._regMap['Clk320M_Psel'] << 1 | self._regMap['Dataout_Sel']]      # reg 0x05
        reg_value += [self._regMap['Pulse_Sel']]    # reg 0x06
        reg_value += [self._regMap['Clk40M_enableRx'] << 5 | self._regMap['Clk40M_setCommonMode'] << 4 | self._regMap['Clk40M_enableTermination'] << 3 | self._regMap['Clk40M_invertData'] << 2 | self._regMap['Clk40M_equalizer']] # reg 0x07
        reg_value += [self._regMap['Clk320M_enableRx'] << 5 | self._regMap['Clk320M_setCommonMode'] << 4 | self._regMap['Clk320M_enableTermination'] << 3 | self._regMap['Clk320M_invertData'] << 2 | self._regMap['Clk320M_equalizer']] # reg 0x08
        reg_value += [self._regMap['Clk1G28_enableRx'] << 5 | self._regMap['Clk1G28_setCommonMode'] << 4 | self._regMap['Clk1G28_enableTermination'] << 3 | self._regMap['Clk1G28_invertData'] << 2 | self._regMap['Clk1G28_equalizer']] # reg 0x09
        reg_value += [self._regMap['Pulse_enableRx'] << 5 | self._regMap['Pulse_setCommonMode'] << 4 | self._regMap['Pulse_enableTermination'] << 3 | self._regMap['Pulse_invertData'] << 2 | self._regMap['Pulse_equalizer']] # reg 0x0A
        reg_value += [self._regMap['GRO_Start'] << 6 | self._regMap['GRO_TOARST_N'] << 5 | self._regMap['GRO_TOA_CK'] << 4 | self._regMap['GRO_TOA_Latch'] << 3 | self._regMap['GRO_TOTRST_N'] << 2 | self._regMap['GRO_TOT_CK'] << 1 | self._regMap['TDCRawData_Sel']] # reg 0x0B
        reg_value += [self._regMap['GROout_AmplSel'] << 1 | self._regMap['GROout_disCMLDriverBIAS']]
        return reg_value
#--------------------------------------------------------------------------#
## main functionl
def main():
    # reg_addr = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d,\
    #             0x0e, 0x0f, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b]
    # for j in range(len(reg_addr)):
    #     iic_write(1, 0x22, 0, reg_addr[j], j)
    # print(len(reg_addr))
    # for i in range(len(reg_addr)):
    #     print("reg addr %s:"%str(hex(reg_addr[i])), hex(iic_read(0, 0x22, 1, reg_addr[i])))
    # data_out = []
    # data_out = test_ddr3()
    # print(data_out)
    # data_plot(data_out)
    ETROC1_TDCReg1 = ETROC1_TDCReg()
    ETROC1_TDCReg1.set_TDC_offset(0x01)
    ETROC1_TDCReg1.set_TDC_autoReset(0)
    ETROC1_TDCReg1.set_Clk320M_enableRx(0)
    ETROC1_TDCReg1.set_Clk1G28_enableRx(0)
    ETROC1_TDCReg1.set_Pulse_enableRx(0)
    ETROC1_TDCReg1.set_GROout_disCMLDriverBISA(1)
    print(ETROC1_TDCReg1.get_config_vector())
    print("Ok!")
#--------------------------------------------------------------------------#
## if statement
if __name__ == "__main__":
	# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#initial socket
	# s.connect((hostname, port))								#connect socket
	# cmd_interpret = command_interpret(s)					#Class instance
	main()													#execute main function
	# s.close()												#close socket
