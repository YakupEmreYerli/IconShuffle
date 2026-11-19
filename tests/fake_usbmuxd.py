"""A pretend usbmuxd with a pretend iPhone behind it, on real sockets.

pymobiledevice3 talks to it exactly as it talks to the real service: usbmuxd's plist
protocol on the OS's own address (TCP 127.0.0.1:27015 on Windows, where Apple Mobile
Device Service listens; a Unix socket elsewhere), then lockdownd's protocol through a
``Connect``. The phone has never trusted this computer, so pairing fails with the error
the scenario names. Nothing here reaches a real device.
"""

from __future__ import annotations

import asyncio
import plistlib
import struct
from typing import Any

SERIAL = "00008120-0000FAKE0000FAKE"
WINDOWS_ADDRESS = ("127.0.0.1", 27015)


def _public_key_pem() -> bytes:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return key.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.PKCS1
    )


class FakeUsbmuxd:
    """``plugged_in``: whether the phone is on the cable. ``pair_error``: lockdownd's answer to
    ``Pair`` (``PasswordProtected`` for a locked phone, ``UserDeniedPairing`` for Don't
    Trust)."""

    def __init__(self, *, plugged_in: bool = True, pair_error: str = "PasswordProtected"):
        self.plugged_in = plugged_in
        self.pair_error = pair_error
        self.requests: list[str] = []
        self._key = _public_key_pem()

    # ----------------------------------------------------------------- usbmuxd

    async def handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            while True:
                header = await reader.readexactly(16)
                size, version, _kind, tag = struct.unpack("<4I", header)
                message = plistlib.loads(await reader.readexactly(size - 16))
                name = message.get("MessageType", "")
                self.requests.append(name)
                if name == "Connect":
                    self._reply(writer, version, tag, {"MessageType": "Result", "Number": 0})
                    await writer.drain()
                    await self._lockdown(reader, writer)
                    return
                self._reply(writer, version, tag, self._answer(name))
                await writer.drain()
        except (asyncio.IncompleteReadError, ConnectionError):
            pass
        finally:
            writer.close()

    def _answer(self, name: str) -> dict[str, Any]:
        if name == "ReadBUID":
            return {"BUID": "FAKE-SYSTEM-BUID"}
        if name == "ListDevices":
            phone = {
                "MessageType": "Attached",
                "DeviceID": 1,
                "Properties": {"SerialNumber": SERIAL, "ConnectionType": "USB"},
            }
            return {"DeviceList": [phone] if self.plugged_in else []}
        # ReadPairRecord and anything else: no such record.
        return {"MessageType": "Result", "Number": 2}

    @staticmethod
    def _reply(writer: asyncio.StreamWriter, version: int, tag: int, body: dict) -> None:
        data = plistlib.dumps(body)
        writer.write(struct.pack("<4I", 16 + len(data), version, 8, tag) + data)

    # ---------------------------------------------------------------- lockdownd

    async def _lockdown(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        values = {
            "UniqueDeviceID": SERIAL,
            "DeviceName": "Fake iPhone",
            "DeviceClass": "iPhone",
            "ProductType": "iPhone15,4",
            "ProductVersion": "26.0",
            "WiFiAddress": "a0:b1:c2:d3:e4:f5",
            "DevicePublicKey": self._key,
        }
        while True:
            (size,) = struct.unpack(">I", await reader.readexactly(4))
            request = plistlib.loads(await reader.readexactly(size))
            name = request.get("Request", "")
            self.requests.append(name)
            answer: dict[str, Any] = {"Request": name}
            if name == "QueryType":
                answer["Type"] = "com.apple.mobile.lockdown"
            elif name == "GetValue":
                key = request.get("Key")
                answer["Value"] = values.get(key) if key else values
            else:  # Pair, and StartSession without a record
                answer["Error"] = self.pair_error
            data = plistlib.dumps(answer)
            writer.write(struct.pack(">I", len(data)) + data)
            await writer.drain()
