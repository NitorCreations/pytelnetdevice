import asyncio

from pytelnetdevice import TelnetDevice


class MyDevice(TelnetDevice):
    async def connect(self):
        print("Connecting to device")
        return await super().connect()

    async def run_command(self, command: str) -> None:
        async with self.connection():
            print(f"Running command {command}")
            # Simulate response that takes a while
            await asyncio.sleep(1)


async def main():
    device = MyDevice("10.211.0.91", 23)

    await asyncio.gather(
        *[
            device.run_command("foo"),
            device.run_command("bar"),
            device.run_command("baz"),
        ]
    )


asyncio.run(main())
