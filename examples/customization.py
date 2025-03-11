import asyncio

from pytelnetdevice import TelnetDevice


class MyDevice(TelnetDevice):
    async def before_disconnect(self):
        print("Before disconnect logic")

    async def after_connect(self):
        print("After connect logic")


async def main():
    device = MyDevice("10.211.0.91", 23)

    await device.connect()
    print("Connected!")
    await device.disconnect()
    print("Disconnected")


asyncio.run(main())
