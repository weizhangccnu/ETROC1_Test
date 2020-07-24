#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
'''
@author: Wei Zhang
@date: Feb 26, 2020
ETROC1 Array Pixel class
'''
#--------------------------------------------------------------------------#
## Manage ETROC1 Array chip's internal registers map
# Allow combining and disassembling individual registers
class ETROC1_ArrayReg(object):
    ## @var _defaultRegMap default register values
    _defaultRegMap = {
        ## Slave I2C A
        'CLSel'                         :   0x0,
        'RfSel'                         :   0x2,
        'HysSel'                        :   0xf,
        'IBSel'                         :   0x7,
        'QSel'                          :   0x6,
        'DIS_VTHInOut7_0'               :   0xff,
        'DIS_VTHInOut15_8'              :   0xff,
        'EN_DiscriOut'                  :   0x11,
        'EN_QInj7_0'                    :   0x01,
        'EN_QInj15_8'                   :   0x00,
        'OE_DMRO_Row'                   :   0x1,
        'DMRO_Col'                      :   0x0,
        'RO_SEL'                        :   0,
        'PD_DACDiscri7_0'               :   0x00,
        'PD_DACDiscri15_8'              :   0x00,
        'VTHIn7_0'                      :   0x00,
        'VTHIn15_8'                     :   0x02,
        'VTHIn23_16'                    :   0x08,
        'VTHIn31_24'                    :   0x20,
        'VTHIn39_32'                    :   0x80,
        'VTHIn47_40'                    :   0x00,
        'VTHIn55_48'                    :   0x02,
        'VTHIn63_56'                    :   0x08,
        'VTHIn71_64'                    :   0x20,
        'VTHIn79_72'                    :   0x80,
        'VTHIn87_80'                    :   0x00,
        'VTHIn95_88'                    :   0x02,
        'VTHIn103_96'                   :   0x08,
        'VTHIn111_104'                  :   0x20,
        'VTHIn119_112'                  :   0x80,
        'VTHIn127_120'                  :   0x00,
        'VTHIn135_128'                  :   0x02,
        'VTHIn143_136'                  :   0x08,
        'VTHIn151_144'                  :   0x20,
        'VTHIn159_152'                  :   0x80,
        'ROI7_0'                        :   0xff,
        'ROI15_8'                       :   0xff,
        ## Slave I2C B
        'TDC_autoReset'                 :   0,
        'TDC_enableMon'                 :   0,
        'TDC_enable'                    :   1,
        'TDC_polaritySel'               :   1,
        'TDC_resetn'                    :   1,
        'TDC_selRawCode'                :   0,
        'TDC_testMode'                  :   0,
        'TDC_timeStampMode'             :   0,
        'TDC_level'                     :   0x1,
        'TDC_offset'                    :   0x0,
        'dllEnable'                     :   1,
        'dllForceDown'                  :   0,
        'dllCapReset'                   :   0,
        'dllCPCurrent'                  :   0x1,
        'PhaseAdj'                      :   0x0,
        'RefStrSel'                     :   0x3,
        'DMRO_ENScr'                    :   1,
        'DMRO_revclk'                   :   0,
        'DMRO_reverse'                  :   0,
        'DMRO_testMode'                 :   0,
        'TestCLK0'                      :   0,
        'TestCLK1'                      :   0,
        'CLKOutSel'                     :   1,
        'Clk1G28_equ'                   :   0x0,
        'Clk1G28_invertData'            :   0,
        'Clk1G28_enTermination'         :   1,
        'Clk1G28_setCommMode'           :   1,
        'Clk1G28_enableRx'              :   1,
        'Clk320M_equ'                   :   0x0,
        'Clk320M_invertData'            :   0,
        'Clk320M_enTermination'         :   1,
        'Clk320M_setCommMode'           :   1,
        'Clk320M_enableRx'              :   0,
        'Clk40M_equ'                    :   0x0,
        'Clk40M_invertData'             :   0,
        'Clk40M_enTermination'          :   1,
        'Clk40M_setCommMode'            :   1,
        'Clk40M_enableRx'               :   0,
        'QInj_equ'                      :   0x0,
        'QInj_invertData'               :   0,
        'QInj_enTermination'            :   1,
        'QInj_setCommMode'              :   1,
        'QInj_enableRx'                 :   1,
        'CLKTO_AmplSel'                 :   0x7,
        'CLKTO_disBIAS'                 :   0,
        'Dataout_AmplSel'               :   0x7,
        'Dataout_disBIAS'               :   0
        }
    ## @var register map local to the class
    _regMap = {}

    def __init__(self):
        self._regMap = copy.deepcopy(self._defaultRegMap)           # deep copy default register value to _regMap.

    def set_CLSel(self, val):                                       # selection of load Capacitance of the preamp first stage.
        self._regMap['CLSel'] = 0x3 & val

    def set_RfSel(self, val):                                       # selection of the feedback resistance of the preamp.
        self._regMap['RfSel'] = 0x3 & val

    def set_HysSel(self, val):                                      # Hysteresis voltage selection
        self._regMap['HysSel'] = 0xf & val

    def set_IBSel(self, val):                                       # Bias current selection of the input transistor in the preamp
        self._regMap['IBSel'] = 0x7 & val

    def set_QSel(self, val):                                        # selection of Injection charge, from 1 fC (5'b00000) to 32 fC (5'b11111).
        self._regMap['QSel'] = 0x1f & val

    def set_Dis_VTHInOut7_0(self, val):                             # Disable threshold voltage input/output of the specified pixel.
        self._regMap['DIS_VTHInOut7_0'] = 0xff & val

    def set_Dis_VTHInOut15_8(self, val):                            # Disable threshold voltage input/output of the specified pixel.
        self._regMap['DIS_VTHInOut15_8'] = 0xff & val

    def set_EN_DiscriOut(self, val):                                # Enable the Discriminator output, active high.
        self._regMap['EN_DiscriOut'] = 0xff & val

    def set_EN_QInj7_0(self, val):                                  # Enable the charge injection of the specified pixel, active high.
        self._regMap['EN_QInj7_0'] = 0xff & val

    def set_EN_QInj15_8(self, val):                                 # Enable the charge injection of the specified pixel, active high.
        self._regMap['EN_QInj15_8'] = 0xff & val

    def set_OE_DMRO_Row(self, val):                                 # Output enable of DMRO in rows.
        self._regMap['OE_DMRO_Row'] = 0xf & val

    def set_DMRO_Col(self, val):                                    # Output enable of DMRO in specified column, 2'b00 : column 0 is selected, 2'b01 : column 1 is selected, 2'b10 : column 2 is selected, 2'b11 : column 3 is selected..
        self._regMap['DMRO_Col'] = 0x3 & val

    def set_RO_SEL(self, val):                                      # 1: SRO readout mode enable.; 0: DMRO readout mode enable.
        self._regMap['RO_SEL'] = 0x1 & val

    def set_PD_DACDiscri7_0(self, val):                             # Power down the DAC and the Discriminator in Pixel
        self._regMap['PD_DACDiscri7_0'] = 0xff & val

    def set_PD_DACDiscri15_8(self, val):                            # Power down the DAC and the Discriminator in Pixel
        self._regMap['PD_DACDiscri15_8'] = 0xff & val

    def set_VTHIn7_0(self, val):                                    # Discriminator threshold voltage [7:0]
        self._regMap['VTHIn7_0'] = 0xff & val

    def set_VTHIn15_8(self, val):                                   # Discriminator threshold voltage [15:8]
        self._regMap['VTHIn15_8'] = 0xff & val

    def set_VTHIn23_16(self, val):                                  # Discriminator threshold voltage [23:16]
        self._regMap['VTHIn23_16'] = 0xff & val

    def set_VTHIn31_24(self, val):                                  # Discriminator threshold voltage [31:24]
        self._regMap['VTHIn31_24'] = 0xff & val

    def set_VTHIn39_32(self, val):                                  # Discriminator threshold voltage [39_32]
        self._regMap['VTHIn39_32'] = 0xff & val

    def set_VTHIn47_40(self, val):                                  # Discriminator threshold voltage [47_40]
        self._regMap['VTHIn47_40'] = 0xff & val

    def set_VTHIn55_48(self, val):                                  # Discriminator threshold voltage [55_48]
        self._regMap['VTHIn55_48'] = 0xff & val

    def set_VTHIn63_56(self, val):                                  # Discriminator threshold voltage [63_56]
        self._regMap['VTHIn63_56'] = 0xff & val

    def set_VTHIn71_64(self, val):                                  # Discriminator threshold voltage [71_64]
        self._regMap['VTHIn71_64'] = 0xff & val

    def set_VTHIn79_72(self, val):                                  # Discriminator threshold voltage [79_72]
        self._regMap['VTHIn79_72'] = 0xff & val

    def set_VTHIn87_80(self, val):                                  # Discriminator threshold voltage [87_80]
        self._regMap['VTHIn87_80'] = 0xff & val

    def set_VTHIn95_88(self, val):                                  # Discriminator threshold voltage [95_88]
        self._regMap['VTHIn95_88'] = 0xff & val

    def set_VTHIn103_96(self, val):                                 # Discriminator threshold voltage [103_96]
        self._regMap['VTHIn103_96'] = 0xff & val

    def set_VTHIn111_104(self, val):                                # Discriminator threshold voltage [111_104]
        self._regMap['VTHIn111_104'] = 0xff & val

    def set_VTHIn119_112(self, val):                                # Discriminator threshold voltage [119_112]
        self._regMap['VTHIn119_112'] = 0xff & val

    def set_VTHIn127_120(self, val):                                # Discriminator threshold voltage [127_120]
        self._regMap['VTHIn127_120'] = 0xff & val

    def set_VTHIn135_128(self, val):                                # Discriminator threshold voltage [135_128]
        self._regMap['VTHIn135_128'] = 0xff & val

    def set_VTHIn143_136(self, val):                                # Discriminator threshold voltage [143_136]
        self._regMap['VTHIn143_136'] = 0xff & val

    def set_VTHIn151_144(self, val):                                # Discriminator threshold voltage [151_144]
        self._regMap['VTHIn151_144'] = 0xff & val

    def set_VTHIn159_152(self, val):                                # Discriminator threshold voltage [159_152]
        self._regMap['VTHIn159_152'] = 0xff & val

    def set_ROI7_0(self, val):                                      # Region of interest, [7:0] low 8-bit vector specified
        self._regMap['ROI7_0'] = 0xff & val

    def set_ROI15_8(self, val):                                     # Region of interest, [15:8] low 8-bit vector specified
        self._regMap['ROI15_8'] = 0xff & val

    def set_TDC_autoReset(self, val):                               # 1: TDC auto reset active, 0: TDC auto reset isn't active.
        self._regMap['TDC_autoReset'] = 0x1 & val

    def set_TDC_enableMon(self, val):                               # 1: Enable TDC raw data output, 0: Disable TDC raw data output.
        self._regMap['TDC_enableMon'] = 0x1 & val

    def set_TDC_enable(self, val):                                  # 1: Enable TDC, 0: Disable TDC.
        self._regMap['TDC_enable'] = 0x1 & val

    def set_TDC_polaritySel(self, val):                             # 1: High power mdoe, 0: Low power mdoe.
        self._regMap['TDC_polaritySel'] = 0x1 & val

    def set_TDC_resetn(self, val):                                  # 1: reset active, 0: reset not active.
        self._regMap['TDC_resetn'] = 0x1 & val

    def set_TDC_selRawCode(self, val):                              # always 0.
        self._regMap['TDC_selRawCode'] = 0x1 & val

    def set_TDC_testMode(self, val):                                # 1: TDC work on test mode, 0: TDC work on normal mode.
        self._regMap['TDC_testMode'] = 0x1 & val

    def set_TDC_timeStampMode(self, val):                           # 1: Cal = Cal-TOA, 0: Cal=Cal
        self._regMap['TDC_timeStampMode'] = 0x1 & val

    def set_TDC_level(self, val):                                   # 1: bubble tolerance level
        self._regMap['TDC_level'] = 0x7 & val

    def set_TDC_offset(self, val):                                  # ripple counter window
        self._regMap['TDC_offset'] = 0x7f & val

    def set_dllEnable(self, val):                                   # 1: Enable DLL 0: Disable DLL
        self._regMap['dllEnable'] = 0x1 & val

    def set_dllForceDown(self, val):                                # 1: Force to pull down the output of the phase detector, high active.
        self._regMap['dllForceDown'] = 0x1 & val

    def set_dllCapReset(self, val):                                 # 1: Reset the control voltage of DLL to power supply
        self._regMap['dllCapReset'] = 0x1 & val

    def set_dllCPCurrent(self, val):                                # 1: Charge pump current control, ranging from 1 to 15 uA
        self._regMap['dllCPCurrent'] = 0xf & val

    def set_PhaseAdj(self, val):                                    # PhaseAdj[7:3] for coarse phase, PhaseAdj[2:0] for fine phase
        self._regMap['PhaseAdj'] = 0xff & val

    def set_RefStrSel(self, val):                                   # TDC reference strobe selection
        self._regMap['RefStrSel'] = 0xff & val

    def set_DMRO_ENScr(self, val):                                  # 1: Enable DMRO Scrambler, 0: Disable DMRO Scrambler
        self._regMap['DMRO_ENScr'] = 0x1 & val

    def set_DMRO_revclk(self, val):                                 # 1: reverse DMRO 40M clock, 0: don't reverse DMRO 40M clock
        self._regMap['DMRO_revclk'] = 0x1 & val

    def set_DMRO_testMode(self, val):                               # 1: Test Mode, PRBS7 output, 0: normal Mode
        self._regMap['DMRO_testMode'] = 0x1 & val

    def set_DMRO_testMode(self, val):                               # 1: Test Mode, PRBS7 output, 0: normal Mode
        self._regMap['DMRO_testMode'] = 0x1 & val

    def set_TestCLK0(self, val):                                    # 1: CLK320M and CLK40M comes from phase shifter, 0: CLK320M and CLK40M comes from external pads
        self._regMap['TestCLK0'] = 0x1 & val

    def set_TestCLK1(self, val):                                    # 1: CLK320M Pulse and CLK40M comes from Pulse Strobe, 0: CLK320M Pulse and CLK40M comes from MUX
        self._regMap['TestCLK1'] = 0x1 & val

    def set_CLKOutSel(self, val):                                   # 1: CLK320M Pulse Strobe Output, 0: Clk40M output
        self._regMap['CLKOutSel'] = 0x1 & val

    def set_Clk1G28_equ(self, val):                                 # 1.28G Clock input eRx equalizer strength 0-3
        self._regMap['Clk1G28_equ'] = 0x3 & val

    def set_Clk1G28_invertData(self, val):                          # 1.28G Clock input eRx data invert
        self._regMap['Clk1G28_invertData'] = 0x1 & val

    def set_Clk1G28_enTermination(self, val):                       # 1: Enable 1.28G Clock input eRx 100 Ohm termination, 0: Disable 1.28G Clock input eRx 100 Ohm termination
        self._regMap['Clk1G28_enTermination'] = 0x1 & val

    def set_Clk1G28_setCommMode(self, val):                         # 1: set common voltage and use it
        self._regMap['Clk1G28_setCommMode'] = 0x1 & val

    def set_Clk1G28_enableRx(self, val):                            # 1: Enable 1.28G clock input eRx, 0: Disable 1.28G clock input eRx
        self._regMap['Clk1G28_enableRx'] = 0x1 & val

    def set_Clk320M_equ(self, val):                                 # 320M Clock input eRx equalizer strength 0-3
        self._regMap['Clk320M_equ'] = 0x3 & val

    def set_Clk320M_invertData(self, val):                          # 320M Clock input eRx data invert
        self._regMap['Clk320M_invertData'] = 0x1 & val

    def set_Clk320M_enTermination(self, val):                       # 1: Enable 320M Clock input eRx 100 Ohm termination, 0: Disable 320M Clock input eRx 100 Ohm termination
        self._regMap['Clk320M_enTermination'] = 0x1 & val

    def set_Clk320M_setCommMode(self, val):                         # 1: set common voltage and use it
        self._regMap['Clk320M_setCommMode'] = 0x1 & val

    def set_Clk320M_enableRx(self, val):                            # 1: Enable 320M clock input eRx, 0: Disable 320M clock input eRx
        self._regMap['Clk320M_enableRx'] = 0x1 & val

    def set_Clk40M_equ(self, val):                                  # 40M Clock input eRx equalizer strength 0-3
        self._regMap['Clk40M_equ'] = 0x3 & val

    def set_Clk40M_invertData(self, val):                           # 40M Clock input eRx data invert
        self._regMap['Clk40M_invertData'] = 0x1 & val

    def set_Clk40M_enTermination(self, val):                        # 1: Enable 40M Clock input eRx 100 Ohm termination, 0: Disable 40M Clock input eRx 100 Ohm termination
        self._regMap['Clk40M_enTermination'] = 0x1 & val

    def set_Clk40M_setCommMode(self, val):                          # 1: set common voltage and use it
        self._regMap['Clk40M_setCommMode'] = 0x1 & val

    def set_Clk40M_enableRx(self, val):                             # 1: Enable 40M clock input eRx, 0: Disable 40M clock input eRx
        self._regMap['Clk40M_enableRx'] = 0x1 & val

    def set_QInj_equ(self, val):                                    # OInj input eRx equalizer strength 0-3
        self._regMap['QInj_equ'] = 0x3 & val

    def set_QInj_invertData(self, val):                             # OInj input eRx data invert
        self._regMap['QInj_invertData'] = 0x1 & val

    def set_QInj_enTermination(self, val):                          # 1: Enable OInj input eRx 100 Ohm termination, 0: Disable OInj input eRx 100 Ohm termination
        self._regMap['QInj_enTermination'] = 0x1 & val

    def set_QInj_setCommMode(self, val):                            # 1: set common voltage and use it
        self._regMap['QInj_setCommMode'] = 0x1 & val

    def set_QInj_enableRx(self, val):                               # 1: Enable OInj input eRx, 0: Disable OInj input eRx
        self._regMap['QInj_enableRx'] = 0x1 & val

    def set_CLKTO_AmplSel(self, val):                               # Test Clock output CML driver output amplitude strength from 0 to 7
        self._regMap['CLKTO_AmplSel'] = 0x7 & val

    def set_CLKTO_disBIAS(self, val):                               # 1: Disable Test Clock output CML driver BIAS, 0: Enable Test Clock output CML driver BIAS
        self._regMap['CLKTO_disBIAS'] = 0x1 & val

    def set_Dataout_AmplSel(self, val):                             # DMOR output data CML driver output amplitude strength from 0 to 7
        self._regMap['Dataout_AmplSel'] = 0x7 & val

    def set_Dataout_disBIAS(self, val):                             # 1: Disable DMOR output data CML driver BIAS, 0: Enable DMOR output data CML driver BIAS
        self._regMap['Dataout_disBIAS'] = 0x1 & val

    ## get I2C register value
    def get_config_vector(self):
        reg_value = []

        ## I2C Slave A
        reg_value += [self._regMap['HysSel'] << 4 | self._regMap['RfSel'] << 2 | self._regMap['CLSel']]
        reg_value += [self._regMap['QSel'] << 3 | self._regMap['IBSel']]
        reg_value += [self._regMap['DIS_VTHInOut7_0']]
        reg_value += [self._regMap['DIS_VTHInOut15_8']]
        reg_value += [self._regMap['EN_DiscriOut']]
        reg_value += [self._regMap['EN_QInj7_0']]
        reg_value += [self._regMap['EN_QInj15_8']]
        reg_value += [self._regMap['RO_SEL'] << 6 | self._regMap['DMRO_Col'] << 4 | self._regMap['OE_DMRO_Row']]
        reg_value += [self._regMap['PD_DACDiscri7_0']]
        reg_value += [self._regMap['PD_DACDiscri15_8']]
        reg_value += [self._regMap['VTHIn7_0']]
        reg_value += [self._regMap['VTHIn15_8']]
        reg_value += [self._regMap['VTHIn23_16']]
        reg_value += [self._regMap['VTHIn31_24']]
        reg_value += [self._regMap['VTHIn39_32']]
        reg_value += [self._regMap['VTHIn47_40']]
        reg_value += [self._regMap['VTHIn55_48']]
        reg_value += [self._regMap['VTHIn63_56']]
        reg_value += [self._regMap['VTHIn71_64']]
        reg_value += [self._regMap['VTHIn79_72']]
        reg_value += [self._regMap['VTHIn87_80']]
        reg_value += [self._regMap['VTHIn95_88']]
        reg_value += [self._regMap['VTHIn103_96']]
        reg_value += [self._regMap['VTHIn111_104']]
        reg_value += [self._regMap['VTHIn119_112']]
        reg_value += [self._regMap['VTHIn127_120']]
        reg_value += [self._regMap['VTHIn135_128']]
        reg_value += [self._regMap['VTHIn143_136']]
        reg_value += [self._regMap['VTHIn151_144']]
        reg_value += [self._regMap['VTHIn159_152']]
        reg_value += [self._regMap['ROI7_0']]
        reg_value += [self._regMap['ROI15_8']]

        ## I2C Slave B
        reg_value += [self._regMap['TDC_timeStampMode'] << 7 | self._regMap['TDC_testMode'] << 6 | self._regMap['TDC_selRawCode'] << 5 | self._regMap['TDC_resetn'] << 4 | self._regMap['TDC_polaritySel'] << 3 | self._regMap['TDC_enable'] << 2 | self._regMap['TDC_enableMon'] << 1 | self._regMap['TDC_autoReset']]
        reg_value += [self._regMap['TDC_level']]
        reg_value += [self._regMap['TDC_offset']]
        reg_value += [self._regMap['dllCPCurrent'] << 3 | self._regMap['dllCapReset'] << 2 | self._regMap['dllForceDown'] << 1 | self._regMap['dllEnable']]
        reg_value += [self._regMap['PhaseAdj']]
        reg_value += [self._regMap['RefStrSel']]
        reg_value += [self._regMap['CLKOutSel'] << 6 | self._regMap['TestCLK1'] << 5 | self._regMap['TestCLK0'] << 4 | self._regMap['DMRO_testMode'] << 3 | self._regMap['DMRO_reverse'] << 2 | self._regMap['DMRO_revclk'] << 1 | self._regMap['DMRO_ENScr']]
        reg_value += [self._regMap['Clk1G28_enableRx'] << 5 | self._regMap['Clk1G28_setCommMode'] << 4 | self._regMap['Clk1G28_enTermination'] << 3 | self._regMap['Clk1G28_invertData'] << 2  | self._regMap['Clk1G28_equ']]
        reg_value += [self._regMap['Clk320M_enableRx'] << 5 | self._regMap['Clk320M_setCommMode'] << 4 | self._regMap['Clk320M_enTermination'] << 3 | self._regMap['Clk320M_invertData'] << 2  | self._regMap['Clk320M_equ']]
        reg_value += [self._regMap['Clk40M_enableRx'] << 5 | self._regMap['Clk40M_setCommMode'] << 4 | self._regMap['Clk40M_enTermination'] << 3 | self._regMap['Clk40M_invertData'] << 2  | self._regMap['Clk40M_equ']]
        reg_value += [self._regMap['QInj_enableRx'] << 5 | self._regMap['QInj_setCommMode'] << 4 | self._regMap['QInj_enTermination'] << 3 | self._regMap['QInj_invertData'] << 2  | self._regMap['QInj_equ']]
        reg_value += [self._regMap['Dataout_disBIAS'] << 7 | self._regMap['Dataout_AmplSel'] << 4 | self._regMap['CLKTO_disBIAS'] << 3 | self._regMap['CLKTO_AmplSel']]
        return reg_value
