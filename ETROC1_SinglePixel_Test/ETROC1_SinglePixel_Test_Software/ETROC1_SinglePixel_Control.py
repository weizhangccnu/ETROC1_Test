#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import copy
import time
import visa
import struct
import socket
import heartrate
import numpy as np
from command_interpret import *
from ETROC1_SinglePixelReg import *
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
'''
@author: Wei Zhang
@date: 2021-05-24
This script is used for testing ETROC1 SinglePixel chip. The mianly function of this script is I2C write and read, Ethernet communication, instrument control and so on.
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
# @param[in] data_num: set fetch data number
def test_ddr3(data_num):
    cmd_interpret.write_config_reg(0, 0x0000)       # written disable
    cmd_interpret.write_pulse_reg(0x0004)           # reset ddr3 logic, data fifo, and fifo32to256 
    time.sleep(0.01)
    print("sent pulse!")

    write_data_into_ddr3(1, 0x0000000, 0x6000000)   # set write begin address and post trigger address and wrap around
    cmd_interpret.write_pulse_reg(0x0008)           # writing start
    time.sleep(0.1)
    cmd_interpret.write_config_reg(0, 0x0001)       # written enable fifo32to256

    time.sleep(0.1)
    cmd_interpret.write_pulse_reg(0x0010)           # writing stop
    time.sleep(0.1)                             
    cmd_interpret.write_config_reg(0, 0x0001)       # fifo32to256 writen enablee 

    time.sleep(1)                                   # delay 2s to receive data
    cmd_interpret.write_config_reg(0, 0x0000)       # fifo32to256 write disablee
    time.sleep(3)
    read_data_from_ddr3(0x0600000)                  # set read begin address

    data_out = []
    for i in range(data_num):                       # reading start
        data_out += cmd_interpret.read_data_fifo(50000)           
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
def Enable_FPGA_Descramblber(val):
    if val==1:
        print("Enable FPGA Descrambler")
    else:
        print("Disable FPGA Descrambler")
    cmd_interpret.write_config_reg(14, 0x0001 & val)       # write enable
#--------------------------------------------------------------------------#
## main functionl
def main():
    slave_addr = 0x4E                                               # I2C slave address
    
    userdefineddir = "Single_Pixel_QSel=15fC_Qinj=1M25_Phase=100_B1"
    userdefineddir = "Single_Pixel_QSel=15fC_Qinj=1M25_Phase=100_B1_log"

    today = datetime.date.today()
    todaystr = today.isoformat() + "_Array_Test_Results"
    try:
        os.mkdir(todaystr)
        print("Directory %s was created!"%todaystr)
    except FileExistsError:
        print("Directory %s has already existed!"%todaystr)

    userdefine_dir = todaystr + "./%s"%userdefineddir
    userdefine_dir_log = todaystr + "./%s"%userdefineddir_log
    try:
        os.mkdir(userdefine_dir)
        os.mkdir(userdefine_dir_log)
        print("User defined directories was created!!!")
    except FileExistsError:
        print("User defined directories have already existed!!!")

    # charge injection settings
    Enable_QInj = 1                                                 # Enable charge injection
    QSel = 20
    # PreAmp settings
    CLSel = 0                                                       # PreAmp capacitor load
    RfSel = 2                                                       # PreAmp feedback resistor
    IBSel = 7                                                       # PreAmp Bias current
    # Discriminator settings
    HysSel = 0xf                                                    # Discriminator Hysteresis
    # DAC settings
    DAC = 400
    # TDC settings

    Test_Pattern_Output = 1                                         # 1: Data from test pattern, 0: Data from TDC
    Enable_FPGA_Descrambler = 1                                     # 1: Enable FPGA Descrambler, 0: Disable FPGA Descrambler

    Fetch_Data = 0                                                  # 1: Turn on fetch data switch, 0: Turn off fetch data switch
    

    reg_val = []
    ETROC1_SinglePixelReg1 = ETROC1_SinglePixelReg()                # New a class
    
    ETROC1_SinglePixelReg1.set_VTHIn7_0(DAC & 0xff)                 # DAC value configuration
    ETROC1_SinglePixelReg1.set_VTHIn9_8((DAC >> 8) & 0xff)

    ETROC1_SinglePixelReg1.set_EN_QInj(Enable_QInj)                 # 1: enable charge injection, 0: disable charge injection
    ETROC1_SinglePixelReg1.set_TDC_selRawCode(Test_Pattern_Output)  # 1: data comes from Test Pattern, 0: data comes from TDC

    Enable_FPGA_Descramblber(Enable_FPGA_Descrambler)               # 1: Enable FPGA Descrambler 0: Disable FPGA Descrambler
    reg_val = ETROC1_SinglePixelReg1.get_config_vector()            # Get Single Pixel Register default data
    print("I2C write in data:")
    print(reg_val)
    for i in range(len(reg_val)):                                   # Write data into I2C register
        iic_write(1, slave_addr, 0, i, int(reg_val[i], 16))
    time.sleep(0.1)

    iic_read_val = []
    for i in range(len(reg_val)):                                   # Read back I2C register value
        iic_read_val += [iic_read(0, slave_addr, 1, i)]
    print("I2C read back data:")
    print(iic_read_val)


    # Receive DMRO output data and store it to dat file
    if Fetch_Data == 1:
        time_stampe = time.strftime('%m-%d_%H-%M-%S',time.localtime(time.time()))
        if Test_Pattern_Output == 1:
            filename = "SinglePixel_TEST_DAC=%d_QSel=%d_CLSel=%d_RfSel=%d_IBSel=%d_PhaseAdj=%03d_B%s_%s_%s.dat"%(DAC_Value, QSel, CLSel, RfSel, IBSel, PhaseAdj, Board_num, Total_point*50000, time_stampe)
        else:
            filename = "SinglePixel_TDC_DAC=%d_QSel=%d_CLSel=%d_RfSel=%d_IBSel=%d_PhaseAdj=%03d_B%s_%s_%s.dat"%(DAC_Value, QSel, CLSel, RfSel, IBSel, PhaseAdj, Board_num, Total_point*50000, time_stampe)
        
        print("filename is: %s"%filename)
        print("Fetching file...")
        time.sleep(1)
        data_out = []
        data_out = test_ddr3(Total_point)                           ## num: The total fetch data num * 50000

        with open("./%s/%s/%s"%(todaystr, userdefinedir, filename),'w') as infile:
            for i in range(len(data_out)):
                if Test_Pattern_Output == 1:
                    Bit = (data_out[i] & 0x3ff00000) >> 20
                    VthIN = (data_out[i] & 0x000f0000) >> 16
                    Counter = data_out[i] & 0x0000ffff
                    infile.write("%3d %2d %5d\n"%(Bit, VthIN, Counter))
                else:
                    TDC_data = []
                    for j in range(30):
                        TDC_data += [((data_out[i] >> j) & 0x1)]
                    hitFlag = TDC_data[0]
                    TOT_Code1 = TDC_data[29] << 8 | TDC_data[28] << 7 | TDC_data[27] << 6 | TDC_data[26] << 5 | TDC_data[25] << 4 | TDC_data[24] << 3 | TDC_data[23] << 2 | TDC_data[22] << 1 | TDC_data[21]
                    TOA_Code1 = TDC_data[20] << 9 | TDC_data[19] << 8 | TDC_data[18] << 7 | TDC_data[17] << 6 | TDC_data[16] << 5 | TDC_data[15] << 4 | TDC_data[14] << 3 | TDC_data[13] << 2 | TDC_data[12] << 1 | TDC_data[11]
                    Cal_Code1 = TDC_data[10] << 9 | TDC_data[9] << 8 | TDC_data[8] << 7 | TDC_data[7] << 6 | TDC_data[6] << 5 | TDC_data[5] << 4 | TDC_data[4] << 3 | TDC_data[3] << 2 | TDC_data[2] << 1 | TDC_data[1]
                    # print(TOA_Code1, TOT_Code1, Cal_Code1, hitFlag)
                    infile.write("%3d %3d %3d %d\n"%(TOA_Code1, TOT_Code1, Cal_Code1, hitFlag))

#--------------------------------------------------------------------------#
## if statement
if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#initial socket
	s.connect((hostname, port))								#connect socket
	cmd_interpret = command_interpret(s)					#Class instance
	main()													#execute main function
	s.close()												#close socket
