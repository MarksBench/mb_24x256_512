# mb_24x256_512
Very simple MicroPython module/driver for Microchip 24x256 and 24x512 I2C EEPROM devices. Works with RP2040 (tested with Raspberry Pi Pico) but should also work with other boards that have hardware or software I2C and are capable of running MicroPython v1.15.

This module is intended to make using the 24x256/512 as simple as possible. It has the following functions:

- Write a value (range 0-255) to an EEPROM address (range 0-32767(24x256) or 0-65535(24x512)).
- Read a value from an EEPROM address, values are returned as an integer (range 0-255)
- And that's it.

Author: mark@marksbench.com

Version: 0.1, 2021-06-04

**NOTE(1): There is no guarantee that this software will work in the way you expect (or at all). Use at your own risk.

**NOTE(2): This driver is intended to be as simple as possible to use. *As a result it does byte writes instead of page writes. That means that each time you write a byte, the entire page is re-written in the EEPROM. This can/will wear the EEPROM significantly faster than doing a page write.* Other options are sequential writes or page writes but they are not part of this driver.

**NOTE(3): Thanks to KJRC on the Adafruit forums for testing and providing feedback and ideas

Prerequisites:
- RP2040 silicon (tested with Raspberry Pi Pico), should work with other MCUs with HW or SW I2C
- MicroPython v1.15
- 24x256/512 connected to hardware I2C pins, should also work with SW I2C


Usage:
- Set up I2C (software or hardware)
- Create constructor:
  thisMemoryChipDeviceName = mb_24x256_512.mb_24x256_512(i2c, i2c_address, EEPROM_DEVICE)
    where i2c_address is a base-10 value that corresponds to the 7-bit i2c address of the EEPROM, and
    where EEPROM_DEVICE is either "24x256" or "24x512"
- To write a single byte to an address:
  thisMemoryChipDeviceName.write_byte(address, value)
- To read a single byte from an address:
  thisMemoryChipDeviceName.read_byte(address), value is returned as an int of range 0-255.

For more information, consult the Raspberry Pi Pico Micropython SDK documentation at:
  https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf
  
and the MicroPython documentation at:
  https://micropython.org

and the Microchip 24x256/512 datasheets at:
  https://www.microchip.com
