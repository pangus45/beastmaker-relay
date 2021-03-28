import asyncio
import time
from bleak import BleakClient

MOTHERBOARD_UUID = "1F78EE57-12C1-45C5-A77F-9F407C7445B6"
LED_SERVICE_UUID = "10ababcd-15e1-28ff-de13-725bea03b127"
GREEN_LED_UUID = "10ab1525-15e1-28ff-de13-725bea03b127"
RED_LED_UUID = "10ab1524-15e1-28ff-de13-725bea03b127"

async def run(address):

    async with BleakClient(address) as client:

        while 1:

            await client.write_gatt_char(RED_LED_UUID, b'\x01')
            await client.write_gatt_char(GREEN_LED_UUID, b'\x00')

            time.sleep(1)

            await client.write_gatt_char(RED_LED_UUID, b'\x01')
            await client.write_gatt_char(GREEN_LED_UUID, b'\x01')

            time.sleep(1)

            await client.write_gatt_char(RED_LED_UUID, b'\x00')
            await client.write_gatt_char(GREEN_LED_UUID, b'\x01')

            time.sleep(1)

            await client.write_gatt_char(RED_LED_UUID, b'\x00')
            await client.write_gatt_char(GREEN_LED_UUID, b'\x00')

            time.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(run(MOTHERBOARD_UUID))


