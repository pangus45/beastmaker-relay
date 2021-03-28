import asyncio
import platform

from bleak import BleakClient, BleakScanner

MOTHERBOARD_UUID = "1F78EE57-12C1-45C5-A77F-9F407C7445B6"

# Device.devices = {};
# Device.uuidServiceUart = '6e400001-b5a3-f393-e0a9-e50e24dcca9e';
# Device.uuidCharacteristicTx = '6e400002-b5a3-f393-e0a9-e50e24dcca9e';
# Device.uuidCharacteristicRx = '6e400003-b5a3-f393-e0a9-e50e24dcca9e';


async def run():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device.name)
        if device.name == 'Motherboard':
            device = await BleakScanner.find_device_by_address(device.address)
            async with BleakClient(device) as client:
                svcs = await client.get_services()
                print("Services Found...")
                for service in svcs:
                    print("Service: " + service.uuid)
                    for char in service.characteristics:
                        print("Char: " + char.uuid)
                    print("")





loop = asyncio.get_event_loop()
loop.run_until_complete(run())