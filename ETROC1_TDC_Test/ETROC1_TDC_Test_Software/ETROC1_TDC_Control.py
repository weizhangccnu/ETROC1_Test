#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import copy
import time
import visa
import datetime
import struct
import socket
import winsound
import heartrate
from command_interpret import *
from ETROC1_TDCReg import *
import numpy as np
from command_interpret import *
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
    cmd_interpret.write_pulse_reg(0x0040)           # reset ddr3 control logic
    time.sleep(0.01)
    print("sent pulse!")

    write_data_into_ddr3(1, 0x0000000, 0x7000000)   # set write begin address and post trigger address and wrap around
    cmd_interpret.write_pulse_reg(0x0008)           # writing start
    time.sleep(0.1)
    cmd_interpret.write_config_reg(0, 0x0001)       # written enable fifo32to256
    time.sleep(0.1)
    cmd_interpret.write_pulse_reg(0x0010)           # writing stop

    time.sleep(4)
    cmd_interpret.write_config_reg(0, 0x0000)       # write enable fifo32to256
    time.sleep(4)
    read_data_from_ddr3(0x7000000)                  # set read begin address

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
## Enable FPGA Descrambler
def Enable_FPGA_Descrablber(val):
    print("val: %d"%val)
    cmd_interpret.write_config_reg(14, 0x0001 & val)       # write enable
#--------------------------------------------------------------------------#
## main functionl
def main():

    slave_addr = 0x23                                       # I2C slave address

    userdefinedir = "TDC_Random_Occupancy=5%_PulseStrobe_0x03"

    ##  Creat a directory named path with date of today
    today = datetime.date.today()
    todaystr = today.isoformat() + "_Standalone_TDC_Test_Results"
    try:
        os.mkdir(todaystr)
        print("Directory %s was created!"%todaystr)
    except FileExistsError:
        print("Directory %s already exists!"%todaystr)
    userdefine_dir = todaystr + "./%s"%userdefinedir
    try:
        os.mkdir(userdefine_dir)
    except FileExistsError:
        print("User define directories already created!!!")

    ## setting parameters
    Pulse_Strobe = 0x03                 # 0x03: 3.125 ns Cal Code
    Board_Num = 1                       # Board Number
    testMode = 0                        # 0: nromal mode 1: test mode
    polaritySel = 1                     # 0: high power mode, 1: low power mode
    Total_point = 400                   # total fetch data = Total_point * 50000
    fetch_data = 1

    reg_val = []
    ETROC1_TDCReg1 = ETROC1_TDCReg()
    ## GRO Test Contorl
    ETROC1_TDCReg1.set_GRO_Start(1)
    ETROC1_TDCReg1.set_GRO_TOA_CK(1)
    ETROC1_TDCReg1.set_GRO_TOT_CK(1)
    ETROC1_TDCReg1.set_GROout_disCMLDriverBISA(0)
    ETROC1_TDCReg1.set_GROout_AmplSel(7)
    ETROC1_TDCReg1.set_GRO_TOARST_N(1)
    ETROC1_TDCReg1.set_GRO_TOTRST_N(1)

    ## Clock 40MHz TX output setting
    ETROC1_TDCReg1.set_Clk40Mout_AmplSel(7)
    ETROC1_TDCReg1.set_Pulse_enableRx(1)

    ## Data output setting
    ETROC1_TDCReg1.set_Dataout_AmplSel(7)
    ETROC1_TDCReg1.set_Dataout_Sel(1)

    ## Strobe pulse setting
    ETROC1_TDCReg1.set_Pulse_Sel(Pulse_Strobe)


    ## DMRO setting
    ETROC1_TDCReg1.set_DMRO_testMode(0)
    ETROC1_TDCReg1.set_DMRO_enable(1)           ## enable Scrambler
    Enable_FPGA_Descrablber(1)                  ## Enable FPGA Firmware Descrambler

    ETROC1_TDCReg1.set_DMRO_resetn(1)
    ETROC1_TDCReg1.set_DMRO_revclk(0)
    ## TDC setting
    ETROC1_TDCReg1.set_TDC_resetn(1)
    ETROC1_TDCReg1.set_TDC_testMode(testMode)
    ETROC1_TDCReg1.set_TDC_autoReset(0)
    ETROC1_TDCReg1.set_TDC_enable(1)
    ETROC1_TDCReg1.set_TDC_level(1)
    ETROC1_TDCReg1.set_TDCRawData_Sel(0)

    ETROC1_TDCReg1.set_TDC_polaritySel(polaritySel)       ## 1: low power mode 0: high power mode
    ETROC1_TDCReg1.set_TDC_timeStampMode(0)

    reg_val = ETROC1_TDCReg1.get_config_vector()
    print("I2C write in data:")
    print(reg_val)
    for i in range(len(reg_val)):
        iic_write(1, slave_addr, 0, i, reg_val[i])
    iic_read_val = []
    for i in range(len(reg_val)):
        iic_read_val += [iic_read(0, slave_addr, 1, i)]
    print("I2C read back data:")
    print(iic_read_val)

    # compare I2C write in data with I2C read back data
    if iic_read_val == reg_val:
        print("Wrote into data matches with read back data!")
        winsound.Beep(1000, 500)
    else:
        print("Wrote into data doesn't matche with read back data!!!!")
        for x in range(3):
            winsound.Beep(1000, 500)


    readonly_reg = [0x21, 0x22, 0x23, 0x24]
    readonly_val = []
    for i in range(len(readonly_reg)):
        readonly_val += [iic_read(0, slave_addr, 1, readonly_reg[i])]
    print(readonly_val)
    TOA_Code = (readonly_val[2] & 0x7) << 7 | ((readonly_val[1] >> 1) & 0x7f)
    TOT_Code = (readonly_val[1] & 0x1) << 8 | readonly_val[0]
    Cal_Code = (readonly_val[3] & 0x1f) << 5 | (readonly_val[2] >> 3) & 0x1f
    print("TOA_Code: %d"%TOA_Code)
    print("TOT_Code: %d"%TOT_Code)
    print("Cal_Code: %d"%Cal_Code)

    if fetch_data == 1:                 # fetch data switch
        time_stamp = time.strftime('%m-%d_%H-%M-%S',time.localtime(time.time()))
        filename = "TDC_Data_Random_Occupancy=5_TestMode=%d_polaritySel=%d_PulseStrobe=%s_B%d_%s_%s.dat"%(testMode, polaritySel, hex(Pulse_Strobe), Board_Num, Total_point*50000, time_stamp)
        print(filename)
        with open("./%s/%s/%s"%(todaystr, userdefinedir, filename), 'w') as infile:

            data_out = [0]
            data_out = test_ddr3(Total_point)      # num: The total fetch data num * 50000
            print("Start store data......")

            for i in range(len(data_out)):
                TDC_data = []
                for j in range(30):
                    TDC_data += [((data_out[i] >> j) & 0x1)]
                hitFlag = TDC_data[29]
                TOT_Code1 = TDC_data[0] << 8 | TDC_data[1] << 7 | TDC_data[2] << 6 | TDC_data[3] << 5 | TDC_data[4] << 4 | TDC_data[5] << 3 | TDC_data[6] << 2 | TDC_data[7] << 1 | TDC_data[8]
                TOA_Code1 = TDC_data[9] << 9 | TDC_data[10] << 8 | TDC_data[11] << 7 | TDC_data[12] << 6 | TDC_data[13] << 5 | TDC_data[14] << 4 | TDC_data[15] << 3 | TDC_data[16] << 2 | TDC_data[17] << 1 | TDC_data[18]
                Cal_Code1 = TDC_data[19] << 9 | TDC_data[20] << 8 | TDC_data[21] << 7 | TDC_data[22] << 6 | TDC_data[23] << 5 | TDC_data[24] << 4 | TDC_data[25] << 3 | TDC_data[26] << 2 | TDC_data[27] << 1 | TDC_data[28]
                infile.write("%3d %3d %3d %d\n"%(TOA_Code1, TOT_Code1, Cal_Code1, hitFlag))

if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#initial socket
	s.connect((hostname, port))								#connect socket
	cmd_interpret = command_interpret(s)					#Class instance
	main()													#execute main function
	s.close()												#close socket
