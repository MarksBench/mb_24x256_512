"""
mb_24x256_512_example.py

Example MicroPython script for Microchip 24x256 and 24x512 I2C EEPROM driver.

Tested with Raspberry Pi Pico (RP2040), should work with other MP-capable microcontrollers
with hardware or software I2C.

Author: mark@marksbench.com

Version: 0.1, 2021-06-04

**NOTE(1): There is no guarantee that this software will work in the way you expect (or at all).
**Use at your own risk.

**NOTE(2): This driver is intended to be as simple as possible to use. AS A RESULT IT
**DOES BYTE WRITES INSTEAD OF PAGE WRITES. That means that each time you write a byte,
**the entire page is re-written in the EEPROM. This can/will wear the EEPROM significantly
**faster than doing a page write.

**NOTE(3): Thanks to KJRC on the Adafruit forums for testing and providing ideas and feedback!


To use:
- Upload the mb_24x256_512_CP.py file to location on your board where you normally store libraries.
- Suggested connection for testing with Pi Pico (check your device for proper pinout):

24x256/512  |   Pi Pico
1 A0        |   Vss (38)
2 A1        |   Vss (38)
3 A2        |   Vss (38)
4 Vss       |   Vss (38)
5 SDA       |   GP0 (1)
6 SCL       |   GP1 (2)
7 WP        |   Vss (38)
8 Vcc       |   Vcc (36)

- Let the driver use the I2C address found by i2c.scan() or set i2c_address yourself.
- Uncomment the appropriate EEPROM_DEVICE line for the device you're using
- To write a value: memory.write_byte(address, value)
- To read a value: value = memory.read_byte(address)
- You should get an error if the address or value is out of range.

"""

from machine import Pin, I2C
import utime
import mb_24x256_512


# Set up I2C (using SCL=GP1 and SDA=GP0 on Raspberry Pi Pico (RP2040))
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)


i2c_address = i2c.scan()
print(i2c_address)

#######################################################################################
# If you know the 7-bit address of the device then you don't need to do a scan and can
# uncomment the following line and set it manually (don't forget to tie the 24x Ax pins
# to either Vcc or Vss!):
#i2c_address = 7_bit_address_of_your_device

#######################################################################################
# Now, uncomment which of the following two lines matches your EEPROM. Choose only one.
EEPROM_DEVICE = "24x256"
#EEPROM_DEVICE = "24x512"


#######################################################################################
# Now that I2C is set up, the EEPROM device address is set (probably 80), and you've
# uncommented out only the EEPROM_DEVICE line that matches your EEPROM, we should be
# good to go!
memory = mb_24x256_512.mb_24x256_512(i2c, i2c_address, EEPROM_DEVICE)


# Write an int of value 115 to address 12345
memory.write_byte(12345, 115)

# Now read it back and print it
read_value = memory.read_byte(12345)

print(read_value)

# That's all there is to it