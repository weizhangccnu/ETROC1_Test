## 1. Documents Organization
  - **ETROC1_TDC_Design_Document:** This document is used to guide the ETROC1 TDC test.
  - **ETROC1_TDC_Test_Firmware:** To organize the ETROC1 TDC test related firmware.
  - **ETROC1_TDC_Test_Software:** To organize the ETROC1 TDC test Python scprit.
  - **Si5338_EVB_Document:** To organize the *Si5338* EVB related documents and configuration files.
  - **Img:** To store readme file used images or figures.
 
## 2. KC705 EVB Configuration and Firmware architecture.
  - The KC705 EVB is the controller between PC and ETROC1 TDC Test board and it includes GTX transceiver, I2C master, Ethernet interface, DDR3 and so on. The KC705 EVB picture is shown as below figure:
![KC705 EVB](https://github.com/weizhangccnu/ETROC1_Test/blob/master/ETROC1_TDC_Test/Img/KC705_EVB.png) 
  - Configure KC705 EVB download mode The DIP switch **SW13** position 3,4, and 5 control determine the configuration mode and the configuration mode is used at power-up or when the PROG pushbutton is pressed. The SW13 should be set as shown the below figure.
![Configuration mode](https://github.com/weizhangccnu/Python_Script/blob/master/ETROC1_TDC_Test_Software/Img/FPGA_Configuration_mode.png)
  -Download `kc705_mig.bit` or `kc705_mig.bit` file into KC705 EVB.

## 3. Test Software (mainly python scripts)

