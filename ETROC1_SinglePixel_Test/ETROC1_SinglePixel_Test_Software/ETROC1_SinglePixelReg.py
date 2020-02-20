#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
'''
@author: Wei Zhang
@date: Feb 15, 2020
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
        'VTHIn7_0'                      :   0x0,
        'VTHIn9_8'                      :   0x2,
        'EN_QInj'                       :   1,
        'EN_DiscriOut'                  :   0,
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

    def set_DMRO_resetn(self, val):                                 # TDC reset, low active
        self._regMap['DMRO_resetn'] = 0x1 & val

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

    def set_CLSel(self, val):                                       # PreAmplifier Load Capacitance, from 0 to 3.
        self._regMap['CLSel'] = 0x3 & val

    def set_RfSel(self, val):                                       # PreAmplifier feedback resistance, from 0 to 3.
        self._regMap['RfSel'] = 0x3 & val

    def set_HysSel(self, val):                                      # Discriminator Hysteresis selection from 0 to 15
        self._regMap['HysSel'] = 0xf & val

    def set_IBSel(self, val):                                       # PreAmplifier Bias current strength, from 0 to 7
        self._regMap['IBSel'] = 0x7 & val

    def set_QSel(self, val):                                        # Charge Injection selection, from 0 to 31.
        self._regMap['QSel'] = 0x1f & val

    def set_VTHIn7_0(self, val):                                    # DAC[7:0] input digital data
        self._regMap['VTHIn7_0'] = 0xff & val

    def set_VTHIn9_8(self, val):                                    # DAC[9:8] input digital data
        self._regMap['VTHIn9_8'] = 0x3 & val

    def set_EN_QInj(self, val):                                     # 1: Enable Charge Injection, 0: Disable Charge Injection.
        self._regMap['EN_QInj'] = 0x1 & val

    def set_EN_DiscriOut(self, val):                                # 1: Enable Discriminator Output, 0: Disable Discriminator Output.
        self._regMap['EN_DiscriOut'] = 0x1 & val

    def set_Dis_VTHInOut(self, val):                                # 1: Disable DAC analog voltage output, 0: Enable DAC analog voltage output.
        self._regMap['Dis_VTHInOut'] = 0x1 & val

    def set_PD_DACDiscri(self, val):                                # 1: Power down DAC and Discriminator, 0: Power on DAC and Discriminator.
        self._regMap['PD_DACDiscri'] = 0x1 & val

    def set_OE_DMRO(self, val):                                     # 1: Enable DMRO output, 0: Disable DMRO output.
        self._regMap['OE_DMRO'] = 0x1 & val

    ## get I2C register value
    def get_config_vector(self):
        reg_value = []
        reg_value += [hex(self._regMap['TDC_timeStampMode'] << 7 | self._regMap['TDC_testMode'] << 6 | self._regMap['TDC_selRawCode'] << 5 | self._regMap['TDC_resetn'] << 4 | self._regMap['TDC_polaritySel'] << 3 | self._regMap['TDC_enable'] << 2 | self._regMap['TDC_enableMon'] << 1 | self._regMap['TDC_autoReset'])]
        reg_value += [hex(self._regMap['TDC_level'])]
        reg_value += [hex(self._regMap['TDC_offset'])]
        reg_value += [hex(self._regMap['dllCPCurrent'] << 3 | self._regMap['dllCapReset'] << 2 | self._regMap['dllForceDown'] << 1 | self._regMap['dllEnable'])]
        reg_value += [hex(self._regMap['PhaseAdj'])]
        reg_value += [hex(self._regMap['RefStrSel'])]
        reg_value += [hex(self._regMap['CLKOutSel'] << 7 | self._regMap['TestCLK1'] << 6 | self._regMap['TestCLK0'] << 5 | self._regMap['DMRO_testMode'] << 4 | self._regMap['DMRO_reverse'] << 3 | self._regMap['DMRO_revclk'] << 2 | self._regMap['DMRO_ENScr'] << 1 | self._regMap['DMRO_resetn'])]
        reg_value += [hex(self._regMap['Clk1G28_enableRx'] << 5 | self._regMap['Clk1G28_setCommMode'] << 4 | self._regMap['Clk1G28_enTermination'] << 3 | self._regMap['Clk1G28_invertData'] << 2  | self._regMap['Clk1G28_equ'])]
        reg_value += [hex(self._regMap['Clk320M_enableRx'] << 5 | self._regMap['Clk320M_setCommMode'] << 4 | self._regMap['Clk320M_enTermination'] << 3 | self._regMap['Clk320M_invertData'] << 2  | self._regMap['Clk320M_equ'])]
        reg_value += [hex(self._regMap['Clk40M_enableRx'] << 5 | self._regMap['Clk40M_setCommMode'] << 4 | self._regMap['Clk40M_enTermination'] << 3 | self._regMap['Clk40M_invertData'] << 2  | self._regMap['Clk40M_equ'])]
        reg_value += [hex(self._regMap['QInj_enableRx'] << 5 | self._regMap['QInj_setCommMode'] << 4 | self._regMap['QInj_enTermination'] << 3 | self._regMap['QInj_invertData'] << 2  | self._regMap['QInj_equ'])]
        reg_value += [hex(self._regMap['Dataout_disBIAS'] << 7 | self._regMap['Dataout_AmplSel'] << 4 | self._regMap['CLKTO_disBIAS'] << 3 | self._regMap['CLKTO_AmplSel'])]
        reg_value += [hex(self._regMap['HysSel'] << 4 | self._regMap['RfSel'] << 2 | self._regMap['CLSel'])]
        reg_value += [hex(self._regMap['QSel'] << 3 | self._regMap['IBSel'])]
        reg_value += [hex(self._regMap['VTHIn7_0'])]
        reg_value += [hex(self._regMap['OE_DMRO'] << 6 | self._regMap['PD_DACDiscri'] << 5 | self._regMap['Dis_VTHInOut'] << 4 | self._regMap['EN_DiscriOut'] << 3 | self._regMap['EN_QInj'] << 2 | self._regMap['VTHIn9_8'])]
        return reg_value

# def main():
#    ETROC1_SinglePixelReg1 = ETROC1_SinglePixelReg()
   # ETROC1_SinglePixelReg1.set_TDC_timeStampMode(1)
   # ETROC1_SinglePixelReg1.set_TDC_autoReset(0)
   # ETROC1_SinglePixelReg1.set_TDC_enable(0)
   # ETROC1_SinglePixelReg1.set_TDC_offset(127)
   # ETROC1_SinglePixelReg1.set_TDC_level(6)
   # ETROC1_SinglePixelReg1.set_PhaseAdj(255)
   # # ETROC1_SinglePixelReg1.set_QInj_enableRx(0)
   # # ETROC1_SinglePixelReg1.set_QInj_setCommMode(0)
   # ETROC1_SinglePixelReg1.set_Dataout_disBIAS(0)
   # ETROC1_SinglePixelReg1.set_Dataout_AmplSel(2)
   # ETROC1_SinglePixelReg1.set_VTHIn7_0(255)
#   print(ETROC1_SinglePixelReg1.get_config_vector())
#
#if __name__ == "__main__":
#    main()
