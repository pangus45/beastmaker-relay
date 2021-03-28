# Connect to an "eval()" service over BLE UART.

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
# from adafruit_ble.services.nordic import Service
# from adafruit_ble.uuid import VendorUUID

# from adafruit_ble.characteristics.int import Uint8Characteristic
# from adafruit_ble.characteristics import Characteristic
# from adafruit_ble.characteristics import Attribute

import time

ble = BLERadio()

gConnection = None
streamingStarted = False
uartService = None

DEBUG = True

messageCount = 0


def lineProcess(pLine):

    line = pLine.decode("utf-8")

    print("Bytes: ", len(line))

    # First response in Stream:60\r\n

    if 'Stream:60\r\n' == line:
        print('Stream start message received')
        return

    if len(line) >= 20:

        SampleNumberHexString = line[0:4]
        BatteryVoltageHexString = line[4:8]

        # Sample1String = line[8:11]
        Sample2String = line[11:14]
        # Sample3String = line[14:17]
        # Sample4String = line[17:20]

        try:

            sampleNumber = hexStringToInt(SampleNumberHexString, pSigned=False)
            voltage = hexStringToInt(BatteryVoltageHexString, pSigned=False)

            # sample1 = hexStringToInt(Sample1String, pSigned=True)
            # sample2 = hexStringToInt(Sample2String, pSigned=True)
            # sample3 = hexStringToInt(Sample3String, pSigned=True)
            # sample4 = hexStringToInt(Sample4String, pSigned=True)

            print('Sample Number: ', sampleNumber, SampleNumberHexString)
            print('Voltage: ', voltage, BatteryVoltageHexString)

            # print('adc_results[0], channel0-a: ', Sample1String, sample1)
            # print('adc_results[1]: channel1-a: ', Sample2String, sample2)
            # print('adc_results[2]: channel0-b: ', Sample3String, sample3)
            # print('adc_results[3]: channel1-b: ', Sample4String, sample4)
            # 4 signed int32 split into 3 bytes in hex

        except:

            print('Byte interpretation failed')


    else:

        print("Less than 20 bytes")


def hexStringToInt(pHexString, pSigned):

    # if 3 == len(pHexString):

       # pHexString = pHexString[:2] + '0' + pHexString[2:]
       # pHexString = pHexString + '0'

    little_hex = bytearray.fromhex(pHexString)

    # little_hex.reverse()

    value = int.from_bytes(little_hex, byteorder='little', signed=pSigned)

    return value


def lineProcessDebug(pLine):

    print('*******************')
    line = pLine.decode("utf-8")

    print(len(pLine), line)


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

        uart_service = gConnection[UARTService]

        while gConnection.connected:

            if not streamingStarted:
                # 1 - standard
                # message = 's'
                # 2 - plain text
                # message = 'D'
                # 3 - plain text - 1 channel only
                # message = 'd'

                if DEBUG:
                    message = 'D'
                else:
                    message = 's'

                uart_service.write(message.encode("utf-8"))
                # uart_service.write(b'\n')

                streamingStarted = True

                break

            line = uart_service.readline()

            messageCount += 1

            if 10 == messageCount:

                messageCount = 0

                if DEBUG:
                    lineProcessDebug(line)
                else:
                    lineProcess(line)
