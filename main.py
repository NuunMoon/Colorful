from PIL import Image
from PIL import ImageGrab
from numpy import asarray 
from numpy import floor
import numpy.random
import serial
import time
from screenshot import screenshot_to_rgb
import keyboard
import random
import sys

def write(x):
    arduino.write(bytes(x, 'utf-8'))
    return

def read():
    data_recieved = arduino.readline()
    data_recieved=data_recieved.decode('utf-8')
    return data_recieved

def screenshot_to_rgb():
    screenshot = ImageGrab.grab()  # Take the screenshot
    #screenshot=screenshot.resize(size=(352,240), resample = None)
    imgdata = asarray(screenshot)
    return imgdata

def estabilish_handshake(ser):
    start = time.time()
    ser.timeout=0.2
    ser.flush()
    print("beginning handshake")
    while True:
        magic = random.randint(0,10000)
        magic_str = f"H{magic}E"
        ser.write(bytes(magic_str, 'utf-8'))
        result = 'H'+ser.readall().decode('utf-8').split('H')[-1]
        if result == magic_str: break
        elif keyboard.is_pressed("q"):
            print("q pressed, ending handshake")
            sys.exit(0)
    end = time.time()
    print(f"{end - start} seconds elapsed to estabilish handshake")

arduino = serial.Serial('COM3', 9600, timeout=5)
sample_count=5000

estabilish_handshake(arduino)
arduino.timeout=5

print("begin")
while True:
    imgdata = screenshot_to_rgb()
    average=[0,0,0]
    for i in range(0,sample_count):
        r_row=random.randint(0,imgdata.shape[0]-1)
        r_col=random.randint(0,imgdata.shape[1]-1)
        r_pixel=imgdata[r_row][r_col]
        average +=r_pixel

    average= floor(average/sample_count)

    data_to_transmit = f"r{int(average[0])}g{int(average[1])}b{int(average[2])}E"

    write(data_to_transmit)
    print(data_to_transmit)
    
    print(arduino.readline())
    if keyboard.is_pressed("q"):
        print("q pressed, ending loop")
        break

arduino.close()