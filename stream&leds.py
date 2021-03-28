# Connect to an "eval()" service over BLE UART.

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.services.nordic import Service
from adafruit_ble.uuid import VendorUUID

from adafruit_ble.characteristics.int import Uint8Characteristic
from adafruit_ble.characteristics import Characteristic
from adafruit_ble.characteristics import Attribute

import time

LED_SERVICE_UUID = "10ababcd-15e1-28ff-de13-725bea03b127"
GREEN_LED_UUID = "10ab1525-15e1-28ff-de13-725bea03b127"
RED_LED_UUID = "10ab1524-15e1-28ff-de13-725bea03b127"

ble = BLERadio()

gConnection = None
initialized = False

ledService = None
uartService = None


class LEDService(Service):

    uuid = VendorUUID(LED_SERVICE_UUID)

    redChar = Uint8Characteristic(uuid=VendorUUID(RED_LED_UUID), properties=Characteristic.WRITE_NO_RESPONSE)
    greenChar = Uint8Characteristic(uuid=VendorUUID(GREEN_LED_UUID), properties=Characteristic.WRITE_NO_RESPONSE)

    phase = 0

    def phaseChange(self):

        self.phase = self.phase + 1

        if self.phase > 3:
            self.phase = 0

        if 0 == self.phase:
            self.charsWrite(1, 0)
        elif 1 == self.phase:
            self.charsWrite(1, 1)
        elif 2 == self.phase:
            self.charsWrite(0, 1)
        elif 3 == self.phase:
            self.charsWrite(0, 0)

    def charsWrite(self, pRed, pGreen):

        self.redCharWrite(pRed)
        self.greenCharWrite(pGreen)

    def redCharWrite(self, pValue):

        self.redChar = pValue

    def greenCharWrite(self, pValue):

        self.greenChar = pValue


def flashLoop():

    global ledService

    # for i in range(2):

    for j in range(3):

        # print(j)
        ledService.phaseChange()
        time.sleep(1)

while True:
    if not gConnection:
        print("Trying to connect...")
        for adv in ble.start_scan(ProvideServicesAdvertisement):
            if UARTService in adv.services:
                try:
                    gConnection = ble.connect(adv)
                except:
                    print('Connection Failed!')
                    break

                print("Connected")
                break
        ble.stop_scan()

    if gConnection and gConnection.connected:

        ledService = gConnection[LEDService]

        flashLoop()

        uart_service = gConnection[UARTService]

        while gConnection.connected:

            if not initialized:
                # 1 - standard
                message = 's'
                # 2 - plain text
                # message = 'D'
                # 3 - plain text - 1 channel only
                # message = 'd'

                uart_service.write(message.encode("utf-8"))
                # uart_service.write(b'\n')

                initialized = True

                break

            line = uart_service.readline()

            ledService.phaseChange()

            # s = input("Eval: ")
            # uart_service.write(s.encode("utf-8"))
            # uart_service.write(b'\n')
            # print(line)
            print(len(line))
            print(line.decode("utf-8"))
