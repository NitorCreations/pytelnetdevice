# pytelnetdevice

[![Linting](https://github.com/NitorCreations/pytelnetdevice/actions/workflows/ruff.yaml/badge.svg)](https://github.com/NitorCreations/pytelnetdevice/actions/workflows/ruff.yaml)

Base building block for libraries designed to communicate with Telnet-based devices. 
It aims to abstract away the boilerplate needed to connect and disconnect from 
devices, read bytes, handle eventual handshake requirements and ensuring concurrent 
access doesn't cause troubles.

The library has no external dependencies.

## Usage

In the simplest form we simply connect and disconnect to a device:

```python3
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
```

### Synchronization

There are two mechanisms you can use to serialize access to the device, depending on how you want to handle 
connections.

#### Semaphore

The built-in semaphore is handy if you want to maintain a long-running connection and serialize and commands that 
should be executed on the device:

```python
import asyncio

from pytelnetdevice import TelnetDevice


class MyDevice(TelnetDevice):
    async def connect(self):
        print("Connecting to device")
        return await super().connect()

    async def run_command(self, command: str) -> None:
        async with self._semaphore:
            print(f"Running command {command}")
            # Simulate response that takes a while
            await asyncio.sleep(1)


async def main():
    device = MyDevice("10.211.0.91", 23)

    await device.connect()
    await asyncio.gather(
        *[
            device.run_command("foo"),
            device.run_command("bar"),
            device.run_command("baz"),
        ]
    )


asyncio.run(main())
```

The above will print:

```
Connecting to device
Running command foo
Running command bar
Running command baz
```

#### Connection context

You can also use a connection context to open and hold an exclusive connection while executing the command:

```python
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
```

The above will print:

```
Connecting to device
Running command foo
Connecting to device
Running command bar
Connecting to device
Running command baz
```

### Customization

Some devices may require a form of handshake after a new connection is opened before they begin accepting commands. 
You can implement this logic by overriding `after_connect()` and/or `before_disconnect()`:

```python
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
```

The above will print:

```
After connect logic
Connected!
Before disconnect logic
Disconnected
```

## License

GNU GENERAL PUBLIC LICENSE version 3
