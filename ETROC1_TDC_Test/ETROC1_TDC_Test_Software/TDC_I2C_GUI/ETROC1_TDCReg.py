#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
'''
@author: Wei Zhang
@date: 2019-12-11
ETROC1 TDC Test Block class
'''
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

    def set_Dataout_AmplSel(self, val):                                         # Dataout TX amplitude select
        self._regMap['Dataout_AmplSel'] = 0x7 & val

    def set_DMRO_testMode(self, val):                                           # DMRO testMode select, 1: testMode 0: normal mode
        self._regMap['DMRO_testmode'] = 0x1 & val

    def set_DMRO_enable(self, val):                                             # DMRO enable, 1: enable 0: disable
        self._regMap['DMRO_enable'] = 0x1 & val

    def set_DMRO_reverse(self, val):                                            # DMRO data reverse
        self._regMap['DMRO_reverse'] = 0x1 & val

    def set_DMRO_resetn(self, val):                                             # DMRO resetn, low active
        self._regMap['DMRO_resetn'] = 0x1 & val

    def set_DMRO_revclk(self, val):                                              # DMRO reverse clock
        self._regMap['DMRO_revclk'] = 0x1 & val

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
