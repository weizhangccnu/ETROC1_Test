-- $Id: i2c_tic.vhd  Dong Wang $
-------------------------------------------------------------------------------
-- Title      : i2c read and write in cycle
-- Project    : MIMOSA readout
-------------------------------------------------------------------------------
-- File       : i2c_tic.vhd
-- Author     : Dong Wang
-- Company    : Central China Normal University
-- Created    : 2017-3-15
-- Last update:
-- Platform   : Linux Vivado 2015.4.2
-- Target     : KC705
-- Standard   : VHDL'93/02
-------------------------------------------------------------------------------
-- Description: continuous read and write from i2c command register
-- 6 command register is used for cycling buffer
-------------------------------------------------------------------------------
-- Copyright (c) 2017
-------------------------------------------------------------------------------
-- Revisions  :
-- Date        Version  Author        Description
-- 2017-3-15  1.0      Dong      Created
-------------------------------------------------------------------------------
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE ieee.std_logic_unsigned.all;

ENTITY i2c_tic IS
  PORT (
    CLK      : IN  std_logic;           --  system clock 60Mhz
    RESET    : IN  std_logic;           --  active high reset

    START    : OUT  std_logic;           -- the rising edge trigger a start, generate by config_reg
    MODE     : OUT  std_logic_vector(1 DOWNTO 0);          -- '0' is 1 bytes read or write, '1' is 2 bytes read or write,
                                                          -- '2' is 3 bytes write only , don't set to '3'
    SL_WR    : OUT  std_logic;           -- '0' is write, '1' is read
    SL_ADDR  : OUT  std_logic_vector(6 DOWNTO 0);  -- slave addr
    WR_ADDR  : OUT  std_logic_vector(7 DOWNTO 0);  -- chip internal addr for read and write
    WR_DATA0 : OUT  std_logic_vector(7 DOWNTO 0);  -- first byte data for write
    WR_DATA1 : OUT  std_logic_vector(7 DOWNTO 0);  -- second byte data for write
    RD_DATA0 : IN   std_logic_vector(7 DOWNTO 0);  -- first byte readout
    RD_DATA1 : IN   std_logic_vector(7 DOWNTO 0);  -- second byte readout

    COMMAND0 : IN  std_logic_vector(34 DOWNTO 0);
    COMMAND1 : IN  std_logic_vector(34 DOWNTO 0);
    COMMAND2 : IN  std_logic_vector(34 DOWNTO 0);
    COMMAND3 : IN  std_logic_vector(34 DOWNTO 0);
    COMMAND4 : IN  std_logic_vector(34 DOWNTO 0);
    COMMAND5 : IN  std_logic_vector(34 DOWNTO 0);

    DATA0    : OUT std_logic_vector(15 DOWNTO 0);
    DATA1    : OUT std_logic_vector(15 DOWNTO 0);
    DATA2    : OUT std_logic_vector(15 DOWNTO 0);
    DATA3    : OUT std_logic_vector(15 DOWNTO 0);
    DATA4    : OUT std_logic_vector(15 DOWNTO 0);
    DATA5    : OUT std_logic_vector(15 DOWNTO 0)
    );
END i2c_tic;

ARCHITECTURE arch OF i2c_tic IS

  SIGNAL sTicCnt        : std_logic_vector(23 DOWNTO 0);
  SIGNAL signA          : std_logic;
  SIGNAL signB          : std_logic;

BEGIN

  tic_counter : PROCESS (CLK, RESET) IS
  BEGIN
    IF RESET = '1' THEN                 -- asynchronous reset (active high)
      sTicCnt <= (others => '0');
    ELSIF rising_edge(CLK) THEN
      sTicCnt <= sTicCnt + '1';
    END IF;
  END PROCESS;
  
  PROCESS (CLK, RESET) IS
    BEGIN
      IF RESET = '1' THEN                 -- asynchronous reset (active high)
        signA <= '0';
        signB <= '0';
      ELSIF rising_edge(CLK) THEN
        IF COMMAND5(34) = '1' THEN
            signA <= '1';
        ELSIF sTicCnt = x"a00000" and signA = '1' THEN
            signA <= '0';
            signB <= '1';
        ELSIF sTicCnt = x"b00000" and signB = '1' THEN
            signB <= '0';
        END IF;
      END IF;
    END PROCESS;

  PROCESS (CLK, RESET) IS
  BEGIN
    IF RESET = '1' THEN                 -- asynchronous reset (active high)
      START    <= '0';
      MODE     <= (others => '0');
      SL_WR    <= '0';
      SL_ADDR  <= (others => '0');
      WR_ADDR  <= (others => '0');
      WR_DATA0 <= (others => '0');
      WR_DATA1 <= (others => '0');
      DATA0    <= (others => '0');
      DATA1    <= (others => '0');
      DATA2    <= (others => '0');
      DATA3    <= (others => '0');
      DATA4    <= (others => '0');
      DATA5    <= (others => '0');
    ELSIF rising_edge(CLK) THEN
      -- default
      START    <= '0';

      IF sTicCnt = x"000000" and COMMAND0(34) = '0' THEN
        START    <= '1';
        MODE     <= COMMAND0(33 downto 32);
        SL_WR    <= COMMAND0(31);
        SL_ADDR  <= COMMAND0(30 downto 24);
        WR_ADDR  <= COMMAND0(23 downto 16);
        WR_DATA0 <= COMMAND0(15 downto 8);
        WR_DATA1 <= COMMAND0(7  downto 0);
      ELSIF sTicCnt = x"100000" and COMMAND0(34) = '0' THEN
        DATA0    <= RD_DATA0 & RD_DATA1;
      ELSIF sTicCnt = x"200000" and COMMAND1(34) = '0' THEN
        START    <= '1';
        MODE     <= COMMAND1(33 downto 32);
        SL_WR    <= COMMAND1(31);
        SL_ADDR  <= COMMAND1(30 downto 24);
        WR_ADDR  <= COMMAND1(23 downto 16);
        WR_DATA0 <= COMMAND1(15 downto 8);
        WR_DATA1 <= COMMAND1(7  downto 0);
      ELSIF sTicCnt = x"300000" and COMMAND1(34) = '0' THEN
        DATA1    <= RD_DATA0 & RD_DATA1;
      ELSIF sTicCnt = x"400000" and COMMAND2(34) = '0' THEN
        START    <= '1';
        MODE     <= COMMAND2(33 downto 32);
        SL_WR    <= COMMAND2(31);
        SL_ADDR  <= COMMAND2(30 downto 24);
        WR_ADDR  <= COMMAND2(23 downto 16);
        WR_DATA0 <= COMMAND2(15 downto 8);
        WR_DATA1 <= COMMAND2(7  downto 0);
      ELSIF sTicCnt = x"500000" and COMMAND2(34) = '0' THEN
        DATA2    <= RD_DATA0 & RD_DATA1;
      ELSIF sTicCnt = x"600000" and COMMAND3(34) = '0' THEN
        START    <= '1';
        MODE     <= COMMAND3(33 downto 32);
        SL_WR    <= COMMAND3(31);
        SL_ADDR  <= COMMAND3(30 downto 24);
        WR_ADDR  <= COMMAND3(23 downto 16);
        WR_DATA0 <= COMMAND3(15 downto 8);
        WR_DATA1 <= COMMAND3(7  downto 0);
      ELSIF sTicCnt = x"700000" and COMMAND3(34) = '0' THEN
        DATA3    <= RD_DATA0 & RD_DATA1;
      ELSIF sTicCnt = x"800000" and COMMAND4(34) = '0' THEN
        START    <= '1';
        MODE     <= COMMAND4(33 downto 32);
        SL_WR    <= COMMAND4(31);
        SL_ADDR  <= COMMAND4(30 downto 24);
        WR_ADDR  <= COMMAND4(23 downto 16);
        WR_DATA0 <= COMMAND4(15 downto 8);
        WR_DATA1 <= COMMAND4(7  downto 0);
      ELSIF sTicCnt = x"900000" and COMMAND4(34) = '0' THEN
        DATA4    <= RD_DATA0 & RD_DATA1;
--      ELSIF sTicCnt = x"a0000" and COMMAND5(34) = '0' THEN
      ELSIF sTicCnt = x"a00000" and signA = '1' THEN
        START    <= '1';
        MODE     <= COMMAND5(33 downto 32);
        SL_WR    <= COMMAND5(31);
        SL_ADDR  <= COMMAND5(30 downto 24);
        WR_ADDR  <= COMMAND5(23 downto 16);
        WR_DATA0 <= COMMAND5(15 downto 8);
        WR_DATA1 <= COMMAND5(7  downto 0);
--      ELSIF sTicCnt = x"b0000" and COMMAND5(34) = '0' THEN
      ELSIF sTicCnt = x"b00000" and signB = '1' THEN
        DATA5    <= RD_DATA0 & RD_DATA1;
      ELSE
        START    <= '0';
      END IF;

    END IF;
  END PROCESS;

END arch;
