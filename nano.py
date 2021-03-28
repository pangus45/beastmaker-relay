import serial
import time

from serial.tools import list_ports

DOWN = 0
UP = 1

# Commands

# PORT_NAME = '/dev/cu.usbserial-1420'
PORT_TAG = 'usbserial'
BAUD_RATE = 57600

global gPort


def init():

    while True:

        global gPort

        ports = list_ports.comports()

        print("Looking for usb serial")

        for port in ports:

            # print("Checking " + port.device)

            if -1 != port.device.find(PORT_TAG):

                print('Connecting to ' + port.device)

                gPort = serial.Serial(port=port.device, timeout=1, baudrate=BAUD_RATE)

                return

        print("USB serial not found")
        time.sleep(1)


def nextMessageGet():

    line = gPort.readline()

    if line:

        print(line)
        return line

    return None


def velocitySet(pVelocity):

    message = ''

    if pVelocity > 0:

        message = message + str(UP)

    else:

        message = message + str(DOWN)
        pVelocity = -pVelocity

    message += str(pVelocity)

    messageSend(message)


def messageSend(pMessage):

    pMessage += '\n'

    print('Sending message: ' + pMessage)

    gPort.write(pMessage.encode())