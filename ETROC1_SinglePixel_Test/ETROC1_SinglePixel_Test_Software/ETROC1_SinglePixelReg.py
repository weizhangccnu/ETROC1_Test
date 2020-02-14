#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
'''
@author: Wei Zhang
@date: 2019-12-11
ETROC1 Single Pixel class
'''
#--------------------------------------------------------------------------#
## Manage ETROC1 SinglePixel chip's internal registers map
# Allow combining and disassembling individual registers
class ETROC1_SinglePixelReg(object):
    ## @var _defaultRegMap default register values
    _defaultRegMap = {
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
        'DMRO_resetn'                   :   1,
        'DMRO_ENScr'                    :   1,
        'DMRO_reclk'                    :   0,
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
        'Clk320M_enableRx'              :   1,
        'Clk40M_equ'                    :   0x0,
        'Clk40M_invertData'             :   0,
        'Clk40M_enTermination'          :   1,
        'Clk40M_setCommMode'            :   1,
        'Clk40M_enableRx'               :   1,
        'QInj_equ'                      :   0x0,
        'QInj_invertData'               :   0,
        'QInj_enTermination'            :   1,
        'QInj_setCommMode'              :   1,
        'QInj_enableRx'                 :   1,
        'CLKTO_AmplSel'                 :   0x7,
        'CLKTO_disBIAS'                 :   0,
        'Dataout_AmplSel'               :   0x7,
        'Dataout_disBIAS'               :   0,
        'CLSel'                         :   0x0,
        'RfSel'                         :   0x2,
        'HysSel'                        :   0xf,
        'IBSel'                         :   0x7,
        'QSel'                          :   0x6,
        'VTHIn[7:0]'                    :   0x0,
        'VTHIn[9:8]'                    :   0x2,
        'En_Qinj'                       :   1,
        'En_DiscriOut'                  :   0,
        'Dis_VTHInOut'                  :   1,
        'PD_DACDiscri'                  :   0,
        'OE_DMRO'                       :   1,
        }
    ## @var register map local to the class
    _regMap = {}

    def __init__(self):
        self._regMap = copy.deepcopy(self._defaultRegMap)

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


    ## get I2C register value
    def get_config_vector(self):
        reg_value = []
        reg_value += [hex(self._regMap['TDC_timeStampMode'] << 7 | self._regMap['TDC_testMode'] << 6 | self._regMap['TDC_selRawCode'] << 5 | self._regMap['TDC_resetn'] << 4 | self._regMap['TDC_polaritySel'] << 3 | self._regMap['TDC_enable'] << 2 | self._regMap['TDC_enableMon'] << 1 | self._regMap['TDC_autoReset'])]
        reg_value += [hex(self._regMap['TDC_level'] << 3 | self._regMap['TDC_offset'])]
        reg_value += [hex(self._regMap['dllCPCurrent'] << 3 | self._regMap['dllCapReset'] << 2 | self._regMap['dllForceDown'] << 1 | self._regMap['dllEnable'])]
        
        return reg_value

def main():
   ETROC1_SinglePixelReg1 = ETROC1_SinglePixelReg()
   ETROC1_SinglePixelReg1.set_TDC_timeStampMode(1)
   ETROC1_SinglePixelReg1.set_TDC_autoReset(0)
   ETROC1_SinglePixelReg1.set_TDC_enable(0)

   print(ETROC1_SinglePixelReg1.get_config_vector())

if __name__ == "__main__":
    main()
