-- $Id: i2c_wr_bytes.vhd  Dong Wang $
-------------------------------------------------------------------------------
-- Title      : you can control how many bytes read or write via i2c bus
-- Project    : HFT PXL
-------------------------------------------------------------------------------
-- File       : i2c_wr_bytes.vhd
-- Author     : Dong Wang
-- Company    : Central China Normal University
-- Created    : 2016-10-9
-- Last update:
-- Platform   : Linux Vivado 2015.4.2
-- Target     : KC705
-- Standard   : VHDL'93/02
-------------------------------------------------------------------------------
-- Description: When receive a pulse from pulse_reg, you can control how many
-- bytes read or write via i2c bus, the limit is 3 bytes.
-------------------------------------------------------------------------------
-- Copyright (c) 2016
-------------------------------------------------------------------------------
-- Revisions  :
-- Date        Version  Author        Description
-- 2016-10-9  1.0      Dong      Created
-------------------------------------------------------------------------------
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE ieee.std_logic_unsigned.all;

ENTITY i2c_wr_bytes IS
  PORT (
    CLK      : IN  std_logic;           --  system clock 50Mhz
    RESET    : IN  std_logic;           --  active high reset
    START    : IN  std_logic;           -- the rising edge trigger a start, generate by config_reg
    MODE     : IN  std_logic_vector(1 DOWNTO 0);          -- '0' is 1 bytes read or write, '1' is 2 bytes read or write,
                                                          -- '2' is 3 bytes write only , don't set to '3'
    SL_WR    : IN  std_logic;           -- '0' is write, '1' is read
    SL_ADDR  : IN  std_logic_vector(6 DOWNTO 0);  -- slave addr
    WR_ADDR  : IN  std_logic_vector(7 DOWNTO 0);  -- chip internal addr for read and write
    WR_DATA0 : IN  std_logic_vector(7 DOWNTO 0);  -- first byte data for write
    WR_DATA1 : IN  std_logic_vector(7 DOWNTO 0);  -- second byte data for write
    RD_DATA0 : buffer std_logic_vector(7 DOWNTO 0);  -- first byte readout
    RD_DATA1 : buffer std_logic_vector(7 DOWNTO 0);  -- second byte readout
    BUSY     : OUT std_logic;           -- indicates transaction in progress
    SDA_in   : IN  std_logic;           -- serial data input of i2c bus
    SDA_out  : OUT std_logic;           -- serial data output of i2c bus
    SDA_T    : OUT std_logic;           -- serial data direction of i2c bus
    SCL      : OUT std_logic            -- serial clock output of i2c bus
    );
END i2c_wr_bytes;

ARCHITECTURE arch OF i2c_wr_bytes IS
  COMPONENT i2c_master IS
    GENERIC (
      INPUT_CLK_FREQENCY : integer;
      BUS_CLK_FREQUENCY  : integer
      );
    PORT (
      CLK       : IN  std_logic;
      RESET     : IN  std_logic;
      ENA       : IN  std_logic;
      ADDR      : IN  std_logic_vector(6 DOWNTO 0);
      RW        : IN  std_logic;
      DATA_WR   : IN  std_logic_vector(7 DOWNTO 0);
      BUSY      : OUT std_logic;
      DATA_RD   : OUT std_logic_vector(7 DOWNTO 0);
      ACK_ERROR : OUT std_logic;
      SDA_in    : IN  std_logic;
      SDA_out   : OUT std_logic;
      SDA_T     : OUT std_logic;
      SCL       : OUT std_logic
      );
  END COMPONENT i2c_master;

  SIGNAL sI2C_enable    : std_logic;
  SIGNAL sI2C_data_wr   : std_logic_vector(7 DOWNTO 0);
  SIGNAL sI2C_data_rd   : std_logic_vector(7 DOWNTO 0);
  SIGNAL sI2C_busy      : std_logic;
  SIGNAL sBusyCnt       : std_logic_vector(2 DOWNTO 0);
  SIGNAL sBusy_d1       : std_logic;
  SIGNAL sBusy_d2       : std_logic;

  TYPE machine_type IS (StWaitStart,
                        StWr1,
                        StWr2,
                        StWr3,
                        StRd1,
                        StRd2
                        );              -- needed states
  SIGNAL state : machine_type;          -- state machine

BEGIN
  i2c_master_inst : i2c_master
    GENERIC MAP (
      INPUT_CLK_FREQENCY => 60_000_000,
      BUS_CLK_FREQUENCY  => 60_000
     --BUS_CLK_FREQUENCY         => 50_000
      )
    PORT MAP (
      CLK       => CLK,
      RESET     => RESET,
      ENA       => sI2C_enable,
      ADDR      => SL_ADDR,
      RW        => SL_WR,
      DATA_WR   => sI2C_data_wr,
      BUSY      => sI2C_busy,
      DATA_RD   => sI2C_data_rd,
      ACK_ERROR => OPEN,
      SDA_in    => SDA_in,
      SDA_out   => SDA_out,
      SDA_T     => SDA_T,
      SCL       => SCL
      );

  --busy counter
  busy_d : PROCESS (CLK) IS
  BEGIN
    IF rising_edge(CLK) THEN
      sBusy_d1 <= sI2C_busy;
      sBusy_d2 <= sBusy_d1;
    END IF;
  END PROCESS busy_d;

  busy_counter : PROCESS (CLK, RESET) IS
  BEGIN
    IF RESET = '1' THEN                 -- asynchronous reset (active high)
      sBusyCnt     <= "000";
    ELSIF rising_edge(CLK) THEN
      IF state = StWaitStart THEN
        sBusyCnt     <= "000";
      ELSIF sBusy_d2 = '0' and sBusy_d1 = '1' THEN
        sBusyCnt <= sBusyCnt + '1';
      ELSE
        sBusyCnt <= sBusyCnt;
      END IF;
    END IF;
  END PROCESS busy_counter;


  state_machine : PROCESS (CLK, RESET) IS
  BEGIN
    IF RESET = '1' THEN                 -- asynchronous reset (active high)
      sI2C_enable  <= '0';
      sI2C_data_wr <= (OTHERS => '0');
      BUSY         <= '0';
      RD_DATA0     <= (OTHERS => '0');
      RD_DATA1     <= (OTHERS => '0');
      state        <= StWaitStart;

    ELSIF rising_edge(CLK) THEN         -- rising clock edge
      CASE state IS
--      //// Wait for signal to start I2C transaction
        WHEN StWaitStart =>
          sI2C_enable  <= '0';
          sI2C_data_wr <= (OTHERS => '0');
          BUSY         <= '0';
          RD_DATA0     <= RD_DATA0;
          RD_DATA1     <= RD_DATA1;
          IF START = '1' THEN
            IF SL_WR = '0' THEN    -- write
              IF MODE = "00" THEN    -- 1 bytes write
                state <= StWr1;
              ELSIF MODE = "01" THEN -- 2 bytes write
                state <= StWr2;
              ELSIF MODE = "10" THEN -- 3 bytes write
                state <= StWr3;
              ELSE
                state <= StWaitStart;
              END IF;
            ELSE
              IF MODE = "00" THEN    -- 1 bytes read
                state <= StRd1;
              ELSIF MODE = "01" THEN -- 2 bytes read
                state <= StRd2;
              ELSE
                state <= StWaitStart;
              END IF;
            END IF;
          ELSE
            state <= StWaitStart;
          END IF;

        -- 1 bytes write
        WHEN StWr1 =>
          BUSY         <= '1';
          RD_DATA0     <= RD_DATA0;
          RD_DATA1     <= RD_DATA1;
          CASE sBusyCnt IS
            WHEN "000" =>
              sI2C_enable  <= '1';
              sI2C_data_wr <= WR_ADDR;
              state <= StWr1;
            WHEN "001" =>
              sI2C_enable  <= '0';
              sI2C_data_wr <= WR_ADDR;
              IF sI2C_busy = '0' THEN
                state <= StWaitStart;
              ELSE
                state <= StWr1;
              END IF;
            WHEN OTHERS =>
              sI2C_enable  <= '0';
              sI2C_data_wr <= (OTHERS => '0');
              state <= StWaitStart;
          END CASE;

        -- 2 bytes write
        WHEN StWr2 =>
          BUSY         <= '1';
          RD_DATA0     <= RD_DATA0;
          RD_DATA1     <= RD_DATA1;
          CASE sBusyCnt IS
            WHEN "000" =>
              sI2C_enable  <= '1';
              sI2C_data_wr <= WR_ADDR;
              state <= StWr2;
            WHEN "001" =>
              sI2C_enable  <= '1';
              sI2C_data_wr <= WR_DATA0;
              state <= StWr2;
            WHEN "010" =>
              sI2C_enable  <= '0';
              sI2C_data_wr <= WR_DATA0;
              IF sI2C_busy = '0' THEN
                state <= StWaitStart;
              ELSE
                state <= StWr2;
              END IF;
            WHEN OTHERS =>
              sI2C_enable  <= '0';
              sI2C_data_wr <= (OTHERS => '0');
              state <= StWaitStart;
          END CASE;

        -- 3 bytes write
        WHEN StWr3 =>
          BUSY         <= '1';
          RD_DATA0     <= RD_DATA0;
          RD_DATA1     <= RD_DATA1;
          CASE sBusyCnt IS
            WHEN "000" =>
              sI2C_enable  <= '1';
              sI2C_data_wr <= WR_ADDR;
              state <= StWr3;
            WHEN "001" =>
              sI2C_enable  <= '1';
              sI2C_data_wr <= WR_DATA0;
              state <= StWr3;
            WHEN "010" =>
              sI2C_enable  <= '1';
              sI2C_data_wr <= WR_DATA1;
              state <= StWr3;
            WHEN "011" =>
              sI2C_enable  <= '0';
              sI2C_data_wr <= WR_DATA1;
              IF sI2C_busy = '0' THEN
                state <= StWaitStart;
              ELSE
                state <= StWr3;
              END IF;
            WHEN OTHERS =>
              sI2C_enable  <= '0';
              sI2C_data_wr <= (OTHERS => '0');
              state <= StWaitStart;
          END CASE;

        -- 1 bytes read
        WHEN StRd1 =>
          BUSY         <= '1';
          RD_DATA1     <= RD_DATA1;
          sI2C_data_wr <= (OTHERS => '0');
          CASE sBusyCnt IS
            WHEN "000" =>
              sI2C_enable  <= '1';
              RD_DATA0     <= RD_DATA0;
              state <= StRd1;
            WHEN "001" =>
              sI2C_enable  <= '0';
              IF sI2C_busy = '0' THEN
                state    <= StWaitStart;
                RD_DATA0 <= sI2C_data_rd;
              ELSE
                state <= StRd1;
                RD_DATA0     <= RD_DATA0;
              END IF;
            WHEN OTHERS =>
                sI2C_enable  <= '0';
                RD_DATA0     <= RD_DATA0;
                state        <= StWaitStart;
          END CASE;


        -- 2 bytes read
        WHEN StRd2 =>
          BUSY         <= '1';
          sI2C_data_wr <= (OTHERS => '0');
          CASE sBusyCnt IS
            WHEN "000" =>
              sI2C_enable  <= '1';
              RD_DATA0     <= RD_DATA0;
              RD_DATA1     <= RD_DATA1;
              state <= StRd2;
            WHEN "001" =>
              sI2C_enable  <= '1';
              IF sI2C_busy = '0' THEN
                state    <= StRd2;
                RD_DATA0 <= sI2C_data_rd;
                RD_DATA1 <= RD_DATA1;
              ELSE
                state <= StRd2;
                RD_DATA0 <= RD_DATA0;
                RD_DATA1 <= RD_DATA1;
              END IF;
            WHEN "010" =>
              sI2C_enable  <= '0';
              IF sI2C_busy = '0' THEN
                state    <= StWaitStart;
                RD_DATA0 <= RD_DATA0;
                RD_DATA1 <= sI2C_data_rd;
              ELSE
                state <= StRd2;
                RD_DATA0 <= RD_DATA0;
                RD_DATA1 <= RD_DATA1;
              END IF;
            WHEN OTHERS =>
              sI2C_enable  <= '0';
              RD_DATA0     <= RD_DATA0;
              RD_DATA1     <= RD_DATA1;
              state        <= StWaitStart;
          END CASE;

--      //// shouldn't happen
        WHEN OTHERS =>
          sI2C_enable  <= '0';
          sI2C_data_wr <= (OTHERS => '0');
          BUSY         <= '0';
          RD_DATA0     <= (OTHERS => '0');
          RD_DATA1     <= (OTHERS => '0');
          state        <= StWaitStart;

      END CASE;
    END IF;
  END PROCESS state_machine;

END arch;
