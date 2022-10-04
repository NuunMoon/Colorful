#!/usr/bin/env python3
"""Control the arduino project over serial"""

import random
import sys
import time
from PIL import ImageGrab  # type: ignore
from numpy.typing import NDArray
import numpy as np
from serial import Serial  # type: ignore
import serial  # type: ignore
import keyboard  # type: ignore


def write(message: str, serial_port: Serial) -> None:
    """Writes a string to the serial port"""
    serial_port.write(bytes(message, "utf-8"))
    return


def screenshot_to_rgb() -> NDArray:
    """Takes an images and returns a numpy array of the rgb values"""
    screenshot = ImageGrab.grab()  # Take the screenshot
    return np.asarray(screenshot)


def estabilish_handshake(ser):
    """Estabilish a handshake with the arduino"""
    start = time.time()
    ser.timeout = 0.2
    ser.flush()
    print("beginning handshake")
    while True:
        magic = random.randint(0, 10000)
        magic_str = f"H{magic}E"
        ser.write(bytes(magic_str, "utf-8"))
        result = "H" + ser.readall().decode("utf-8").split("H")[-1]
        if result == magic_str:
            break
        elif keyboard.is_pressed("q"):
            print("q pressed, ending handshake")
            sys.exit(0)
    end = time.time()
    print(f"{end - start} seconds elapsed to estabilish handshake")


def calculate_average_color(rgb_array: NDArray, sample_count: int) -> NDArray:
    """Calculates the average color of an image"""
    average_color = np.asarray([0, 0, 0])
    for _ in range(0, sample_count):
        r_row = random.randint(0, rgb_array.shape[0] - 1)
        r_col = random.randint(0, rgb_array.shape[1] - 1)
        r_pixel = rgb_array[r_row][r_col]
        average_color += r_pixel

    return average_color / sample_count


SAMPLE_COUNT = 5000
VERBOSE = True
COM_PORT = "COM3"
BAUD_RATE = 9600

if __name__ == "__main__":
    try:
        # arduino = serial.Serial("COM3", 9600, timeout=5)
        with serial.Serial(COM_PORT, BAUD_RATE) as arduino:
            estabilish_handshake(arduino)
            arduino.timeout = 5

            print("begin")
            while True:
                imgdata = screenshot_to_rgb()

                # Calculate the dominant color
                average = calculate_average_color(imgdata, SAMPLE_COUNT)

                data_to_transmit = (
                    f"r{int(average[0])}g{int(average[1])}b{int(average[2])}E"
                )

                write(data_to_transmit, arduino)
                if VERBOSE:
                    print(data_to_transmit)

                read_from_arduino = arduino.readline()
                if VERBOSE:
                    print(read_from_arduino)

                if keyboard.is_pressed("q"):
                    print("q pressed, ending loop")
                    break

    except KeyboardInterrupt:
        print("Keyboard interrupt, ending loop")
        arduino.close()
        sys.exit(0)
