# Connect to an "eval()" service over BLE UART.

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

from adafruit_ble.services import Service

ble = BLERadio()

motherboardConnection = None
servicesAdvertisement = None

initialized = False

while True:
    if not motherboardConnection:
        print("Scanning...")
        for adv in ble.start_scan(ProvideServicesAdvertisement):
            if 'Motherboard' == adv.complete_name:
                try:
                    motherboardConnection = ble.connect(adv)
                except:
                    print('Connection Failed!')
                    break

                print("Connected")
                ble.stop_scan()
                servicesAdvertisement = adv
                break

    if motherboardConnection and motherboardConnection.connected:
        for service in servicesAdvertisement.services:
            print(service)

            # serv= Service()
        # led_service = motherboardConnection[Service]
