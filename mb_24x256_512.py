'''
mb_24x256_512.py

Very Simple MicroPython module/driver for Microchip 24x256 and 24x512 I2C EEPROM

Author: mark@marksbench.com

Version: 0.1, 2021-06-04

**NOTE(1): There is no guarantee that this software will work in the way you expect (or at all).
**Use at your own risk.

**NOTE(2): This driver is intended to be as simple as possible to use. As a result it
**does byte writes instead of page writes. That means that each time you write a byte,
**the entire page is re-written in the EEPROM. This can/will wear the EEPROM significantly
**faster than doing a page write. Other options are sequential writes or saving data in RAM
**and writing them 128 bytes at a time but they are not part of this driver.

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

'''

from machine import Pin, I2C
import utime

class mb_24x256_512:
    """Driver for Microchip 24x256/512 EEPROM devices"""

    def __init__(self, i2c, i2c_address, EEPROM_device):
        # Init with the I2C setting
        self.i2c = i2c
        self.i2c_address = i2c_address[0]

        if(EEPROM_device == "24x256"):
            self._MAX_ADDRESS = 32767
        elif(EEPROM_device == "24x512"):
            self._MAX_ADDRESS = 65535
        else:
            raise ValueError("Please choose a device from the list")

            return()

    # Done init, ready to go

    def write_byte(self, address, data):
        if((address > self._MAX_ADDRESS) or (address < 0)):
            raise ValueError("Address is outside of device address range")
            return()

        if((data > 255) or (data < 0)):
            raise ValueError("You can only pass an 8-bit data value 0-255 to this function")
            return()

        self.i2c.writeto_mem(self.i2c_address, address, bytes([data]), addrsize=16)
        utime.sleep_ms(10) # EEPROM needs time to write and will not respond if not ready


    def read_byte(self, address):
        if((address > self._MAX_ADDRESS) or (address < 0)):
            raise ValueError("Address is outside of device address range")
            return()

        self.value_read = bytearray(1)
        self.value_read = self.i2c.readfrom_mem(self.i2c_address, address, 1, addrsize=16)
        self.value_read = int.from_bytes(self.value_read, "big")
        return(self.value_read)
