import asyncio

from pytelnetdevice import TelnetDevice


class MyDevice(TelnetDevice):
    pass


async def main():
    device = MyDevice("10.211.0.91", 23)

    await device.connect()
    print("Connected!")
    await device.disconnect()
    print("Disconnected")


asyncio.run(main())
