"""
/***************************************************
 * s-Sense HDC2010 by itbrainpower.net python library v0.3 / 20200218
 * HDC2010 high accuracy temperature and humidity sensors are manufactured by Texas Instruments.
 *
 * This HDC2010 temperature and humidity class it's based on class developed by Brandon Fisher (see bellow). 
 * Thank you Brandon! Great job! 
 * We've ported Brandon's functions into python, add some variables, functions and functionalities.
 *
 * This library it's compatible with:
 *		s-Sense HDC2010 I2C sensor breakout [PN: SS-HDC2010#I2C, SKU: ITBP-6005], info https://itbrainpower.net/sensors/HDC2010-TEMPERATURE-HUMIDITY-I2C-sensor-breakout 
 *		s-Sense CCS811 + HDC2010 I2C sensor breakout [PN: SS-HDC2010+CCS811#I2C, SKU: ITBP-6006], info https://itbrainpower.net/sensors/CCS811-HDC2010-CO2-TVOC-TEMPERATURE-HUMIDITY-I2C-sensor-breakout
 *		all Raspberry PI, using Python 2.7
 * 
 * 
 * 
 * HDC2010 definitions are placed in hdc2010_param.py
 *
 * READ HDC2010 documentation! https://itbrainpower.net/downloadables/hdc2010.pdf
 * 
 * You are legaly entitled to use this SOFTWARE ONLY IN CONJUNCTION WITH s-Sense HDC2010 I2C sensors DEVICES USAGE. Modifications, derivates and redistribution 
 * of this software must include unmodified this COPYRIGHT NOTICE. You can redistribute this SOFTWARE and/or modify it under the terms 
 * of this COPYRIGHT NOTICE. Any other usage may be permited only after written notice of Dragos Iosub / R&D Software Solutions srl.
 * 
 * This SOFTWARE is distributed is provide "AS IS" in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
 * or FITNESS FOR A PARTICULAR PURPOSE.
 *  
 *  
 * itbrainpower.net invests significant time in design phase of our IoT products and in associated software and support resources.
 * Support us by purchasing our environmental and air quality sensors from here https://itbrainpower.net/order#s-Sense
 *
 * This library is dependent on python-smbus2
 *              https://pypi.org/project/smbus2/
 *              https://buildmedia.readthedocs.org/media/pdf/smbus2/latest/smbus2.pdf
 *
 * Dragos Iosub, Bucharest 2020.
 * https://itbrainpower.net
 */
"""

import smbus2 as smbus
from time import sleep
from hdc2010_param import *


def hdc2010ReadRegister(address):
        global bus
        contents = bus.read_i2c_block_data(HDC2010_I2C_address, address, 1)
        return contents[0]

def hdc2010ReadNRegisters(address, length):
        global bus
        contents = bus.read_i2c_block_data(HDC2010_I2C_ADDRESS, address, length)
        return contents

def hdc2010NWriteRegisters(address, data):
        global bus
        bus.write_i2c_block_data(HDC2010_I2C_address, address, data)

def hdc2010WriteRegister(address, data):
        global bus
        #print ""
        #print "register / data : %02x ==> %02x " %(address,data)

        bus.write_byte_data(0x40, address, data)

        #contents = hdc2010ReadRegister(address)
        #print "verified data : %02x " %contents
        #print ""
        #print ""

def hdc2010Reset():
        print "reset ..."
        configContents = hdc2010ReadRegister(HDC2010_CONFIG)

        configContents |= 0x80
        
        hdc2010WriteRegister(HDC2010_CONFIG, configContents)
        sleep(0.005)


"""
Bit 3 of the CONFIG register can be used to enable/disable heater
"""
def hdc2010EnableHeater():
        configContents = hdc2010ReadRegister(HDC2010_CONFIG)
        configContents = (configContents | 0x08)                        #set bit 3 to 1 to enable heater
        hdc2010WriteRegister(HDC2010_CONFIG, configContents)

"""
Bit 3 of the CONFIG register can be used to enable/disable heater
"""
def hdc2010DisableHeater():
        configContents = hdc2010ReadRegister(HDC2010_CONFIG)
        configContents = (configContents & 0xF7)                        #set bit 3 to 0 to disable heater
        hdc2010WriteRegister(HDC2010_CONFIG, configContents)


"""
Bit 2 of the CONFIG register can be used to enable/disable 
the interrupt pin
"""
def hdc2010EnableInterrupt():
        configContents = hdc2010ReadRegister(HDC2010_CONFIG)
        configContents = (configContents | 0x04)
        hdc2010WriteRegister(HDC2010_CONFIG, configContents)

"""
Bit 2 of the CONFIG register can be used to enable/disable 
the interrupt pin
"""
def hdc2010DisableInterrupt():
        configContents = hdc2010ReadRegister(HDC2010_CONFIG)
        configContents = (configContents & 0xFB)
        hdc2010WriteRegister(HDC2010_CONFIG, configContents)

"""
Bit 1 of the CONFIG register can be used to control the
the interrupt pins polarity
"""
def hdc2010SetInterruptPolarity(polarity):
        configContents = hdc2010ReadRegister(HDC2010_CONFIG)

        if(polarity == HDC2010_ACTIVE_HIGH):
                configContents = (configContents | 0x02)
        else:
                configContents = (configContents & 0xFD)
        
        hdc2010WriteRegister(HDC2010_CONFIG, configContents)

"""
Bit 0 of the CONFIG register can be used to control the
the interrupt pin's mode
"""
def hdc2010SetInterruptMode(mode):
        configContents = hdc2010ReadRegister(HDC2010_CONFIG)

        if(mode == HDC2010_COMPARATOR_MODE):
                configContents = (configContents | 0x01)
        else:
                configContents = (configContents & 0xFE)

        hdc2010WriteRegister(HDC2010_CONFIG, configContents)

def hdc2010ReadInterruptStatus():
	regContents = readReg(HDC2010_INTERRUPT_DRDY)
	return regContents

"""Clears the maximum temperature register"""
def hdc20102010ClearMaxTemp():
        hdc2010WriteRegister(HDC2010_TEMP_MAX, 0x00)

"""Clears the maximum humidity register"""
def hdc20102010ClearMaxHumidity():
        hdc2010WriteRegister(HDC2010_HUMID_MAX, 0x00)

"""Reads the maximum temperature register"""
def hdc2010ReadMaxTemp():
        regContents = hdc2010ReadRegister(HDC2010_TEMP_MAX)
        return float(regContents) * 165 / 256 - 40

"""Reads the maximum humidity register"""
def hdc2010ReadMaxHumidity():
        regContents = hdc2010ReadRegister(HDC2010_HUMID_MAX)
        return float(regContents) / 256 * 100

"""Enables the interrupt pin for comfort zone operation"""
def hdc2010EnableThresholdInterrupt():
        regContents = hdc2010ReadRegister(HDC2010_INTERRUPT_CONFIG)
        regContents = (regContents | 0x78)
        hdc2010WriteRegister(HDC2010_INTERRUPT_CONFIG, regContents)


"""Disables the interrupt pin for comfort zone operation"""
def hdc2010DisableThresholdInterrupt():
        regContents = hdc2010ReadRegister(HDC2010_INTERRUPT_CONFIG)
        regContents = (regContents & 0x87)
        hdc2010WriteRegister(HDC2010_INTERRUPT_CONFIG, regContents)

"""Enables the interrupt pin for DRDY operation"""
def hdc2010EnableDRDYInterrupt():
        regContents = hdc2010ReadRegister(HDC2010_INTERRUPT_CONFIG)
        regContents = (regContents | 0x80)
        hdc2010WriteRegister(HDC2010_INTERRUPT_CONFIG, regContents)

"""Disables the interrupt pin for DRDY operation"""
def hdc2010DisableDRDYInterrupt():
        regContents = hdc2010ReadRegister(HDC2010_INTERRUPT_CONFIG)
        regContents = (regContents & 0x7F)
        hdc2010WriteRegister(HDC2010_INTERRUPT_CONFIG, regContents)


def hdc2010SetTemperatureOffset(tempOffset):
	hdc2010WriteRegister(HDC2010_TEMP_OFFSET_ADJUST, tempOffset)


"""check sensor type ID to be 0x07D0  - return true if sensor it's online"""
def hdc2010CheckSensorType():
        byteR = hdc2010ReadRegister(HDC2010_DEVICE_ID_L)
        if (byteR != 0xD0):
                return False
        byteR = hdc2010ReadRegister(HDC2010_DEVICE_ID_H)
        if (byteR != 0x07):
                return False
        return True

"""check sensor manufacturer ID to be 0x5449  - return true if sensor it's online"""
def hdc2010SensorManufacturer():
        byteR = hdc2010ReadRegister(HDC2010_MID_L)
        if (byteR != 0x49):
                return False
        byteR = hdc2010ReadRegister(HDC2010_MID_H)
        if (byteR != 0x54):
                return False
        return True


"""
Bits 6-4  of the CONFIG register controls
the measurement rate
"""
def hdc2010SetMeasurementsMode(mode):
        print "set temp humid ..."
        configContents = hdc2010ReadRegister(HDC2010_MEASUREMENT_CONFIG)
        
        if mode == HDC2010_TEMP_AND_HUMID:
                configContents = configContents & 0xF9                          #TEMP_AND_HUMID
        elif mode == HDC2010_TEMP_ONLY:
                configContents = configContents & 0xFC                          #TEMP_ONLY
                configContents = configContents | 0x02  
        elif mode == HDC2010_HUMID_ONLY:
                configContents = configContents & 0xFD                          #HUMID_ONLY
                configContents = configContents | 0x04
        else:
                configContents = configContents & 0xF9                          #default
        
        hdc2010WriteRegister(HDC2010_MEASUREMENT_CONFIG, configContents)
	
"""
Bits 6-4  of the CONFIG register controls
the measurement rate
"""
def hdc2010SetRate(rate):
        print "set refresh rate ..."
        configContents = hdc2010ReadRegister(HDC2010_CONFIG)
        
        if rate == HDC2010_MANUAL:
                configContents = configContents & 0x8F                                  #manual
        elif rate == HDC2010_TWO_MINS:
                configContents = configContents & 0x9F                                  #at 120sec
                configContents = configContents | 0x10                                  #at 120sec
        elif rate == HDC2010_ONE_MINS:
                configContents = configContents & 0xAF                                  #at 60sec
                configContents = configContents | 0x20                                  #at 60sec
        elif rate == HDC2010_TEN_SECONDS:
                configContents = configContents & 0xBF                                  #at 10sec
                configContents = configContents | 0x30                                  #at 10sec
        elif rate == HDC2010_FIVE_SECONDS:
                configContents = configContents & 0xCF                                  #at 5sec
                configContents = configContents | 0x40                                  #at 5sec
        elif rate == HDC2010_ONE_HZ:
                configContents = configContents & 0xDF                                  #1hz
                configContents = configContents | 0x50                                  #1hz
        elif rate == HDC2010_TWO_HZ:
                configContents = configContents & 0xEF                                  #2hz
                configContents = configContents | 0x60                                  #2hz
        elif rate == HDC2010_FIVE_HZ:
                configContents = configContents | 0x70                                  #5hz
        else:
                configContents = configContents & 0x8F                                  #default
                
        hdc2010WriteRegister(HDC2010_CONFIG, configContents)

	
def hdc2010SetTempRes(resolution):
        print "set temp resolution ..."
        configContents = hdc2010ReadRegister(HDC2010_MEASUREMENT_CONFIG)

        if resolution == HDC2010_FOURTEEN_BIT:
                configContents = configContents & 0x3F                                          #14bits
        elif resolution == HDC2010_ELEVEN_BIT:
                configContents = configContents & 0x7F                                          #11bits
                configContents = configContents | 0x40                                          #11bits
        elif resolution == HDC2010_NINE_BIT:
                configContents = configContents & 0xBF                                          #9bits
                configContents = configContents | 0x80                                          #9bits
        else:
                configContents = configContents & 0x3F                                          #default

        hdc2010WriteRegister(HDC2010_MEASUREMENT_CONFIG, configContents)
	
def hdc2010SetHumidRes(resolution):
        print "set humidity resolution ..."
        configContents = hdc2010ReadRegister(HDC2010_MEASUREMENT_CONFIG)
        
        if resolution == HDC2010_FOURTEEN_BIT:
                configContents = configContents & 0xCF                                          #14bits
        elif resolution == HDC2010_ELEVEN_BIT:
                configContents = configContents & 0xDF                                          #11bits
                configContents = configContents | 0x10                                          #11bits
        elif resolution == HDC2010_NINE_BIT:
                configContents = configContents & 0xEF                                          #9bits
                configContents = configContents | 0x20                                          #9bits
        else:
                configContents = configContents & 0xCF                                          #default

        hdc2010WriteRegister(HDC2010_MEASUREMENT_CONFIG, configContents)

def hdc2010TriggerMeasurement():
        #print "trigger measurements ..."
        configContents = hdc2010ReadRegister(HDC2010_MEASUREMENT_CONFIG)

        configContents = configContents | 0x01          

        hdc2010WriteRegister(HDC2010_MEASUREMENT_CONFIG, configContents)


def hdc2010ReadTemp():
        byte0 = hdc2010ReadRegister(HDC2010_TEMP_LOW)
        byte1 = hdc2010ReadRegister(HDC2010_TEMP_HIGH)
        #print "temp read : %02x %02x" %(byte1,byte0)

        temp = byte1 << 8 | byte0

        return (float(temp) * 165 / 65536 - 40)

def hdc2010ReadHumidity():        
        byte0 = hdc2010ReadRegister(HDC2010_HUMID_LOW)
        byte1 = hdc2010ReadRegister(HDC2010_HUMID_HIGH)
        #print "humid read : %02x %02x" %(byte1,byte0)
        
        humid = byte1 << 8 | byte0
        return ((float(humid) / 65536) * 100)


# Initialize I2C (SMBus)
try:
    configContents = hdc2010ReadRegister(HDC2010_MEASUREMENT_CONFIG)
    print "I2C alredy loaded"
except:
    bus = smbus.SMBus(channel)

bus = smbus.SMBus(channel)
