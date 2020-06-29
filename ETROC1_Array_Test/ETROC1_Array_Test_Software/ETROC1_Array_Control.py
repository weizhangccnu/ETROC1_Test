#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import copy
import time
import visa
import struct
import socket
import winsound
import datetime
import heartrate
from command_interpret import *
from ETROC1_ArrayReg import *
import numpy as np
from command_interpret import *
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
#========================================================================================#
freqency = 1000
duration = 1000
'''
@author: Wei Zhang
@date: 2018-02-28
This script is used for testing ETROC1 Array chip. The mianly function of this script is I2C write and read, Ethernet communication, instrument control and so on.
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
def test_ddr3(data_num):
    cmd_interpret.write_config_reg(0, 0x0000)       # written disable
    cmd_interpret.write_pulse_reg(0x0040)           # reset fifo32to256
    time.sleep(0.02)

    cmd_interpret.write_pulse_reg(0x0004)           # reset ddr3 data fifo
    time.sleep(0.02)

    cmd_interpret.write_pulse_reg(0x0040)           # reset fifo32to256
    time.sleep(0.02)

    cmd_interpret.write_pulse_reg(0x0004)           # reset ddr3 data fifo
    time.sleep(0.02)
    print("sent pulse!")

    cmd_interpret.write_config_reg(0, 0x0001)       # written enable

    write_data_into_ddr3(1, 0x0000000, 0x6000000)   # set write begin address and post trigger address and wrap around
    cmd_interpret.write_pulse_reg(0x0008)           # writing start
    time.sleep(0.02)
    cmd_interpret.write_pulse_reg(0x0010)           # writing stop

    time.sleep(2)
    cmd_interpret.write_config_reg(0, 0x0000)       # write enable
    time.sleep(4)
    read_data_from_ddr3(0x6000000)                  # set read begin address

    data_out = []
    ## memoryview usage
    for i in range(data_num):
        data_out += cmd_interpret.read_data_fifo(50000)           # reading start
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
    time.sleep(0.02)
    cmd_interpret.write_pulse_reg(0x0001)				                      # Sent a pulse to IIC module

    val = mode << 24 | slave_addr << 17 | wr << 16 | reg_addr << 8 | 0x00	  # write device addr and read one byte
    cmd_interpret.write_config_reg(4, 0xffff & val)
    cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
    time.sleep(0.02)
    cmd_interpret.write_pulse_reg(0x0001)				                      # Sent a pulse to IIC module
    time.sleep(0.02)									                      # delay 10ns then to read data
    return cmd_interpret.read_status_reg(0) & 0xff
#--------------------------------------------------------------------------#
## Enable FPGA Descrambler
def Enable_FPGA_Descramblber(val):
    if val==1:
        print("Enable FPGA Descrambler")
    else:
        print("Disable FPGA Descrambler")
    cmd_interpret.write_config_reg(14, 0x0001 & val)       # write enable
#--------------------------------------------------------------------------#
## DAC output configuration, 0x000: 0.6V  ox200: 0.8V  0x2ff: 1V
#@para[in] num : 0-15 value: Digital input value
def DAC_Config(num, value):
    pass
#--------------------------------------------------------------------------#
## main functionl
def main():
    slaveA_addr = 0x03                          # I2C slave A address
    slaveB_addr = 0x7f                          # I2C slave B address

    ## Parameters configuration
    Pixel_Num = 15                              # range from 0-15
    Board_num = 1                               # Board ID show in tag
    EnScr = 1                                   # Enable Scrambler
    DMRO_revclk = 1                             # Sample clock polarity
    TDC_Mode_Output = 0                         # 1: TDC output data, 0: Counter output data
    Fetch_Data = 1


    reg_val = []
    ## charge injection setting
    ETROC1_ArrayReg1.set_QSel(6)
    ETROC1_ArrayReg1.set_EN_QInj7_0(0x01)       # Enable QInj7~0
    ETROC1_ArrayReg1.set_EN_QInj15_8(0x00)      # Enable QInj15~8

    ## PreAmp setting
    ETROC1_ArrayReg1.set_CLSel(1)
    ETROC1_ArrayReg1.set_RfSel(2)
    ETROC1_ArrayReg1.set_IBSel(7)

    ## Discriminator setting
    ETROC1_ArrayReg1.set_HysSel(0xf)

    ETROC1_ArrayReg1.set_EN_DiscriOut(0x11)


    ETROC1_ArrayReg1.set_PD_DACDiscri7_0(0xfe)
    ETROC1_ArrayReg1.set_PD_DACDiscri15_8(0xff)

    ## VDAC setting
    VTHOut_Select = [[0xfe, 0xff], [0xfd, 0xff], [0xfb, 0xff], [0xf7, 0xff], [0xef, 0xff], [0xdf, 0xff], [0xbf, 0xff], [0x7f, 0xff],\
                     [0xff, 0xfe], [0xff, 0xfd], [0xff, 0xfb], [0xff, 0xf7], [0xff, 0xef], [0xff, 0xdf], [0xff, 0xbf], [0xff, 0x7f], [0xff, 0xff]]

    Pixel_VTHOut_Select = 15                 # num ranges from 0-15      16: all turn off
    ETROC1_ArrayReg1.set_Dis_VTHInOut7_0(VTHOut_Select[Pixel_VTHOut_Select][0])
    ETROC1_ArrayReg1.set_Dis_VTHInOut15_8(VTHOut_Select[Pixel_VTHOut_Select][1])

    ETROC1_ArrayReg1.set_VTHIn7_0(0xff)
    ETROC1_ArrayReg1.set_VTHIn15_8(0xff)
    ETROC1_ArrayReg1.set_VTHIn23_16(0xff)
    ETROC1_ArrayReg1.set_VTHIn31_24(0xff)
    ETROC1_ArrayReg1.set_VTHIn39_32(0xff)
    ETROC1_ArrayReg1.set_VTHIn47_40(0xff)
    ETROC1_ArrayReg1.set_VTHIn55_48(0xff)
    ETROC1_ArrayReg1.set_VTHIn63_56(0xff)
    ETROC1_ArrayReg1.set_VTHIn71_64(0xff)
    ETROC1_ArrayReg1.set_VTHIn79_72(0xff)
    ETROC1_ArrayReg1.set_VTHIn87_80(0xff)
    ETROC1_ArrayReg1.set_VTHIn95_88(0xff)
    ETROC1_ArrayReg1.set_VTHIn103_96(0xff)
    ETROC1_ArrayReg1.set_VTHIn111_104(0xff)
    ETROC1_ArrayReg1.set_VTHIn119_112(0xff)
    ETROC1_ArrayReg1.set_VTHIn127_120(0xff)
    ETROC1_ArrayReg1.set_VTHIn135_128(0xff)
    ETROC1_ArrayReg1.set_VTHIn143_136(0xff)
    ETROC1_ArrayReg1.set_VTHIn151_144(0xff)
    ETROC1_ArrayReg1.set_VTHIn159_152(0x02)

    ## Phase Shifter Setting
    ETROC1_ArrayReg1.set_dllCapReset(0)         # should be set to 0
    ETROC1_ArrayReg1.set_dllCPCurrent(1)        # default value 1:
    ETROC1_ArrayReg1.set_dllEnable(1)           # Enable phase shifter
    ETROC1_ArrayReg1.set_dllForceDown(0)        # should be set to 0
    ETROC1_ArrayReg1.set_PhaseAdj(30)           # 0-128 to adjust clock phas

    # 320M clock strobe setting
    ETROC1_ArrayReg1.set_RefStrSel(0x03)        # default 0x03: 3.125 ns

    # clock input and output MUX select
    ETROC1_ArrayReg1.set_TestCLK0(0)            # 0: 40M and 320M clock comes from phase shifter, 1: 40M and 320M clock comes from external pads
    ETROC1_ArrayReg1.set_TestCLK1(0)            # 0: 40M and 320M  go cross clock strobe 1: 40M and 320M bypass
    ETROC1_ArrayReg1.set_CLKOutSel(0)           # 0: 40M clock output, 1: 320M clock or strobe output

    ## DMRO readout Mode
    ETROC1_ArrayReg1.set_OE_DMRO_Row(0x8)       # DMRO readout row select
    ETROC1_ArrayReg1.set_DMRO_Col(0x3)          # DMRO readout column select
    ETROC1_ArrayReg1.set_RO_SEL(0)              # 0: DMRO readout enable  1: Simple readout enable
    ETROC1_ArrayReg1.set_TDC_enableMon(~TDC_Mode_Output)       # 0: Connect to TDC       1: Connect to Test Counter

    ## TDC setting
    ETROC1_ArrayReg1.set_TDC_resetn(1)
    ETROC1_ArrayReg1.set_TDC_testMode(1)
    ETROC1_ArrayReg1.set_TDC_autoReset(0)
    ETROC1_ArrayReg1.set_TDC_enable(1)

    ## DMRO Setting
    ETROC1_ArrayReg1.set_DMRO_ENScr(EnScr)          # Enable DMRO scrambler
    ETROC1_ArrayReg1.set_DMRO_revclk(DMRO_revclk)
    ETROC1_ArrayReg1.set_DMRO_testMode(0)       # DMRO work on test mode
    Enable_FPGA_Descramblber(EnScr)                 # Enable FPGA Firmware Descrambler

    ## DMRO CML driver
    ETROC1_ArrayReg1.set_Dataout_AmplSel(7)

    ETROC1_ArrayReg1.set_CLKTO_AmplSel(7)
    ETROC1_ArrayReg1.set_CLKTO_disBIAS(0)

    reg_val = ETROC1_ArrayReg1.get_config_vector()                      # Get Array Pixel Register default data

    ## write data to I2C register one by one
    print("Write data into I2C slave:")
    print(reg_val)
    for i in range(len(reg_val)):
        if i < 32:                                                      # I2C slave A write
            iic_write(1, slaveA_addr, 0, i, reg_val[i])
        else:                                                           # I2C slave B write
            iic_write(1, slaveB_addr, 0, i-32, reg_val[i])

    ## read back data from I2C register one by one
    iic_read_val = []
    for i in range(len(reg_val)):
        if i < 32:
            iic_read_val += [iic_read(0, slaveA_addr, 1, i)]            # I2C slave A read
        else:
            iic_read_val += [iic_read(0, slaveB_addr, 1, i-32)]         # I2C slave B read
    print("I2C read back data:")
    print(iic_read_val)

    ## compare I2C write in data with I2C read back data
    if iic_read_val == reg_val:
        print("Wrote into data matches with read back data!")
        winsound.Beep(1000, 500)
    else:
        print("Wrote in data doesn't matche with read back data!!!!")
        for x in range(3):
            winsound.Beep(1000, 500)


    # Receive DMRO output data and store it to dat file
    if Fetch_Data == 1:
        for k in range(1):
            Total_point = 10
            if TDC_Mode_Output == 1:
                filename = "Array_Data_Pixel=%02d_VTHIn3_0=0x0F_EnScr=%1d_DMRO_revclk=%1d_TDC_Mode_Output_B%s_%s"%(Pixel_Num, EnScr, DMRO_revclk, Board_num, Total_point*50000)
            else:
                filename = "Array_Data_Pixel=%02d_VTHIn3_0=0x0F_EnScr=%1d_DMRO_revclk=%1d_Counter_Mode_Output_B%s_%s"%(Pixel_Num, EnScr, DMRO_revclk, Board_num, Total_point*50000)

            ##  Creat a directory named path with date of today
            today = datetime.date.today()
            todaystr = today.isoformat() + "_Array_Test_Results"
            try:
                os.mkdir(todaystr)
                print("Directory %s was created!"%todaystr)
            except FileExistsError:
                print("Directory %s already exists!"%todaystr)

            ## add log file
            with open("./%s/log_%s.dat"%(todaystr, time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))),'w+') as logfile:
                logfile.write("%s\n"%time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                logfile.write("I2C write into data:\n")
                for i in range(len(reg_val)):
                    if i < 32:                                                      # I2C slave A write
                        logfile.writelines("REGA_%02d %s\n"%(i, hex(reg_val[i])))
                    else:                                                           # I2C slave B write
                        logfile.writelines("REGB_%02d %s\n"%(i-32, hex(reg_val[i])))
                if iic_read_val == reg_val:
                    logfile.write("Wrote into data matches with read back data!\n")
                else:
                    logfile.write("Wrote in data doesn't matche with read back data!!!!\n")
                logfile.write("%s\n"%filename)

            print("filename is: %s"%filename)
            print("Fetching NO.%01d file..."%k)
            data_out = [0]
            data_out = test_ddr3(Total_point)                           ## num: The total fetch data num * 50000
            # print(data_out)

            with open("./%s/%s_%01d.dat"%(todaystr, filename, k),'w') as infile:
                for i in range(len(data_out)):
                    if TDC_Mode_Output == 0:
                        infile.write("%d\n"%(data_out[i]))
                    else:
                        TDC_data = []
                        for j in range(30):
                            TDC_data += [((data_out[i] >> j) & 0x1)]
                        hitFlag = TDC_data[29]
                        TOT_Code1 = TDC_data[0] << 8 | TDC_data[1] << 7 | TDC_data[2] << 6 | TDC_data[3] << 5 | TDC_data[4] << 4 | TDC_data[5] << 3 | TDC_data[6] << 2 | TDC_data[7] << 1 | TDC_data[8]
                        TOA_Code1 = TDC_data[9] << 9 | TDC_data[10] << 8 | TDC_data[11] << 7 | TDC_data[12] << 6 | TDC_data[13] << 5 | TDC_data[14] << 4 | TDC_data[15] << 3 | TDC_data[16] << 2 | TDC_data[17] << 1 | TDC_data[18]
                        Cal_Code1 = TDC_data[19] << 9 | TDC_data[20] << 8 | TDC_data[21] << 7 | TDC_data[22] << 6 | TDC_data[23] << 5 | TDC_data[24] << 4 | TDC_data[25] << 3 | TDC_data[26] << 2 | TDC_data[27] << 1 | TDC_data[28]
                        # print(TOA_Code1, TOT_Code1, Cal_Code1, hitFlag)
                        infile.write("%3d %3d %3d %d\n"%(TOT_Code1, TOA_Code1, Cal_Code1, hitFlag))

#--------------------------------------------------------------------------#
## if statement
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#initial socket
    s.connect((hostname, port))								#connect socket
    cmd_interpret = command_interpret(s)					#Class instance
    ETROC1_ArrayReg1 = ETROC1_ArrayReg()                                # New a class
    main()													#execute main function
    s.close()												#close socket
