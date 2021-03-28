from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()

DEBUG = True

messageCount = 0

A0 = 0
A1 = 0
B0 = 0
B1 = 0


def hexStringToInt(pHexString, pSigned):
    # if 3 == len(pHexString):

    # pHexString = pHexString[:2] + '0' + pHexString[2:]
    # pHexString = pHexString + '0'

    little_hex = bytearray.fromhex(pHexString)

    # little_hex.reverse()

    value = int.from_bytes(little_hex, byteorder='little', signed=pSigned)

    return value


def lineProcess(pLine):

    global A0, A1, B0, B1

    line = pLine.decode("utf-8")

    line = line.rstrip()

    splitLines = line.splitlines()

    for line in splitLines:

        parts = line.split(',')

        for index, part in enumerate(parts):

            if 'A' == part:

                if index + 2 < len(parts):
                    A0 = parts[index + 1]
                    A1 = parts[index + 2]
                else:
                    print('Bad stream data?')

            elif 'B' == part:

                if index + 2 < len(parts):

                    B0 = parts[index + 1]
                    B1 = parts[index + 2]

                else:

                    print('Bad stream data?')

    print(A0, A1, B0, B1, pLine)


def start():
    messageCount = 0
    connection = None
    streamingStarted = False

    while True:

        if not connection:
            print("Searching for ble device with UART Service...")
            for adv in ble.start_scan(ProvideServicesAdvertisement):
                if UARTService in adv.services:
                    try:
                        connection = ble.connect(adv)
                    except:
                        print('Connection Failed!')
                        break

                    print("Connected")
                    break
            ble.stop_scan()

        if connection and connection.connected:

            uart_service = connection[UARTService]

            while connection.connected:

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

                    lineProcess(line)
