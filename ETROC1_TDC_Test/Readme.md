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
  - Firmware was synthesized and implemented on ***Vivado 2016.2***. The `kc705_mig.bit` or `kc705_mig.bit` file is downlaoded into KC705 EVB via Vivado 2016.2 IDE. 
  - The FPGA socket address is 192.168.2.x, The x is configurable via switch (DIP switch **SW11** positions 1 and 2 control the value of `x`, the positions 1 and 2 are **ON**, `x=3`, the position 1 is **ON** and the position 2 is **OFF**, `x=1`, and so forth) and its value ranges from 0 to 3 and the port number is fixed to 1024. [Schematic of KC705 EVB](https://www.xilinx.com/support/documentation/boards_and_kits/kc705_Schematic_xtp132_rev1_1.pdf)
```verilog
hostname = '192.168.2.3'			#FPGA IP address
port = 1024					#port number
```
  - Verify Ethernet communication
    - Before executing ping command at docs command line, we should make sure that the Ethernet interface of KC705 EVB was connected to PC RJ45 interface with a **1000M** ethernet cable. 
    - Open Windows docs command line and execute command `ping 192.168.2.3`. The below figure shows the connected and disconnected outputs after executing `ping 192.168.2.3` command.
![Ping Command](https://github.com/weizhangccnu/ETROC1_Test/blob/master/ETROC1_TDC_Test/Img/Ping_Command.PNG)
  - The GTX transceiver needs a pair of differential clock that will be provided by Si5338 EVB **CLK0A/CLK0B**. The GTX transceiver reference clock input locates on **J15/J16** SMA connectors as reference clock whose frequency is accurate **160 MHz**. The GTX transceiver isn't sensitive to the ploarity of reference clock, so you needn't take care of the ploarity when you can connect **J15/J16** SMA connectors with **CLK0A/CLK0B** SMA connectors via coxial cables.
  - The I2C SCL and SDA interface are assigned on **Pin 18 and 20** of the KC705 EVB **J46** connector. The I2C infterface mapping is shown as below figure.
![I2C interface mapping](https://github.com/weizhangccnu/ETROC1_Test/blob/master/ETROC1_TDC_Test/Img/I2C_Interface_Mapping.png)

## 3. Test Software (mainly python scripts)
  - There are two python files located on ETROC1_TDC_Test_Software directory and named *command_interpret.py* and *kc705_mig_control.py*, respectively.
    - The **command_interpret.py** file maily includes a class for socket communication.
    - The **kc705_mig_control.py** file includes all kinds of functions such as I2C write/read, DDR3 data store and fetch, Ethernet communication and so on.
  - Python version: **Python 3.7.5** is the python version that we used now.
  - **Atom editor** is the python script execution environment at SMU.
  - Before you execute the list one python scripts, you should make sure that all the modules imported at the begin of each python file have already been installed. Otherwise, you have to install all used modules with the command of `pip install modulename`.

## 4. Configure Si5338 EVB
  - [User's guide of Si5338 EVB](https://www.silabs.com/documents/public/user-guides/Si5338-EVB.pdf)
  - The Si5338 EVB is configured by ClockBuilder Pro v.2.37.0.1 [ClockBuilder Pro download link](https://www.silabs.com/products/development-tools/software/clockbuilder-pro-software)

