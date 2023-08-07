#!/usr/bin/env python
"""GPIO_debug.py: Sends GPIO signals to test wiring.
User will enter a number into a prompt and the Pi will output the number in binary.
"""

__version__ = "0.1.0"

__author__ = "Matthew DiMaggio"
__date__ = "13 June 2023"

import time
import random

import RPi.GPIO as GPIO


def intTobinary(int):
	if  abs(int) > 2047:
		binary = f'{0:012b}'
	else:
		binary = f'{abs(int):012b}'

	binarylst = []
	for i in range(len(binary)):
		binarylst.append(binary[i])

	if int < 0:
		binarylst[0] = 1
	else:
		binarylst[0] = 0

	return binarylst


def get_time():
	return time.localtime().tm_sec


def StopCallback():
	print("Callback")
	setBin([1,0,1,0,1,0,1,0,1,0,1,0])
	print("Lights On")
	print("Waiting 3")
	time.sleep(3)
	resetBin()
	print("Lights Off")
	print("Cleanup")
	GPIO.cleanup()
	print("Quit")
	quit()

def resetBin():
	GPIO.output(Bi1, 0) # Blue
	GPIO.output(Bi2, 0) # Blue
	GPIO.output(Bi3, 0) # Blue
	GPIO.output(Bi4, 0) # Blue
	GPIO.output(Bi5, 0) # Yellow
	GPIO.output(Bi6, 0) # Yellow
	GPIO.output(Bi7, 0) # Yellow
	GPIO.output(Bi8, 0) # Yellow
	GPIO.output(Bi9, 0) # Green
	GPIO.output(Bi10, 0) # Green
	GPIO.output(Bi11, 0) # Green
	GPIO.output(BiS, 0) # Green

def setBin(binary):
	GPIO.output(Bi1, int(binary[-1]))
	GPIO.output(Bi2, int(binary[-2]))
	GPIO.output(Bi3, int(binary[-3]))
	GPIO.output(Bi4, int(binary[-4]))
	GPIO.output(Bi5, int(binary[-5]))
	GPIO.output(Bi6, int(binary[-6]))
	GPIO.output(Bi7, int(binary[-7]))
	GPIO.output(Bi8, int(binary[-8]))
	GPIO.output(Bi9, int(binary[-9]))
	GPIO.output(Bi10, int(binary[-10]))
	GPIO.output(Bi11, int(binary[-11]))
	GPIO.output(BiS, int(binary[-12]))

# Initialize
GPIO.cleanup()


# Establish Misc Variables
class Count:
	num = -2047


# Establish Inputs
StopExec = 26 # White
Robr = 19 # White
Robst = 13 # White

# Establish Outputs
Bi1 = 21 # Blue
Bi2 = 20 # Blue
Bi3 = 16 # Blue
Bi4 = 12 # Blue
Bi5 = 1 # Yellow
Bi6 = 7 # Yellow
Bi7 = 8 # Yellow
Bi8 = 25 # Yellow
Bi9 = 24 # Green
Bi10 = 23 # Green
Bi11 = 18 # Green
BiS = 4 # Green
CamStep = 17 # Red

# Disable Pin Warnings
GPIO.setwarnings(False)

# Setup PinMode to BCM
GPIO.setmode(GPIO.BCM)

# Setup Output Pins
GPIO.setup(Bi1, GPIO.OUT)
GPIO.setup(Bi2, GPIO.OUT)
GPIO.setup(Bi3, GPIO.OUT)
GPIO.setup(Bi4, GPIO.OUT)
GPIO.setup(Bi5, GPIO.OUT)
GPIO.setup(Bi6, GPIO.OUT)
GPIO.setup(Bi7, GPIO.OUT)
GPIO.setup(Bi8, GPIO.OUT)
GPIO.setup(Bi9, GPIO.OUT)
GPIO.setup(Bi10, GPIO.OUT)
GPIO.setup(Bi11, GPIO.OUT)
GPIO.setup(BiS, GPIO.OUT)
GPIO.setup(CamStep, GPIO.OUT)

# Setup Input Pins
GPIO.setup(StopExec, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Robr, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Robst, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def main():
	if GPIO.input(StopExec):
		StopCallback()

	go = True

	if go: #GPIO.input(Robr):
		binary = intTobinary(int(round(float(input("Number between -2047 and 2047: ")),0)))
		#binary = intTobinary(random.randrange(-2047, 2048, 1))
		setBin(binary)
		time.sleep(.5)

		"""
		if Count.num >= 2048:
			Count.num = -2047
		else:
			Count.num += 1
		"""
	else:
		pass

if __name__ == '__main__':
	while True:
		main()
		time.sleep(0.05)

