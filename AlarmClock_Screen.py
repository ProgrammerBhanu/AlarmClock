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
from time import sleep, strftime
from datetime import datetime
from array import array
import pickle
import Adafruit_CharLCD as LCD
import Adafruit_MCP9808.MCP9808 as MCP9808
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN)

#intialise LCD
lcd = LCD.Adafruit_CharLCDPlate()
#set initial background colour
lcd.set_color(1.0,0.0,1.0) # blue LCD only
#set background off intially, need GPIO event to set high
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
        GPIO.cleanup()
        quit()


def Get_ActualTime():
    """
    Get_ActualTime Function:
    Function to get the actual time from the system, then seperate into
    a time for the display and a dictionary item for the time in
    individual hours, minutes and seconds

    Args: None

    Return: ActualTime,  ActualTimeDisplay
    """
    try:
        ActualTimeDisplay = datetime.now().strftime('%H:%M')
        Hour = int(datetime.now().strftime('%H'))
        Min = int(datetime.now().strftime('%M'))
        Sec = int(datetime.now().strftime('%S'))
        ActualTime = {'H':Hour, 'M':Min, 'S':Sec}
        return ActualTime, ActualTimeDisplay
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Get_ActualTime')
        GPIO.cleanup()
        quit()

def Get_Date():
    """
    Get_Date fucntion:
    Fucntion to get date from the system

    Args: None

    Return: Date
    """
    try:
        Date = datetime.now().strftime('%a %d %b')
        return Date
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Get_Date')
        GPIO.cleanup()
        quit()

def _Display_AlarmTime(Hour, Min, Alarm_Number):
    """
    _Display_AlarmTime Method:
    This is a method of Set_AlarmTime fucntion, it is responsible for displaying
    the alarm time on the LCD

    Args: Hour, Min, Alarm_Number

    Return: None
    """
    try:
        lcd.clear()
        lcd.message('Alarm ' + str(Alarm_Number) + ' Time:\n' )
        lcd.message(str(Hour))
        lcd.set_cursor(2,1)
        lcd.message(':')
        lcd.set_cursor(3,1)
        lcd.message(str(Min))
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Method _Display_AlarmTime')
        GPIO.cleanup()
        quit()

def Set_AlarmTime(Hour, Min, Sec, Alarm_Number):
    """
    Set_AlarmTime Function:
    Function to alter the set alarm time using the LCD touchbuttons changing
    hour and minute seperately

    Args: Hour, Min, Sec, Alarm_Number

    Return: Hour, Min, Sec
    """
    try:
        lcd.set_backlight(1)
        _Display_AlarmTime(Hour, Min, Alarm_Number)

        #ideally want to use for loop here but can't as won't display hour and min
        #   correctly
        Cycle = True
        while Cycle:
            lcd.set_cursor(0,1)
            lcd.blink(True) # start blinking cursor so user knows what they are changing
            if lcd.is_pressed(LCD.UP):
                Hour += 1
                _Display_AlarmTime(Hour, Min, Alarm_Number)
            elif lcd.is_pressed(LCD.DOWN):
                Hour -= 1
                lcd.clear()
                _Display_AlarmTime(Hour, Min, Alarm_Number)
            elif lcd.is_pressed(LCD.SELECT):
                Cycle = False
                sleep(0.5)

        Cycle = True
        while Cycle:
            lcd.set_cursor(3,1)
            if lcd.is_pressed(LCD.UP):
                Min += 1
                _Display_AlarmTime(Hour, Min, Alarm_Number)
            elif lcd.is_pressed(LCD.DOWN):
                Min -= 1
                _Display_AlarmTime(Hour, Min, Alarm_Number)
            elif lcd.is_pressed(LCD.SELECT):
                Cycle = False
                sleep(0.5)

        lcd.clear()
        lcd.blink(False)
        lcd.set_backlight(0)
        return Hour, Min, Sec
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Set_AlarmTime')
        GPIO.cleanup()
        quit()


def Get_AlarmTime(Hour, Min, Sec, Alarm_Number):
    """
    Get_AlarmTime function:
    Function to get the individual times of the alarm in Hous, mins and secs
    and convert to dictionary item

    Args: Hour, Min, Sec, Alarm_Number

    Return: AlarmTime
    """
    try:
        #convert to dictionary
        AlarmTime = {'H':Hour, 'M':Min, 'S':Sec}
        return AlarmTime
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Get_AlarmTime')
        GPIO.cleanup()
        quit()


def F_BackLightON(channel):
    """
    F_BackLightON function:
    Function to turn LCD backlight on for a duration of time

    Args: None

    Return: None
    """
    try:
        lcd.set_backlight(1)
        sleep(8)
        lcd.set_backlight(0)
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function F_BackLightON')
        GPIO.cleanup()
        quit()

#trigger event for backlight
GPIO.add_event_detect(25, GPIO.RISING, callback=F_BackLightON, bouncetime=300)

def F_AlarmOnOff(AlarmActive, Alarm_Number):
    """
    AlarmActive function:
    Function to enable and disable alarm when button is pressed as well as
    display status on screen

    Args: AlarmActive

    Return: AlarmActive
    """
    try:
        if AlarmActive:
            AlarmActive = False
            lcd.set_backlight(1)
            lcd.clear()
            lcd.message('Alarm ' + str(Alarm_Number) + ' Disabled')
            sleep(2)
            lcd.clear()
            lcd.set_backlight(0)
            return AlarmActive
        else:
            AlarmActive = True
            lcd.set_backlight(1)
            lcd.clear()
            lcd.message('Alarm ' + str(Alarm_Number) + ' Enabled')
            sleep(2)
            lcd.clear()
            lcd.set_backlight(0)
            return AlarmActive
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function F_AlarmOnOff')
        GPIO.cleanup()
        quit()

def main():
    """
    Main Function:
    Runs continously calling appropriate functions to set screens depending on buttons pressed
    """
    try:
        #Intialise variables
        AlarmActive = array('l',[False, False])
        #alarm times
        Hour = array('l',[1,1])
        Min = array('l',[1,1])
        Sec = array('l',[1,1])

        while True:
            if lcd.is_pressed(LCD.UP):
                #trigger event to enable/disable alarm 1
                AlarmActive[0] = F_AlarmOnOff(AlarmActive[0], 1)
            elif lcd.is_pressed(LCD.DOWN):
                #trigger event to enable/disable alarm 2
                AlarmActive[1] = F_AlarmOnOff(AlarmActive[1], 2)
            elif lcd.is_pressed(LCD.LEFT):
                #trigger event to set alarm 1 time
                Hour[0], Min[0], Sec[0] = Set_AlarmTime(Hour[0], Min[0], Sec[0], 1)
            elif lcd.is_pressed(LCD.RIGHT):
                #trigger event to set alarm 2 time
                Hour[1], Min[1], Sec[1] = Set_AlarmTime(Hour[1], Min[1], Sec[1], 2)
            else:
                #Main Screen
                ActualTime, ActualTimeDisplay = Get_ActualTime()
                date = Get_Date()
                temp = Get_Temperature()
                lcd.set_cursor(0,0)
                lcd.message(ActualTimeDisplay)
                lcd.set_cursor(12,0)
                lcd.message(temp + chr(223) + 'C') #chr(223) is degree sign
                lcd.set_cursor(3,1)
                lcd.message(date)
                sleep(0.5) #preserve processor

                #trigger event for backlight
                # if GPIO.input(25):
                #     F_BackLightON()

                #setup pickles here to pass data to AlarmClock_Alarm.py
                with open('Alarm1Active.pickle', 'wb') as f:
                    # Pickle the 'data' using the highest protocol available.
                    pickle.dump(AlarmActive[0], f, pickle.HIGHEST_PROTOCOL)
                with open('Alarm2Active.pickle', 'wb') as f2:
                    # Pickle the 'data' using the highest protocol available.
                    pickle.dump(AlarmActive[1], f2, pickle.HIGHEST_PROTOCOL)
                with open('AlarmTime1.pickle', 'wb') as f3:
                    AlarmTime1 = Get_AlarmTime(Hour[0], Min[0], Sec[0], 1)
                    # Pickle the 'data' using the highest protocol available.
                    pickle.dump(AlarmTime1, f3, pickle.HIGHEST_PROTOCOL)
                with open('AlarmTime2.pickle', 'wb') as f4:
                    AlarmTime2 = Get_AlarmTime(Hour[1], Min[1], Sec[1], 2)
                    # Pickle the 'data' using the highest protocol available.
                    pickle.dump(AlarmTime2, f4, pickle.HIGHEST_PROTOCOL)

    except KeyboardInterrupt:
        print('KeyboardInterrupt in Main')
        GPIO.cleanup()
        quit()

if __name__ == '__main__':
    main()
