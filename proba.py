
# Import the necessary libraries
from math import floor
from PIL import Image
from numpy import asarray 
from numpy import floor
import serial
import time

 

def write(x):
    arduino.write(bytes(x, 'utf-8'))
    return 
def read():
    data_recieved = arduino.readline()
    data_recieved=data_recieved.decode('utf-8')
    return data_recieved

arduino = serial.Serial('COM3', 9600)
time.sleep(2) #wait for the arduino serial to set up communication


img = Image.open('cyberpunk.png')
imgdata = asarray(img)
average=[0,0,0,0]

for i in range(imgdata.shape[0]):
    for j in range(imgdata.shape[1]):
            average+=imgdata[i][j]

average= floor(average/(imgdata.shape[0]*imgdata.shape[1]))

data_to_transmit = f"r{int(average[0])}g{int(average[1])}b{int(average[2])}"

write(data_to_transmit)
print(data_to_transmit)


arduino.close()