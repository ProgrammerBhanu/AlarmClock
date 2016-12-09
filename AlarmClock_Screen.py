# encoding: utf-8
"""
AlarmClock_screen.py

Script 1 of 2 from AlarmClock Project:
Script for controlling the LCD Screen on the alarm clock, displaying time and date,
reading the set alarm time etc.

Created by Christopher Beard on 16-07-2016.
Copyright (c) 2016 notice:
This code is shared under the Creative Commons Attribution-ShareAlike
4.0 International Public License
It is also shared under the GNU GENERAL PUBLIC LICENSE Version 3
"""
from time import sleep
import Adafruit_CharLCD as LCD
import Adafruit_MCP9808.MCP9808 as MCP9808
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
#intialise LCD
lcd = LCD.Adafruit_CharLCDPlate()

#set initial background colour
lcd.set_color(1.0,0.0,1.0) # blue LCD only

#set background off intially, need GPIO Interuption# to set high
lcd.set_backlight(0)

#intialise temp sensor
sensor = MCP9808.MCP9808()
sensor.begin()

def Get_Temperature():
    """
    Get_Tepearture Function:
    Function to get the temperature in degrees C from the attached sensor

    Args: None

    Return: Temperature (as string)
    """
    try:
        temp = sensor.readTempC()
        temp = str('%.0f' % temp) # convert to string of 0 decimal places
        return temp
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Get_Temperature')
    except:
        print ('Error in Function Get_Temperature')
    finally:
        GPIO.cleanup()

def Get_ActualTime():
    ActualTimeDisplay = datetime.now().strftime('%H:%M')
    Hour = int(datetime.now().strftime('%H'))
    Min = int(datetime.now().strftime('%M'))
    Sec = int(datetime.now().strftime('%S'))
    ActualTime = {'H':Hour, 'M':Min, 'S':Sec}
    return ActualTime, ActualTimeDisplay

def Get_AlarmTime(Alarm_Number):
    pass
